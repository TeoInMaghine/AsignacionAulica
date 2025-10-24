from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.lógica_de_asignación.preprocesamiento import AulasPreprocesadas, ClasesPreprocesadasPorDía
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día
from asignacion_aulica.lógica_de_asignación import preferencias

from mocks import MockAula, MockCarrera, MockClase, MockEdificio, MockMateria

@pytest.mark.aulas(MockAula(), MockAula(), MockAula())
@pytest.mark.carreras(MockCarrera(
    edificio_preferido=0,
    materias=(
        MockMateria(
            clases=(
                MockClase(día=Día.Lunes),
                MockClase(día=Día.Lunes)
            )
        ),
    )
))
@pytest.mark.asignaciones_forzadas({ 0: 1, 1: 2 })
def test_todas_las_aulas_en_el_edificio_preferido(
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía,
    modelo: cp_model.CpModel,
    asignaciones: np.ndarray
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    print(clases_lunes.rangos_de_aulas_preferidas)
    clases_fuera_del_edificio_preferido, cota_superior = preferencias.cantidad_de_clases_fuera_del_edificio_preferido(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
    assert cota_superior == 2

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(clases_fuera_del_edificio_preferido) == 0

@pytest.mark.edificios(
    MockEdificio(
        nombre='preferido',
        aulas=(
            MockAula(nombre='0'),
            MockAula(nombre='1'),
        )
    ),
    MockEdificio(
        nombre='no preferido',
        aulas=(
            MockAula(nombre='2'),
        )
    ),
    MockEdificio(
        nombre='otro preferido',
        aulas=(
            MockAula(nombre='3'),
        )
    )
)
@pytest.mark.carreras(
    MockCarrera(
        edificio_preferido=0,
        materias=(
            MockMateria(
                clases=(
                    MockClase(día=Día.Lunes),
                    MockClase(día=Día.Lunes),
                    MockClase(día=Día.Lunes)
                )
            ),
        )
    ),
    MockCarrera(
        edificio_preferido=2,
        materias=(
            MockMateria(
                clases=(
                    MockClase(día=Día.Lunes),
                    MockClase(día=Día.Lunes)
                )
            ),
        )
    ),
    MockCarrera(
        edificio_preferido=None,
        materias=(
            MockMateria(
                clases=(MockClase(día=Día.Lunes),)
            ),
        )
    )
)
@pytest.mark.asignaciones_forzadas({ 0: 2, 1: 1, 2: 2, 3: 2, 4: 0, 5: 0 })
def test_algunas_aulas_en_el_edificio_preferido(
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía,
    modelo: cp_model.CpModel,
    asignaciones: np.ndarray
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    clases_fuera_del_edificio_preferido, cota_superior = preferencias.cantidad_de_clases_fuera_del_edificio_preferido(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
    # La clase que no tiene edificio preferido no puede estar fuera de su
    # edificio preferido, y la cota máxima refleja este hecho
    assert cota_superior == len(clases_lunes.clases) - 1

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(clases_fuera_del_edificio_preferido) == 4

@pytest.mark.edificios(
    MockEdificio(nombre='0 no preferido', aulas=(MockAula(),)),
    MockEdificio(nombre='1 no preferido', aulas=(MockAula(),)),
    MockEdificio(nombre='2 preferido',    aulas=(MockAula(),)),
    MockEdificio(nombre='3 no preferido', aulas=(MockAula(),)),
    MockEdificio(nombre='4 no preferido', aulas=(MockAula(),))
)
@pytest.mark.carreras(MockCarrera(
    edificio_preferido=2,
    materias=(MockMateria(clases=(MockClase(),)),)
))
def test_elije_aula_en_edificio_preferido(
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía,
    modelo: cp_model.CpModel,
    asignaciones: np.ndarray
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    clases_fuera_del_edificio_preferido, cota_superior = preferencias.cantidad_de_clases_fuera_del_edificio_preferido(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
    assert cota_superior == 1

    # Pedir al modelo minimizar cantidad de clases fuera del edificio preferido 
    modelo.minimize((1 / cota_superior) * clases_fuera_del_edificio_preferido)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    # La clase se debe asignar al aula en el edificio preferido
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 2] == 1
    assert solver.value(clases_fuera_del_edificio_preferido) == 0
