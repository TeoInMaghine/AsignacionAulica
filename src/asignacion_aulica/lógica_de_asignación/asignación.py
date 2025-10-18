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
from collections.abc import Sequence
import numpy as np
import logging

from asignacion_aulica.gestor_de_datos.entidades import Edificio, Aula, Carrera, Materia, Clase
from asignacion_aulica.lógica_de_asignación.excepciones import AsignaciónImposibleException
from asignacion_aulica.lógica_de_asignación.preferencias import obtener_penalización
from asignacion_aulica.lógica_de_asignación import restricciones
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día
from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulasPreprocesadas, ClasesPreprocesadas, preprocesar_clases
)

logger = logging.getLogger(__name__)

def asignar(
    edificios: Sequence[Edificio],
    aulas: Sequence[Aula],
    carreras: Sequence[Carrera],
    materias: Sequence[Materia],
    clases: Sequence[Clase],
):
    '''
    Asignar aula a todas las clases presenciales que no tienen una asignación
    fijada.

    A las clases con `no_cambiar_asignación == False` se les asigna un aula y se
    sobreescriben sus atributos `aula` y `edificio` (el valor que tengan
    inicialmente es ignorado).

    A las clases con `no_cambiar_asignación == True` no se les modifica nada,
    pero se tiene en cuenta el aula que tienen asignada para evitar
    superposiciones.
    
    :param edificios: Los edificios disponibles (ordenados alfabéticamente).
    :param aulas: Las aulas disponibles en cada uno de los edificios (agrupadas
    por edificio, en el mismo orden que la secuencia de edificios, y dentro de
    cada edificio ordenadas alfabéticamente).
    :param carreras: Las carreras que existen, en orden alfabético.
    :param materias: Las materias de todas las carreras (agrupadas por carrera
    en el mismo orden que la secuencia de carreras).
    :param clases: Las clases de todas las materias (agrupadas por materia, en
    el mismo orden que la secuencia de materias).
    
    :raise AsignaciónImposibleException: Si no es posible asignar aula a una o
    más clases.
    '''
    # Preprocesar los datos
    aulas_preprocesadas: AulasPreprocesadas = AulasPreprocesadas(edificios, aulas)
    clases_preprocesadas = preprocesar_clases(carreras, materias, clases, aulas_preprocesadas)

    # Asignar las aulas de cada día
    días_sin_asignar: list[Día] = []
    for día, clases_del_día in zip(Día, clases_preprocesadas):
        try:
            asignaciones: list[int] = resolver_problema_de_asignación(clases_del_día, aulas_preprocesadas)
        except RuntimeError as err:
            logger.error('Falló la asignación para el día %s: %s', día.name, err)
            días_sin_asignar.append(día)
        else:
            for i_clase, i_aula in zip(clases_del_día.índices_originales, asignaciones):
                clase = clases[i_clase]
                aula = aulas[i_aula]
                clase.edificio = aula.edificio
                clase.aula = aula.nombre
    
    # Tirar excepción si no se pudo asignar algún día
    if len(días_sin_asignar) != 0:
        raise AsignaciónImposibleException(*días_sin_asignar)

def resolver_problema_de_asignación(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas
) -> list[int]:
    '''
    Asignar aulas a todas las clases en un problema de asignación.

    :param clases: Los datos de las clases de el problema de asignación.
    :pram aulas: Los datos de las aulas disponibles.

    :return: Una lista con el número de aula asignada a cada clase.
    :raise RuntimeError: Si el CpModel no se puede resolver. 
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

    # Resolver (loggueando el proceso)
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    solver.parameters.log_to_stdout = False
    solver.log_callback = logger.debug

    status = solver.solve(modelo)
    # TODO: ¿qué hacer si da FEASIBLE?¿en qué condiciones ocurre?¿aceptamos la solución suboptima o tiramos excepción?
    if status != cp_model.OPTIMAL:
        raise RuntimeError(f'El solucionador de restricciones terminó con status {solver.status_name(status)}.')
    
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
    
    :param clases: Los datos de las clases de el problema de asignación.
    :pram aulas: Los datos de las aulas disponibles.
    :param modelo: El CpModel al que agregar variables.

    :return: La matriz con las variables de asignación.
    '''
    asignaciones = np.empty(shape=(len(clases.clases), len(aulas.aulas)), dtype=object)

    # Popular con constantes
    for índices in restricciones.aulas_prohibidas(clases, aulas):
        asignaciones[*índices] = 0
    
    # Rellenar los elementos vacíos con variables
    for asignaciones_de_una_clase, aula in np.ndindex(asignaciones.shape):
        if asignaciones[asignaciones_de_una_clase, aula] is None:
            asignaciones[asignaciones_de_una_clase, aula] = modelo.new_bool_var(f'clase_{asignaciones_de_una_clase}_asignada_al_aula_{aula}')
    
    # Asegurar que cada clase se asigna a exactamente un aula
    for asignaciones_de_una_clase in asignaciones:
        modelo.add_exactly_one(asignaciones_de_una_clase)
    
    return asignaciones
