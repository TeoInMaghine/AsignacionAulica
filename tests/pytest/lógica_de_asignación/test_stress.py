import pytest, random, logging

from pandas import DataFrame

from asignacion_aulica.lógica_de_asignación.dia import Día
from asignacion_aulica import lógica_de_asignación
from conftest import make_aulas, make_clases

@pytest.fixture
def aulas_generadas(
        aulas_count: int,
        capacidad_max: int,
        edificios_count: int
    ) -> DataFrame:
    '''
    Genera aulas *proceduralmente*.
    Las capacidades de las aulas se generan pseudo-aleatoriamente, pero con una
    semilla fija para que sea consistente.

    :param aulas_count: Cantidad de aulas a generar.
    :param capacidad_max: Capacidad máxima exclusiva para un aula.
    :param edificios_count: Cantidad total de edificios.
    :return: Un DataFrame con el formato esperado por lógica_de_asignación.
    '''
    # Dar semilla para que siempre sean los mismo números
    random.seed(0)
    aulas_params = []

    for i in range(aulas_count):
        aulas_params.append({
            'capacidad': random.randrange(1, capacidad_max),
            # Garantiza que haya al menos un aula por edificio (si aulas_count >= edificios_count)
            'edificio': i % edificios_count,
        })

    return make_aulas(aulas_params)

@pytest.fixture
def clases_generadas(
        amount_per_hour: int,
        cantidad_de_alumnos_max: int,
        edificios_count: int
    ) -> DataFrame:
    '''
    Genera clases *proceduralmente*.
    Las cantidades de alumnos y los edificios preferidos de las clases se
    generan pseudo-aleatoriamente, pero con una semilla fija para que sea
    consistente.

    :param amount_per_hour: Cantidad de clases a generar por cada hora de la semana.
        Debe ser menor o igual a la cantidad de aulas generadas para que la
        asignación sea posible.
    :param cantidad_de_alumnos_max: Cantidad máxima exclusiva de alumnos.
    :param edificios_count: Cantidad total de edificios.
    :return: Un DataFrame con el formato esperado por lógica_de_asignación.
    '''
    # Dar semilla para que siempre sean los mismo números
    random.seed(1)
    clases_params = []

    for día in Día:
        for hora in range(0, 24):
            horario_inicio = hora
            horario_fin = hora + 1
            for i in range(amount_per_hour):
                clases_params.append({
                    'día': día,
                    'horario_inicio': horario_inicio,
                    'horario_fin': horario_fin,
                    'cantidad_de_alumnos': random.randrange(1, cantidad_de_alumnos_max),
                    'edificio_preferido': random.randrange(edificios_count),
                })

    logging.info(f'Cantidad de clases: {len(clases_params)}.')

    return make_clases(clases_params)

# NOTE: Esta forma de parametrizar no está muy claramente documentada, la
# encontré de casualidad en StackOverflow, pero la fuente primaria sería esta:
# https://docs.pytest.org/en/stable/how-to/fixtures.html#override-a-fixture-with-direct-test-parametrization

@pytest.mark.stress_test
@pytest.mark.parametrize(
    "edificios_count,capacidad_max,aulas_count,amount_per_hour,cantidad_de_alumnos_max",
   [(             10,          100,         10,             10,                    100),
    (             10,          100,         20,             20,                    100),
    (             10,          100,         30,             30,                    100)]
)
def test_stress_asignación_posible(aulas_generadas, clases_generadas):
    lógica_de_asignación.asignar(clases_generadas, aulas_generadas)

@pytest.mark.stress_test
@pytest.mark.parametrize(
    "edificios_count,capacidad_max,aulas_count,amount_per_hour,cantidad_de_alumnos_max",
   [(             10,          100,         30,             31,                    100)]
)
def test_stress_asignación_imposible(aulas_generadas, clases_generadas):
    with pytest.raises(lógica_de_asignación.AsignaciónImposibleException):
        lógica_de_asignación.asignar(clases_generadas, aulas_generadas)

