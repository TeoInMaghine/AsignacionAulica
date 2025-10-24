from datetime import time
import pytest, random, logging

from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.entidades import Carreras, Edificios
from asignacion_aulica.lógica_de_asignación.asignación import asignar

from mocks import MockAula, MockClase, MockEdificio, MockCarrera, MockMateria, make_carreras, make_edificios

logger = logging.getLogger()

@pytest.fixture
def edificios_generados(
    n_aulas: int,
    n_edificios: int,
    capacidad_max: int
) -> Edificios:
    '''
    Genera aulas *proceduralmente*.

    Las capacidades de las aulas se generan pseudo-aleatoriamente, pero con una
    semilla fija para que sea reproducible.

    :param n_aulas: Cantidad de aulas a generar.
    :param n_edificios: Cantidad total de edificios.
    :param capacidad_max: Capacidad máxima exclusiva para un aula.

    :return: La lista de edificios esperada por lógica_de_asignación.
    '''
    # Dar semilla para que siempre sean los mismos números
    random.seed(0)

    edificios = [MockEdificio(nombre=str(i), aulas=list()) for i in range(n_edificios)]

    for i in range(n_aulas):
        aula = MockAula(capacidad=random.randrange(1, capacidad_max))

        # Garantiza que haya al menos un aula por edificio (si aulas_count >= edificios_count)
        i_edificio=i % n_edificios
        edificios[i_edificio].aulas.append(aula)

    return make_edificios(edificios)

@pytest.fixture
def carreras_generadas(
    clases_por_hora: int,
    cantidad_de_alumnos_max: int,
    edificios_generados: Edificios
) -> Carreras:
    '''
    Genera clases *proceduralmente*.

    Las cantidades de alumnos y los edificios preferidos de las clases se
    generan pseudo-aleatoriamente, pero con una semilla fija para que sea
    reproducible.

    :param clases_por_hora: Cantidad de clases a generar por cada hora de la
    semana. Debe ser menor o igual a la cantidad de aulas generadas para que la
    asignación sea posible.
    :param cantidad_de_alumnos_max: Cantidad máxima exclusiva de alumnos.
    :param edificios_generados: Los edificios generados por el fixture correspondiente.

    :return: La lista de carreras esperada por lógica_de_asignación.
    '''
    # Dar semilla para que siempre sean los mismos números
    random.seed(1)

    # Crear una carrera que prefiere cada edificio,
    # y crear clases con algunos parámetros aleatorios
    carreras = [
        MockCarrera(
            edificio_preferido=i,
            materias=(MockMateria(clases=list()),) # Una sola materia por carrera.
        )
        for i in range(len(edificios_generados))
    ]

    # Crear clases con algunos parámetros aleatorios
    for día in Día:
        for hora in range(0, 23):
            horario = RangoHorario(time(hora), time(hora+1))
            for _ in range(clases_por_hora):
                carrera=random.choice(carreras)
                carrera.materias[0].clases.append(MockClase(
                    día=día,
                    horario=horario,
                    cantidad_de_alumnos=random.randrange(1, cantidad_de_alumnos_max),
                ))

    logger.debug('Se crearon un total de %d clases.', sum(len(materia.clases) for carrera in carreras for materia in carrera.materias))
    return make_carreras(edificios_generados, carreras)

# NOTE: Esta forma de parametrizar no está muy claramente documentada, la
# encontré de casualidad en StackOverflow, pero la fuente primaria sería esta:
# https://docs.pytest.org/en/stable/how-to/fixtures.html#override-a-fixture-with-direct-test-parametrization

@pytest.mark.stress_test
@pytest.mark.parametrize(
    argnames="n_edificios,capacidad_max,n_aulas,clases_por_hora,cantidad_de_alumnos_max",
    argvalues=[(       10,          100,     10,             10,                    100),
               (       10,          100,     20,             20,                    100),
               (       10,          100,     30,             30,                    100)]
)
def test_stress_asignación_posible(edificios_generados: Edificios, carreras_generadas: Carreras):
    resultado = asignar(edificios_generados, carreras_generadas)
    assert resultado.todo_ok()

@pytest.mark.stress_test
@pytest.mark.parametrize(
    argnames="n_edificios,capacidad_max,n_aulas,clases_por_hora,cantidad_de_alumnos_max",
    argvalues=[(       10,          100,     30,             31,                    100)]
)
def test_stress_asignación_imposible(edificios_generados: Edificios, carreras_generadas: Carreras):
    resultado = asignar(edificios_generados, carreras_generadas)
    assert not resultado.todo_ok()

