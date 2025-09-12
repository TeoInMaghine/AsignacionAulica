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
from pandas import DataFrame
import numpy as np
import logging

from asignacion_aulica.gestor_de_datos import Edificio, Aula, Carrera, Materia, Clase, Día
from asignacion_aulica.lógica_de_asignación.excepciones import AsignaciónImposibleException
from asignacion_aulica.lógica_de_asignación.preferencias import obtener_penalización
from asignacion_aulica.lógica_de_asignación import restricciones

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
    inicialmente es indistinto).

    A las clases con `no_cambiar_asignación == True` no se les modifica nada,
    pero se tiene en cuenta el aula que tienen asignada para evitar
    superposiciones.
    
    :param edificios: Los edificios disponibles. #TODO: ¿pueden venir ordenados de la base de datos?
    :param aulas: Las aulas disponibles en todos los edificios. #TODO: ¿pueden venir ordenadas por edificio?
    :param carreras: Las carreras que existen. #TODO: orden?
    :param materias: Las materias de todas las carreras. #TODO: orden?
    :param clases: Las clases de todas las materias. #TODO: pueden venir ordenadas por carrera y materia?
    
    :raise AsignaciónImposibleException: Si no es posible asignar aula a una o
    más clases.
    '''
    # Las clases con asignaciones manuales no son parte del problema de
    # asignación, sólo generan restricciones de aulas ocupadas.
    clases_sin_asignar, índices_sin_asignar, aulas_ocupadas = separar_asignaciones_manuales(clases)

    # Resolver el problema de asignación de las aulas no asignadas manualmente
    asignaciones = resolver_problema_de_asignación(clases_sin_asignar, aulas, aulas_dobles, aulas_ocupadas)

    # Escribir los resultados en la tabla de clases
    clases.loc[índices_sin_asignar, 'aula_asignada'] = asignaciones


def separar_asignaciones_manuales(clases: DataFrame) -> tuple[ DataFrame, list[int], set[tuple[int, Día, int, int]] ]:
    '''
    Separa los datos de la clases que ya tienen aulas asignadas.

    :return:
        - Una copia de la tabla de clases pero sin las filas de las clases con
          asignación manual
        - Una lista de los índices (en la tabla original) de las clases sin
          asignación manual
        - Un set de horarios en los que algunas aulas están ocupadas con
          las asignaciones maunales, en tuplas (aula, día, inicio, fin).
    '''
    sin_asignar = clases['aula_asignada'].isnull()
    clases_sin_asignar = clases[sin_asignar].copy()
    índices_sin_asignar = list(clases_sin_asignar.index)
    clases_sin_asignar.reset_index(drop=True, inplace=True)
    
    aulas_ocupadas = {
        (clase.aula_asignada, clase.día, clase.horario_inicio, clase.horario_fin)
        for clase in clases[~sin_asignar].itertuples()
    }

    return clases_sin_asignar, índices_sin_asignar, aulas_ocupadas

def resolver_problema_de_asignación(
    clases: DataFrame,
    aulas: DataFrame,
    aulas_dobles: dict[ int, tuple[int,int] ],
    aulas_ocupadas: set[tuple[int, Día, int, int]]
    ) -> list[int]:
    '''
    El docstring de `asignar` miente, la que resuelve el problema de asignación
    soy yo!

    Pero no manejo el tema de las asignaciones manuales.

    :param aulas_ocupadas: Horarios en los que algunas aulas están ocupadas con
        otra cosa, en tuplas (aula, día, inicio, fin).
    :return: Una lista con el número de aula asignada a cada clase.
    '''

    if clases.empty:
        return []

    # Crear modelo, variables, restricciones, y penalizaciones
    modelo = cp_model.CpModel()
    asignaciones = crear_matriz_de_asignaciones(clases, aulas, aulas_dobles, aulas_ocupadas, modelo)

    for predicado in restricciones.restricciones_con_variables(clases, aulas, aulas_dobles, asignaciones):
        modelo.add(predicado)
    
    penalización = obtener_penalización(clases, aulas, modelo, asignaciones)
    modelo.minimize(penalización)

    # Resolver
    solver = cp_model.CpSolver()

    # Loguear progreso de forma limpia
    solver.parameters.log_search_progress = True
    solver.parameters.log_to_stdout = False
    solver.log_callback = logging.debug

    status = solver.solve(modelo)
    # TODO: ¿qué hacer si da FEASIBLE?¿en qué condiciones ocurre?¿aceptamos la solución suboptima o tiramos excepción?
    if status != cp_model.OPTIMAL:
        raise AsignaciónImposibleException(f'El solucionador de restricciones terminó con status {solver.status_name(status)}.')
    
    # Armar lista con las asignaciones
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    aulas_asignadas = list(asignaciones_finales.argmax(axis=1))

    return aulas_asignadas

def crear_matriz_de_asignaciones(
    clases: DataFrame,
    aulas: DataFrame,
    aulas_dobles: dict[ int, tuple[int,int] ],
    aulas_ocupadas: set[tuple[int, Día, int, int]],
    modelo: cp_model.CpModel
    ) -> np.ndarray:
    '''
    Genera una matriz con las variables de asignación.

    Las filas de la matriz representan clases y las columnas representan aulas.
    Cada elemento de la matriz es un booleano que indica si ese aula está
    asignada a esa clase. El booleano puede ser una constante 0, o puede ser una
    variable booleana del modelo.

    Algunos elementos de la matriz se inicializan con las constantes que se
    pueden deducir de las restricciones. Luego se agregan variables al modelo
    para completar los elementos restantes.

    También se agregan restricciones para que cada clase se asigne exactamente a
    un aula.

    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param aulas_dobles: Diccionario donde las keys son los índices de las
        aulas dobles y los valores son tuplas con las aulas individuales que
        conforman el aula doble.
    :param aulas_ocupadas: Horarios en los que algunas aulas están ocupadas con
        otra cosa, en tuplas (aula, día, inicio, fin).
    :param modelo: El CpModel al que agregar variables.
    :return: La expresión de penalización total.
    '''
    asignaciones = np.empty(shape=(len(clases), len(aulas)), dtype=object)

    # Popular con constantes
    for índices in restricciones.aulas_prohibidas(clases, aulas, aulas_dobles, aulas_ocupadas):
        asignaciones[*índices] = 0
    
    # Rellenar los elementos vacíos con variables
    for clase, aula in np.ndindex(asignaciones.shape):
        if asignaciones[clase, aula] is None:
            asignaciones[clase, aula] = modelo.new_bool_var(f'clase_{clase}_asignada_al_aula_{aula}')
    
    # Asegurar que cada clase se asigna a exactamente un aula
    for clase in clases.index:
        modelo.add_exactly_one(asignaciones[clase,:])
    
    return asignaciones

