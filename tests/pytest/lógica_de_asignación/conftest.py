'''
Los fixtures que se definen acá están disponibles en todos los casos de prueba
de `lógica_de_asignación`.

Para usar un fixture, hay que ponerlo como argumento en la función del caso de
prueba que lo necesita.

Ver https://docs.pytest.org/en/stable/how-to/fixtures.html
'''
from ortools.sat.python.cp_model import CpModel
import numpy as np
import pytest

from asignacion_aulica.gestor_de_datos.entidades import Edificios, Carreras
from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    ClasesPreprocesadasPorDía,
    AulasPreprocesadas,
    preprocesar_clases
)

from mocks import (
    MockEdificio,
    MockCarrera,
    MockMateria,
    make_edificios,
    make_carreras,
    make_asignaciones
)

def pytest_configure(config):
    # Registrar los markers usados por las fixtures
    config.addinivalue_line("markers", "edificios: marca para pasar parametros al fixture edificios")
    config.addinivalue_line("markers", "aulas: marca para pasar parametros al fixture aulas")
    config.addinivalue_line("markers", "carreras: marca para pasar parametros al fixture carreras")
    config.addinivalue_line("markers", "clases: marca para pasar parametros al fixture clases")
    config.addinivalue_line("markers", "asignaciones_forzadas: marca para pasar parametros al fixture asignaciones")

@pytest.fixture
def edificios(request: pytest.FixtureRequest) -> Edificios:
    '''
    Recibe datos (posiblemente incompletos) de edificios y/o aulas. Rellena esos
    datos con valores por defecto.

    Puede recibir en el marker "edificios" una tupla de `MockEdificio`s, o en el
    marker "aulas" una tupla de `MockAula`s. No se pueden usar los dos markers a
    la vez.

    :return: La secuencia de edificios esperada por lógica_de_asignación.
    '''
    marker_edificios = request.node.get_closest_marker('edificios')
    marker_aulas = request.node.get_closest_marker('aulas')
    edificios: tuple[MockEdificio, ...]

    if marker_edificios and marker_aulas:
        raise RuntimeError('No se pueden usar a la misma vez los markers "edificios" y "aulas".')
    elif marker_edificios:
        edificios = marker_edificios.args
    elif marker_aulas:
        edificios = (
            MockEdificio(
                aulas=marker_aulas.args
            ),
        )
    else:
        edificios = tuple()
    
    return make_edificios(edificios)

@pytest.fixture
def aulas_preprocesadas(edificios: Edificios) -> AulasPreprocesadas:
    return AulasPreprocesadas(edificios)

@pytest.fixture
def carreras(request, edificios: Edificios) -> Carreras:
    '''
    Recibe datos (posiblemente incompletos) de carreras/materias/clases. Rellena
    esos datos con valores por defecto.

    Puede recibir en el marker "carreras" una tupla de `Mockcarreras`s, o en el
    marker "clases" una tupla de `MockClases`s. No se pueden usar los dos
    markers a la vez.

    :return: La secuencia de carreras esperada por lógica_de_asignación.
    '''
    marker_carreras = request.node.get_closest_marker('carreras')
    marker_clases = request.node.get_closest_marker('clases')
    carreras: tuple[MockCarrera, ...]

    if marker_carreras and marker_clases:
        raise RuntimeError('No se pueden usar a la misma vez los markers "carreras" y "clases".')
    elif marker_carreras:
        carreras = marker_carreras.args
    elif marker_clases:
        carreras = (
            MockCarrera(
                materias=(
                    MockMateria(clases=marker_clases.args),
                )
            ),
        )
    else:
        carreras = tuple()
    
    return make_carreras(edificios, carreras)

@pytest.fixture
def clases_preprocesadas(
    carreras: Carreras,
    aulas_preprocesadas: AulasPreprocesadas
) -> ClasesPreprocesadasPorDía:
    '''
    :return: El resultado de preprocesar las carreras obtenidas del
    correspondiente fixture.
    '''
    return preprocesar_clases(carreras, aulas_preprocesadas)

@pytest.fixture
def modelo() -> CpModel:
    ':return: Un CpModel para este caso de prueba.'
    return CpModel()

@pytest.fixture
def asignaciones(
    request,
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía,
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

    La matriz tiene filas para todas las clases, sin separar por días, así que
    este fixture sólo es correcto cuando ``clases`` contiene clases en un único
    día.

    :return: Matriz con los datos de asignaciones.
    '''
    marker = request.node.get_closest_marker('asignaciones_forzadas')
    asignaciones_forzadas: dict[int, int] = marker.args[0] if marker else dict()
    
    n_clases = max(len(día.clases) for día in clases_preprocesadas)

    return make_asignaciones(n_clases, len(aulas_preprocesadas.aulas), modelo, asignaciones_forzadas)
