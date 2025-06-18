from ortools.sat.python import cp_model
from pandas import DataFrame
import numpy as np

def make_aulas(*data):
    '''
    Recibe una lista de diccionarios con datos (posiblemente incompletos) de
    aulas.

    Rellena esos datos con valores por defecto y los devuelve en un DataFrame
    con el formato esperado por las funciones de backend.
    '''
    default_values = {
        'edificio': 'edificio',
        'nombre': 'aula',
        'capacidad': 1,
        'equipamiento': set(),
        'horarios': {
            'lunes':     (0, 24),
            'martes':    (0, 24),
            'miércoles': (0, 24),
            'jueves':    (0, 24),
            'viernes':   (0, 24),
            'sábado':    (0, 24),
            'domingo':   (0, 24)
        }
    }

    return DataFrame.from_records(default_values | explicit_values for explicit_values in data)

def make_clases(*data):
    '''
    Recibe una lista de diccionarios con datos (posiblemente incompletos) de
    clases.

    Rellena esos datos con valores por defecto y los devuelve en un DataFrame
    con el formato esperado por las funciones de backend.
    '''
    default_values = {
        'nombre': 'materia',
        'día': 'lunes',
        'horario_inicio': 10,
        'horario_fin': 11,
        'cantidad_de_alumnos': 1,
        'equipamiento_necesario': set(),
        'edificio_preferido': 'edificio'
    }

    clases = DataFrame.from_records(default_values | explicit_values for explicit_values in data)

    return clases

def make_asignaciones(clases: DataFrame, aulas: DataFrame, modelo: cp_model.CpModel) -> np.ndarray:
    '''
    Genera una matriz con las variables de asignación. No hay constantes, todas
    son variables que se agregan al modelo.

    También se agregan restricciones para que cada clase se asigne exactamente a
    un aula.

    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param modelo: El CpModel al que agregar variables.
    :return: La expresión de penalización total.
    '''
    asignaciones = np.empty(shape=(len(clases), len(aulas)), dtype=object)
    
    for clase, aula in np.ndindex(asignaciones.shape):
        asignaciones[clase, aula] = modelo.new_bool_var(f'clase_{clase}_asignada_al_aula_{aula}')
    
    # Asegurar que cada clase se asigna a exactamente un aula
    for clase in clases.index:
        modelo.add_exactly_one(asignaciones[clase,:])
    
    return asignaciones

def predicado_es_not_equals_entre_variable_y_constante(predicado, constante):
    '''
    Devuelve `True` si `predicado` es una expresión de la forma `variable != constante`,
    donde `variable` es una variable de un `CpModel`.
    '''
    return isinstance(predicado, cp_model.BoundedLinearExpression) \
        and len(predicado.vars) == 1 \
        and predicado.coeffs == [1] \
        and predicado.offset == 0 \
        and predicado.bounds.complement().flattened_intervals() == [constante, constante]

def predicado_es_not_equals_entre_dos_variables(predicado):
    '''
    Devuelve `True` si `predicado` es una expresión de la forma `variable1 != variable2`,
    donde `variable1` y `variable2` son variables de un `CpModel`.
    '''
    return isinstance(predicado, cp_model.BoundedLinearExpression) \
        and len(predicado.vars) == 2 \
        and predicado.coeffs == [1, -1] \
        and predicado.offset == 0 \
        and predicado.bounds.complement().flattened_intervals() == [0, 0]

def predicado_es_nand_entre_dos_variables_bool(predicado):
    '''
    Devuelve `True` si `predicado` es una expresión de la forma
    `variable1 + variable2 <= 1`, donde `variable1` y `variable2` son variables
    booleanas de un `CpModel`.
    '''
    return isinstance(predicado, cp_model.BoundedLinearExpression) \
        and len(predicado.vars) == 2 \
        and predicado.coeffs == [1, 1] \
        and predicado.offset == 0 \
        and predicado.bounds.max() == 1
