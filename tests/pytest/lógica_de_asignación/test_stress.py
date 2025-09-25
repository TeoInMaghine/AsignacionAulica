from datetime import time
import pytest, random, logging

from conftest import make_aulas, make_carreras, make_clases, make_edificios, make_materias

from asignacion_aulica.gestor_de_datos.entidades import Edificio, Aula, Carrera, Clase, Materia
from asignacion_aulica.lógica_de_asignación.excepciones import AsignaciónImposibleException
from asignacion_aulica.lógica_de_asignación.asignación import asignar
from asignacion_aulica.gestor_de_datos.día import Día

logger = logging.getLogger()

@pytest.fixture
def aulas_generadas(
    n_aulas: int,
    n_edificios: int,
    capacidad_max: int
) -> tuple[list[Edificio], list[Aula]]:
    '''
    Genera aulas *proceduralmente*.

    Las capacidades de las aulas se generan pseudo-aleatoriamente, pero con una
    semilla fija para que sea reproducible.

    :param n_aulas: Cantidad de aulas a generar.
    :param n_edificios: Cantidad total de edificios.
    :param capacidad_max: Capacidad máxima exclusiva para un aula.

    :return: Las listas de edificios y aulas esperadas por lógica_de_asignación.
    '''
    # Dar semilla para que siempre sean los mismos números
    random.seed(0)
    edificios_params = tuple(
        dict(nombre=str(i)) for i in range(n_edificios)
    )
    aulas_params = tuple(
        dict(
            capacidad=random.randrange(1, capacidad_max),
            # Garantiza que haya al menos un aula por edificio (si aulas_count >= edificios_count)
            edificio=str(i % n_edificios)
        )
        for i in range(n_aulas)
    )

    return make_edificios(edificios_params), make_aulas(aulas_params)

@pytest.fixture
def clases_generadas(
    clases_por_hora: int,
    cantidad_de_alumnos_max: int,
    n_edificios: int
) -> tuple[list[Carrera], list[Materia], list[Clase]]:
    '''
    Genera clases *proceduralmente*.

    Las cantidades de alumnos y los edificios preferidos de las clases se
    generan pseudo-aleatoriamente, pero con una semilla fija para que sea
    reproducible.

    :param clases_por_hora: Cantidad de clases a generar por cada hora de la
    semana. Debe ser menor o igual a la cantidad de aulas generadas para que la
    asignación sea posible.
    :param cantidad_de_alumnos_max: Cantidad máxima exclusiva de alumnos.
    :param n_edificios: Cantidad total de edificios.

    :return: Las listas de carreras, materias, y clases esperadas por
    lógica_de_asignación.
    '''
    # Dar semilla para que siempre sean los mismo números
    random.seed(1)

    # Crear una carrera que prefiere cada edificio
    carreras = make_carreras(tuple(
        dict(nombre=str(i), edificio_preferido=str(i))
        for i in range(n_edificios)
    ))

    # Cada carrera tiene que tener una materia
    materias = make_materias(tuple(
        dict(carrera=carrera.nombre, nombre='m')
        for carrera in carreras
    ))

    # Crear clases con algunos parámetros aleatorios
    clases_params = []

    for día in Día:
        for hora in range(0, 23):
            horario_inicio = time(hora)
            horario_fin = time(hora + 1)
            for _ in range(clases_por_hora):
                clases_params.append(dict(
                    día=día,
                    horario_inicio=horario_inicio,
                    horario_fin=horario_fin,
                    cantidad_de_alumnos=random.randrange(1, cantidad_de_alumnos_max),
                    carrera=random.choice(carreras).nombre,
                    materia='m'
                ))
    clases = make_clases(clases_params)
    logger.info(f'Cantidad de clases: {len(clases)}.')

    return carreras, materias, clases

# NOTE: Esta forma de parametrizar no está muy claramente documentada, la
# encontré de casualidad en StackOverflow, pero la fuente primaria sería esta:
# https://docs.pytest.org/en/stable/how-to/fixtures.html#override-a-fixture-with-direct-test-parametrization

@pytest.mark.stress_test
@pytest.mark.parametrize(
    "n_edificios,capacidad_max,n_aulas,clases_por_hora,cantidad_de_alumnos_max",
   [(         10,          100,     10,             10,                    100),
    (         10,          100,     20,             20,                    100),
    (         10,          100,     30,             30,                    100)]
)
def test_stress_asignación_posible(aulas_generadas, clases_generadas):
    asignar(*aulas_generadas, *clases_generadas)

@pytest.mark.stress_test
@pytest.mark.parametrize(
    "n_edificios,capacidad_max,n_aulas,clases_por_hora,cantidad_de_alumnos_max",
   [(         10,          100,     30,             31,                    100)]
)
def test_stress_asignación_imposible(aulas_generadas, clases_generadas):
    with pytest.raises(AsignaciónImposibleException):
        asignar(*aulas_generadas, *clases_generadas)

