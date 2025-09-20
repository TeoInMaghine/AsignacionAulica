'''
Los fixtures que se definen acá están disponibles en todos los casos de prueba.

Para usar un fixture, hay que ponerlo como argumento en la función del caso de
prueba que lo necesita.

Ver https://docs.pytest.org/en/stable/how-to/fixtures.html
'''
from collections.abc import Sequence
from pandas import DataFrame
from typing import Any
import numpy as np
import pytest

from ortools.sat.python.cp_model import CpModel
from datetime import time

from asignacion_aulica.gestor_de_datos.entidades import Edificio, Aula, Carrera, Materia, Clase
from asignacion_aulica.gestor_de_datos.día import Día

from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulaPreprocesada,
    ClasePreprocesada,
    calcular_rango_de_aulas_por_edificio,
    preprocesar_aulas,
    preprocesar_clases
)

def pytest_configure(config):
    # Registrar los markers usados por las fixtures
    config.addinivalue_line("markers", "edificios: marca para pasar parametros al fixture edificios")
    config.addinivalue_line("markers", "aulas: marca para pasar parametros al fixture aulas")
    config.addinivalue_line("markers", "carreras: marca para pasar parametros al fixture carreras")
    config.addinivalue_line("markers", "materias: marca para pasar parametros al fixture materias")
    config.addinivalue_line("markers", "clases: marca para pasar parametros al fixture clases")
    config.addinivalue_line("markers", "asignaciones_forzadas: marca para pasar parametros al fixture asignaciones")

def make_edificios(edificios: tuple[dict[str, Any], ...]) -> list[Edificio]:
    '''
    Recibe datos de los edificios (posiblemente incompletos) y los rellena con
    valores por defecto.

    :param edificios: Tupla de diccionarios con datos de edificios.
    :return: La secuencia de edificios esperada por lógica_de_asignación.
    '''
    # Tiene que haber al menos un edificio
    if len(edificios) == 0:
        edificios = ({},)

    horario_default = (time(0), time(23, 59))
    _edificios = [
        Edificio(
            edificio.get('nombre', f'edificio {i}'),
            edificio.get('horario_lunes', horario_default),
            edificio.get('horario_martes', horario_default),
            edificio.get('horario_miércoles', horario_default),
            edificio.get('horario_jueves', horario_default),
            edificio.get('horario_viernes', horario_default),
            edificio.get('horario_sábado', horario_default),
            edificio.get('horario_domingo', horario_default),
            edificio.get('aulas_dobles', dict()),
            edificio.get('preferir_no_usar', False)
        )
        for i, edificio in enumerate(edificios)
    ]
    _edificios.sort(key=lambda e: e.nombre)
    return _edificios

def make_aulas(aulas: tuple[dict[str, Any], ...]) -> list[Aula]:
    '''
    Recibe datos de las aulas (posiblemente incompletos) y los rellena con
    valores por defecto.

    :param aulas: Tupla de diccionarios con datos de aulas.
    :return: La secuencia de aulas esperada por lógica_de_asignación.
    '''
    _aulas = [
        Aula(
            aula.get('nombre', f'aula {i}'),
            aula.get('edificio', 'edificio 0'),
            aula.get('capacidad', 1),
            aula.get('equipamiento', set()),
            aula.get('horario_lunes', None),
            aula.get('horario_martes', None),
            aula.get('horario_miércoles', None),
            aula.get('horario_jueves', None),
            aula.get('horario_viernes', None),
            aula.get('horario_sábado', None),
            aula.get('horario_domingo', None)
        )
        for i, aula in enumerate(aulas)
    ]
    _aulas.sort(key=lambda a: a.nombre)
    _aulas.sort(key=lambda a: a.edificio)
    return _aulas

def make_carreras(carreras: tuple[dict[str, Any], ...]) -> list[Carrera]:
    '''
    Recibe datos de las carreras (posiblemente incompletos) y los rellena con
    valores por defecto.

    :param aulas: Tupla de diccionarios con datos de carreras.
    :return: La secuencia de carreras esperada por lógica_de_asignación.
    '''
    # Tiene que haber al menos una carrera
    if len(carreras) == 0:
        carreras = ({},)

    _carreras = [
        Carrera(
            carrera.get('nombre', f'carrera {i}'),
            carrera.get('edificio_preferido', None)
        )
        for i, carrera in enumerate(carreras)
    ]
    _carreras.sort(key=lambda c: c.nombre)
    return _carreras

def make_materias(materias: tuple[dict[str, Any], ...]) -> list[Materia]:
    '''
    Recibe datos de las materias (posiblemente incompletos) y los rellena con
    valores por defecto.

    :param aulas: Tupla de diccionarios con datos de materias.
    :return: La secuencia de materias esperada por lógica_de_asignación.
    '''
    # Tiene que haber al menos una materia
    if len(materias) == 0:
        materias = ({},)

    _materias = [
        Materia(
            materia.get('nombre', f'materia {i}'),
            materia.get('carrera', 'carrera 0'),
            materia.get('año', 1),
            materia.get('cuatrimestral_o_anual', None)
        )
        for i, materia in enumerate(materias)
    ]
    _materias.sort(key=lambda c: c.nombre)
    _materias.sort(key=lambda c: c.carrera)
    return _materias

