from ortools.sat.python import cp_model
import pandas as pd

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
        'horario_apertura': 0,
        'horario_cierre': 24
    }

    return pd.DataFrame.from_records(default_values | explicit_values for explicit_values in data)

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

    clases = pd.DataFrame.from_records(default_values | explicit_values for explicit_values in data)

    return clases

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
