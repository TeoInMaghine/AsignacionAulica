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
from pandas import DataFrame
import numpy as np

from .impossible_assignment_exception import ImposibleAssignmentException
from asignacion_aulica.lógica_de_asignación import restricciones
from .dia import Día
from .preferencias import obtener_penalización

def asignar(clases: DataFrame, aulas: DataFrame, aulas_dobles: dict[ int, tuple[int,int] ] = {}):
    '''
    Resolver el problema de asignación.

    Las aulas asignadas se representan en la columna 'aula_asignada' de la tabla
    de clases. Las clases con asignaciones manuales tienen un número de aula en
    esta columna, y las clases que no tienen un aula asignada tienen `None`.

    Esta función asigna aulas a las clases que no tienen un aula asignada
    manualmente, y reemplaza el valor `None` con el número de aula que se
    asignó.

    :param clases: Tabla con los datos de todas las clases.
        Una clase por fila.
        Columnas:
        - nombre: str (materia y comisión)
        - día: Día
        - horario_inicio: int (medido en minutos)
        - horario_fin: int (medido en minutos)
        - cantidad_de_alumnos: int
        - equipamiento_necesario: set[str]
        - edificio_preferido: Optional[str]
        - aula_asignada: Optional[int]
    
    :param aulas: Tabla con los datos de todas las aulas disponibles.
        Columnas:
        - edificio: str
        - nombre: str
        - capacidad: int
        - equipamiento: set[str]
        - horarios: dict[Día, tuple[int, int]]
          Mapea días de la semana a tuplas (apertura, cierre). Los días que no
          están en el diccionario se considera que el aula está cerrada.
          Apertura y cierre se miden en minutos.
    
    :param aulas_dobles: Diccionario donde las keys son los índices de las
        aulas dobles y los valores son tuplas con las aulas individuales que
        conforman el aula doble.
    
    :raise ImposibleAssignmentException: Si no es posible hacer la asignación.
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
    # Crear modelo, variables, restricciones, y penalizaciones
    modelo = cp_model.CpModel()
    asignaciones = crear_matriz_de_asignaciones(clases, aulas, aulas_dobles, aulas_ocupadas, modelo)

    for predicado in restricciones.restricciones_con_variables(clases, aulas, aulas_dobles, asignaciones):
        modelo.add(predicado)
    
    penalización = obtener_penalización(clases, aulas, modelo, asignaciones)
    modelo.minimize(penalización)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    # TODO: ¿qué hacer si da FEASIBLE?¿en qué condiciones ocurre?¿aceptamos la solución suboptima o tiramos excepción?
    if status != cp_model.OPTIMAL:
        raise ImposibleAssignmentException(f'El solucionador de restricciones terminó con status {solver.status_name(status)}.')
    
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

