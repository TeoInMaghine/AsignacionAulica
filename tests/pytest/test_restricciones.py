from ortools.sat.python import cp_model
import pandas as pd

from asignacion_aulica.backend import restricciones

def make_aulas(*data):
    '''
    Recibe una lista de diccionarios con datos (posiblemente incompletos) de
    aulas.

    Rellena esos datos con valores por defecto y los devuelve en un DataFrame.
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

def make_clases(n_aulas, *data):
    '''
    Recibe el número de aulas y una lista de diccionarios con datos
    (posiblemente incompletos) de clases.

    Rellena esos datos con valores por defecto y los devuelve en un DataFrame.
    También devuelve el modelo que se usó para generar las variables.
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

    modelo = cp_model.CpModel()
    clases = pd.DataFrame.from_records(default_values | explicit_values for explicit_values in data)
    clases['aula_asignada'] = [modelo.new_int_var(0, n_aulas-1, f'aula_clase_{i}') for i in clases.index]

    return clases

def test_superposición():
    aulas = make_aulas({})
    clases = make_clases(
        1,
        {'horario_inicio': 1, 'horario_fin': 3},
        {'horario_inicio': 2, 'horario_fin': 4},
        {'horario_inicio': 5, 'horario_fin': 6}
    )

    predicados = list(restricciones.no_superponer_clases(clases, aulas))

    # Debería generar solamente un predicado entre las primeras dos clases
    assert len(predicados) == 1
    assert clases.loc[0, 'aula_asignada'] in predicados[0].vars
    assert clases.loc[1, 'aula_asignada'] in predicados[0].vars