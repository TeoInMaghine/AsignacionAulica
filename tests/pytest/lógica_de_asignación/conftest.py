'''
Los fixtures que se definen acá están disponibles en todos los casos de prueba.

Para usar un fixture, hay que ponerlo como argumento en la función del caso de
prueba que lo necesita.

Ver https://docs.pytest.org/en/stable/how-to/fixtures.html
'''
import pytest

from ortools.sat.python.cp_model import CpModel
from pandas import DataFrame
import numpy as np

from asignacion_aulica.gestor_de_datos import Día

def pytest_configure(config):
    # Registrar los markers usados por las fixtures
    config.addinivalue_line("markers", "aulas: marca para pasar parametros al fixture aulas")
    config.addinivalue_line("markers", "clases: marca para pasar parametros al fixture clases")
    config.addinivalue_line("markers", "asignaciones_forzadas: marca para pasar parametros al fixture asignaciones")

def make_aulas(aulas) -> DataFrame:
    '''
    Recibe datos de las aulas (posiblemente incompletos) y los rellena con valores por defecto.

    :param aulas: Tupla de diccionarios con datos (posiblemente incompletos) de aulas.
    :return: Un DataFrame con el formato esperado por lógica_de_asignación.
    '''
    default_values = {
        'edificio': 'edificio',
        'nombre': 'aula',
        'capacidad': 1,
        'equipamiento': set(),
        'preferir_no_usar': False,
        'horarios': {
            Día.LUNES:     (0, 24),
            Día.MARTES:    (0, 24),
            Día.MIÉRCOLES: (0, 24),
            Día.JUEVES:    (0, 24),
            Día.VIERNES:   (0, 24),
            Día.SÁBADO:    (0, 24),
            Día.DOMINGO:   (0, 24)
        }
    }

    return DataFrame.from_records(default_values | explicit_values for explicit_values in aulas)

def make_clases(clases) -> DataFrame:
    '''
    Recibe datos de las clases (posiblemente incompletos) y los rellena con valores por defecto.

    :param clases: Tupla de diccionarios con datos (posiblemente incompletos) de clases.
    :return: Un DataFrame con el formato esperado por lógica_de_asignación.
    '''
    default_values = {
        'nombre': 'materia',
        'día': Día.LUNES,
        'horario_inicio': 10,
        'horario_fin': 11,
        'cantidad_de_alumnos': 1,
        'equipamiento_necesario': set(),
        'edificio_preferido': 'edificio',
        'aula_asignada': None
    }

    data = {
        columna: [clase.get(columna, default) for clase in clases]
        for columna, default in default_values.items()
    }

    return DataFrame(data, dtype=object)

def make_asignaciones(
        clases: DataFrame,
        aulas: DataFrame,
        modelo: CpModel,
        asignaciones_forzadas: dict[int, int] = {}
    ) -> np.ndarray:
    '''
    Genera una matriz con las variables de asignación. No hay constantes, todas
    son variables que se agregan al modelo, a menos que se especifiquen
    asignaciones forzadas, en cuyo caso se colocan los ceros donde corresponda
    (no unos, para simular como ocurriría en la asignación real).

    También se agregan restricciones para que cada clase se asigne exactamente a
    un aula.

    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param modelo: El modelo que usar para generar variables.
    :param asignaciones_forzadas: Diccionario de índices de clases a índices de
    aulas.
    :return: Matriz con los datos de asignaciones.
    '''
    asignaciones = np.empty(shape=(len(clases), len(aulas)), dtype=object)
    
    for clase, aula in np.ndindex(asignaciones.shape):
        if clase not in asignaciones_forzadas or asignaciones_forzadas[clase] == aula:
            asignaciones[clase, aula] = modelo.new_bool_var(f'clase_{clase}_asignada_al_aula_{aula}')
        else:
            asignaciones[clase, aula] = 0
    
    # Asegurar que cada clase se asigna a exactamente un aula
    for clase in clases.index:
        modelo.add_exactly_one(asignaciones[clase,:])
    
    return asignaciones

@pytest.fixture
def aulas(request) -> DataFrame:
    '''
    Recibe en el marker "aulas" una tupla de diccionarios con datos
    (posiblemente incompletos) de aulas.

    Rellena esos datos con valores por defecto.

    :return: Un DataFrame con el formato esperado por lógica_de_asignación.
    '''
    data = request.node.get_closest_marker('aulas').args
    return make_aulas(data)

@pytest.fixture
def clases(request) -> DataFrame:
    '''
    Recibe en el marker "clases" una tupla de diccionarios con datos
    (posiblemente incompletos) de clases.

    Rellena esos datos con valores por defecto.
    
    :return: Un DataFrame con el formato esperado por lógica_de_asignación.
    '''
    clases = request.node.get_closest_marker('clases').args
    return make_clases(clases)

@pytest.fixture
def modelo() -> CpModel:
    ':return: Un CpModel para este caso de prueba.'
    return CpModel()

@pytest.fixture
def asignaciones(
        request,
        clases: DataFrame,
        aulas: DataFrame,
        modelo: CpModel
    ) -> np.ndarray:
    '''
    Genera una matriz con las variables de asignación. No hay constantes, todas
    son variables que se agregan al modelo, a menos que se especifiquen
    asignaciones forzadas, en cuyo caso se colocan los ceros donde corresponda
    (no unos, para simular como ocurriría en la asignación real).

    También se agregan restricciones para que cada clase se asigne exactamente a
    un aula.

    Las asignaciones forzadas se definen en el marker "asignaciones_forzadas",
    que si está presente tiene que tener un diccionario que mapea índices de
    clases a índices de aulas.

    :return: Matriz con los datos de asignaciones.
    '''
    marker = request.node.get_closest_marker('asignaciones_forzadas')
    asignaciones_forzadas: dict[int, int] = marker.args[0] if marker else dict()

    return make_asignaciones(clases, aulas, modelo, asignaciones_forzadas)
