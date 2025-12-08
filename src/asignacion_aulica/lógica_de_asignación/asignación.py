'''
Este módulo resuelve el problema lógico de asignación de aulas usando el
solucionador de restricciones CP-SAT de `ortools`.

Ver manual de ortools: https://developers.google.com/optimization/cp

Se define un modelo (CpModel) con los siguientes componentes:
- Matriz de variables de asignación: Es una matriz donde cada fila representa
  una clase, cada columna representa un aula, y cada celda contiene un booleano
  que indica si esa clase está asignada a ese aula.

  Los booleanos están codificados como 0 (False) o 1 (True) porque así lo pide
  la interfaz de ortools. Algunas celdas contienen constantes (asignaciones
  fijas) y otras contienen variables del modelo (asignaciones a ser resueltas
  por ortools).

- Restricciones: Cada restricción es una condición booleana que se tiene que
  cumplir para que la asignación de aulas sea correcta.

- Penalizaciones: Son un puntaje que se asigna a las situaciones que preferimos
  evitar si es posible, aunque no generen una asignación de aulas incorrecta.

Luego se usa el solver para encontrar una combinación de variables que cumpla
con todas las restricciones y que tenga la menor penalización posible.
'''
from ortools.sat.python import cp_model
import numpy as np
import logging

from asignacion_aulica.lógica_de_asignación.excepciones import AsignaciónImposibleException
from asignacion_aulica.lógica_de_asignación.postprocesamiento import InfoPostAsignación
from asignacion_aulica.lógica_de_asignación.preferencias import obtener_penalización
from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificios, Carreras
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día
from asignacion_aulica.lógica_de_asignación import restricciones
from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulasPreprocesadas, ClasesPreprocesadas, ClasesPreprocesadasPorDía, preprocesar_clases
)

logger = logging.getLogger(__name__)

def asignar(edificios: Edificios, carreras: Carreras) -> InfoPostAsignación:
    '''
    Asignar aula a todas las clases presenciales que no tienen una asignación
    fijada.

    A las clases con `no_cambiar_asignación == False` se les asigna un aula y se
    les sobreescribe el atributo `aula_asignada` (el valor que tenga
    inicialmente es ignorado).

    A las clases con `no_cambiar_asignación == True` no se les modifica nada,
    pero se tiene en cuenta el aula que tienen asignada para evitar
    superposiciones.
    
    :param edificios: Los edificios disponibles.
    :param carreras: Las carreras que existen.
    
    :return: Info sobre el resultado de la asignación.
    '''
    # Preprocesar los datos
    aulas_preprocesadas: AulasPreprocesadas = AulasPreprocesadas(edificios)
    clases_preprocesadas: ClasesPreprocesadasPorDía = preprocesar_clases(carreras, aulas_preprocesadas)

    # Asignar las aulas de cada día
    días_sin_asignar: list[Día] = []
    for día in Día:
        clases_del_día = clases_preprocesadas[día]
        try:
            asignaciones: list[int] = resolver_problema_de_asignación(clases_del_día, aulas_preprocesadas)
        except AsignaciónImposibleException as exc:
            logger.error('Falló la asignación para el día %s: %s', día.name, exc)
            días_sin_asignar.append(día)
        else:
            # Si no hubo excepciones, asignar las aulas a las clases que se pasaron por argumento
            for clase, i_aula_asignada in zip(clases_del_día.clases, asignaciones):
                aula_asignada: Aula = aulas_preprocesadas.aulas[i_aula_asignada].aula_original
                clase.aula_asignada = aula_asignada
    
    # Postprocesar los datos
    reporte = InfoPostAsignación(edificios, carreras, días_sin_asignar)
    
    return reporte

def resolver_problema_de_asignación(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas
) -> list[int]:
    '''
    Asignar aulas a todas las clases en un problema de asignación.

    :param clases: Los datos de las clases de el problema de asignación.
    :pram aulas: Los datos de las aulas disponibles.

    :return: Una lista con el índice del aula asignada a cada clase.
    :raise AsignaciónImposibleException: Si el CpModel no se puede resolver. 
    '''
    if len(clases.clases) == 0:
        return []

    # Crear modelo, variables, restricciones, y penalizaciones
    modelo = cp_model.CpModel()
    asignaciones = crear_matriz_de_asignaciones(clases, aulas, modelo)

    for predicado in restricciones.restricciones_con_variables(clases, aulas, asignaciones):
        modelo.add(predicado)
    
    penalización = obtener_penalización(clases, aulas, modelo, asignaciones)
    modelo.minimize(penalización)

    # Resolver (setear log_search_progress para loggear el proceso)
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = False #True
    solver.parameters.log_to_stdout = False
    solver.log_callback = logger.debug

    logger.info('Resolviendo el modelo para el día %s.', clases.clases[0].día.name)
    status = solver.solve(modelo)
    # TODO: ¿qué hacer si da FEASIBLE?¿en qué condiciones ocurre?¿aceptamos la solución suboptima o tiramos excepción?
    if status != cp_model.OPTIMAL:
        raise AsignaciónImposibleException(f'El solucionador de restricciones terminó con status {solver.status_name(status)}.')
    
    # Armar lista con las asignaciones
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    aulas_asignadas = list(asignaciones_finales.argmax(axis=1))

    return aulas_asignadas

def crear_matriz_de_asignaciones(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    modelo: cp_model.CpModel
) -> np.ndarray:
    '''
    Genera una matriz con las variables de asignación.

    Las filas de la matriz representan clases y las columnas representan aulas.
    Cada elemento de la matriz es un booleano que indica si ese aula está
    asignada a esa clase. El booleano puede ser una constante 0, o puede ser una
    variable booleana del modelo.

    Algunos elementos de la matriz se inicializan con las constantes 0 que se
    pueden deducir de las restricciones. Luego se agregan variables al modelo
    para completar los elementos restantes.

    También se agregan restricciones para que cada clase se asigne exactamente a
    un aula.
    
    :param clases: Los datos de las clases del problema de asignación.
    :pram aulas: Los datos de las aulas disponibles.
    :param modelo: El CpModel al que agregar variables.

    :return: La matriz con las variables de asignación.
    '''
    asignaciones = np.empty(shape=(len(clases.clases), len(aulas.aulas)), dtype=object)

    # Popular con constantes
    for índices in restricciones.aulas_prohibidas(clases, aulas):
        asignaciones[*índices] = 0
    
    # Rellenar los elementos vacíos con variables
    for i_clase, i_aula in np.ndindex(asignaciones.shape):
        if asignaciones[i_clase, i_aula] is None:
            asignaciones[i_clase, i_aula] = modelo.new_bool_var(f'clase_{i_clase}_asignada_al_aula_{i_aula}')
    
    # Asegurar que cada clase se asigna a exactamente un aula
    for clase in asignaciones:
        modelo.add_exactly_one(clase)
    
    return asignaciones