def make_clases(clases: tuple[dict[str, Any], ...]) -> list[Clase]:
    '''
    Recibe datos de las clases (posiblemente incompletos) y los rellena con
    valores por defecto.

    :param clases: Tupla de diccionarios con datos de clases.
    :return: La secuencia de clases esperada por lógica_de_asignación.
    '''
    _clases = [
        Clase(
            clase.get('id', i),
            clase.get('materia', 'materia 0'),
            clase.get('carrera', 'carrera 0'),
            clase.get('día', Día.Lunes),
            clase.get('horario_inicio', time(10)),
            clase.get('horario_fin', time(11)),
            clase.get('virtual', False),
            clase.get('cantidad_de_alumnos', 1),
            clase.get('equipamiento_necesario', set()),
            clase.get('no_cambiar_asignación', False),
            clase.get('edificio', None),
            clase.get('aula', None),
            clase.get('comisión', None),
            clase.get('teórica_o_práctica', None),
            clase.get('promocionable', None),
            clase.get('docente', None),
            clase.get('auxiliar', None)
        )
        for i, clase in enumerate(clases)
    ]
    _clases.sort(key=lambda c: c.materia)
    _clases.sort(key=lambda c: c.carrera)
    return _clases

def make_asignaciones(
        n_clases: int,
        n_aulas: int,
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

    :param asignaciones_forzadas: Diccionario de índices de clases a índices de
    aulas.
    :return: Matriz con los datos de asignaciones.
    '''
    asignaciones = np.empty(shape=(n_clases, n_aulas), dtype=object)
    
    for clase, aula in np.ndindex(asignaciones.shape):
        if clase not in asignaciones_forzadas or asignaciones_forzadas[clase] == aula:
            asignaciones[clase, aula] = modelo.new_bool_var(f'clase_{clase}_asignada_al_aula_{aula}')
        else:
            asignaciones[clase, aula] = 0
    
    # Asegurar que cada clase se asigna a exactamente un aula
    for clase in range(asignaciones.shape[0]):
        modelo.add_exactly_one(asignaciones[clase,:])
    
    return asignaciones

@pytest.fixture
def edificios(request: pytest.FixtureRequest) -> Sequence[Edificio]:
    '''
    Recibe en el marker "edificios" una tupla de diccionarios con datos
    (posiblemente incompletos) de edificios.

    Rellena esos datos con valores por defecto.

    :return: La secuencia de edificios esperada por lógica_de_asignación.
    '''
    marker = request.node.get_closest_marker('edificios')
    data = marker.args if marker else ()
    return make_edificios(data)

@pytest.fixture
def aulas(request) -> Sequence[Aula]:
    '''
    Recibe en el marker "aulas" una tupla de diccionarios con datos
    (posiblemente incompletos) de aulas.

    Rellena esos datos con valores por defecto.

    :return: La secuencia de aulas esperada por lógica_de_asignación.
    '''
    marker = request.node.get_closest_marker('aulas')
    data = marker.args if marker else ()
    return make_aulas(data)

@pytest.fixture
def rangos_de_aulas(edificios, aulas) -> dict[str, tuple[int, int]]:
    return calcular_rango_de_aulas_por_edificio(edificios, aulas)

@pytest.fixture
def aulas_preprocesadas(edificios, aulas, rangos_de_aulas) -> Sequence[AulaPreprocesada]:
    return preprocesar_aulas(edificios, aulas, rangos_de_aulas)

@pytest.fixture
def carreras(request) -> Sequence[Carrera]:
    '''
    Recibe en el marker "carreras" una tupla de diccionarios con datos
    (posiblemente incompletos) de carreras.

    Rellena esos datos con valores por defecto.

    :return: La secuencia de carreras esperada por lógica_de_asignación.
    '''
    marker = request.node.get_closest_marker('carreras')
    data = marker.args if marker else ()
    return make_carreras(data)

@pytest.fixture
def materias(request) -> Sequence[Materia]:
    '''
    Recibe en el marker "materias" una tupla de diccionarios con datos
    (posiblemente incompletos) de materias.

    Rellena esos datos con valores por defecto.

    :return: La secuencia de materias esperada por lógica_de_asignación.
    '''
    marker = request.node.get_closest_marker('materias')
    data = marker.args if marker else ()
    return make_materias(data)

@pytest.fixture
def clases(request) -> Sequence[Clase]:
    '''
    Recibe en el marker "clases" una tupla de diccionarios con datos
    (posiblemente incompletos) de clases.

    Rellena esos datos con valores por defecto.
    
    :return: La secuencia de clases esperada por lógica_de_asignación.
    '''
    marker = request.node.get_closest_marker('clases')
    data = marker.args if marker else ()
    return make_clases(data)

@pytest.fixture
def clases_preprocesadas(clases, materias, carreras) -> tuple[
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ]
]:
    '''
    :return: El resultado de preprocesar las clases/materias/carreras obtenidas
    de los correspondientes fixtures.
    '''
    return preprocesar_clases(clases, materias, carreras)

@pytest.fixture
def modelo() -> CpModel:
    ':return: Un CpModel para este caso de prueba.'
    return CpModel()

@pytest.fixture
def asignaciones(
        request,
        clases: Sequence[Clase],
        aulas: Sequence[Aula],
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

    return make_asignaciones(len(clases), len(aulas), modelo, asignaciones_forzadas)
