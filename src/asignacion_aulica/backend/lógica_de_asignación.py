'''
Este módulo resuelve el problema lógico de asignación de aulas
usando el solucionador de restricciones `ortools`.

Ver manual de ortools: https://developers.google.com/optimization/cp

Se define un modelo con los siguientes componentes:
- Variables: Cada variable es el número de aula que tiene asignada una clase.
  El número de aula 0 significa que no tiene asignada un aula.

- Restricciones: Cada restricción es una condición booleana que se tiene que
  cumplir para que la asignación de aulas no sea incorrecta.

- Penalizaciones: Son un puntaje que se asigna a las situaciones que no generan
  una asignación de aulas incorrecta, pero que preferimos evitar si es posible.

Luego se usa el solver para encontrar una combinación de variables que cumpla
con todas las restricciones y que tenga la menor penalización posible.
'''
from ortools.sat.python import cp_model
from pandas import DataFrame

from .impossible_assignment_exception import ImposibleAssignmentException
from .restricciones import todas_las_restricciones
from .constantes import DÍAS_DE_LA_SEMANA

def asignar(aulas: DataFrame, materias: DataFrame) -> DataFrame:
    '''
    Resolver el problema de asignación.

    :param aulas: Tabla con los datos de todas las aulas disponibles.
        Un aula por fila, con la numeración empezando en 1.
        Columnas:
        - edificio
        - nombre
        - capacidad
        - equipamiento
    
    :param materias: Tabla con los datos de todas las materias.
        Una materia por fila.
        Los horarios de inicio y fin se ignoran cuando la modalidad es no.
        Columnas:
        - nombre (incluye comisión)
        - cantidad de alumnos
        - equipamiento necesario
        - edificio preferido
        - modalidad lunes (presencial, virtual, o no)
        - horario inicio lunes
        - horario fin lunes
        - modalidad martes (presencial, virtual, o no)
        - horario inicio martes
        - horario fin martes
        - modalidad miércoles (presencial, virtual, o no)
        - horario inicio miércoles
        - horario fin miércoles
        - modalidad jueves (presencial, virtual, o no)
        - horario inicio jueves
        - horario fin jueves
        - modalidad viernes (presencial, virtual, o no)
        - horario inicio viernes
        - horario fin viernes
        - modalidad sábado (presencial, virtual, o no)
        - horario inicio sábado
        - horario fin sábado
    
    :return: Tabla con las aulas asignadas.
        Cada fila es una materia, cada columna es un día, y cada celda tiene el
        número de aula que se le asignó a esa materia para la clase de ese día.
        El número 0 significa que no hay un aula asignada.
    
    :raise ImposibleAssignmentException: Si no es posible hacer la asignación.
    '''
    # Modelo que contiene las variables, restricciones, y penalizaciones
    modelo = cp_model.CpModel()
    asignaciones = crear_tabla_de_asignaciones(modelo, materias, len(aulas))
    
    # Agregar al modelo las restricciones:
    for restricción in todas_las_restricciones:
        for predicado in restricción(materias=materias, aulas=aulas, asignaciones=asignaciones):
            modelo.Add(predicado)

    # El resolvedor que resuelve
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    status_name = solver.status_name(status)
    if status_name != 'OPTIMAL':
        raise ImposibleAssignmentException(f'El solucionador de restricciones terminó con status {status_name}.')

    # Armar tabla con las asignaciones
    resultados = asignaciones.map(lambda x: solver.Value(x))
    
    return resultados
    
def crear_tabla_de_asignaciones(
    modelo: cp_model.CpModel,
    materias: DataFrame,
    n_aulas: int
    ) -> DataFrame:
    '''
    Agrega al modelo una variable por cada materia y por cada día, que
    representa el número de aula que tiene asignada esa materia ese día.

    :return: Una tabla con una fila por materia y una columna por día.
        Cada celda de la tabla es una variable del modelo que corresponde al
        número de aula que tiene esa materia ese día.
    '''
    asignaciones = DataFrame(index=materias.index, columns=DÍAS_DE_LA_SEMANA)

    for i in materias.index:
        for día in DÍAS_DE_LA_SEMANA:
            asignaciones.loc[i, día] = modelo.NewIntVar(0, n_aulas, f'aula_materia_{i}_{día}')
    
    return asignaciones
  