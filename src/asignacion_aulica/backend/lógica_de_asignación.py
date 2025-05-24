'''
Este módulo resuelve el problema lógico de asignación de aulas
usando el solucionador de restricciones `ortools`.

Ver manual de ortools: https://developers.google.com/optimization/cp

Se define un modelo con los siguientes componentes:
- Variables: Cada variable es el número de aula que tiene asignada una clase.
  El número de aula 0 significa que no tiene asignada un aula.

- Restricciones: Cada restricción es una condición booleana que se tiene que
  cumplir para que la asignación de aulas sea correcta.

- Penalizaciones: Son un puntaje que se asigna a las situaciones que preferimos
  evitar si es posible, aunque no generen una asignación de aulas incorrecta.

Luego se usa el solver para encontrar una combinación de variables que cumpla
con todas las restricciones y que tenga la menor penalización posible.
'''
from ortools.sat.python import cp_model
from pandas import DataFrame

from .impossible_assignment_exception import ImposibleAssignmentException
from .restricciones import todas_las_restricciones

def asignar(aulas: DataFrame, clases: DataFrame) -> list[int]:
    '''
    Resolver el problema de asignación.

    :param aulas: Tabla con los datos de todas las aulas disponibles.
        Columnas:
        - edificio
        - nombre
        - capacidad
        - equipamiento
        - horario apertura
        - horario cierre
    :param clases: Tabla con los datos de todas las clases.
        Una clase por fila.
        Columnas:
        - nombre (materia y comisión)
        - día (de la semana)
        - horario inicio #TODO: Decidir cómo representar los horarios en números enteros
        - horario fin
        - cantidad de alumnos
        - equipamiento necesario
        - edificio preferido
    :return: Lista con el número de aula asignada a cada clase
    :raise ImposibleAssignmentException: Si no es posible hacer la asignación.
    '''
    # Modelo que contiene las variables, restricciones, y penalizaciones
    modelo = cp_model.CpModel()
    
    # Agregar al modelo una variable por cada clase, que representa el
    # número de aula que tiene asignada esa clase.
    max_aula = len(aulas) - 1
    variables = [modelo.new_int_var(0, max_aula, f'aula_clase_{i}') for i in clases.index]
    
    # Agregar al modelo las restricciones
    for predicado in todas_las_restricciones(clases, aulas, variables):
        modelo.add(predicado)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    status_name = solver.status_name(status)
    if status_name != 'OPTIMAL':
        raise ImposibleAssignmentException(f'El solucionador de restricciones terminó con status {status_name}.')

    # Armar lista con las asignaciones
    aulas_asignadas = list(map(solver.value, variables))
    
    return aulas_asignadas
  