from ortools.sat.python import cp_model
from collections.abc import Sequence
import pytest

from asignacion_aulica.gestor_de_datos.entidades import Carreras, Edificios
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día
from asignacion_aulica.lógica_de_asignación import preferencias

from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulasPreprocesadas, ClasesPreprocesadas, preprocesar_clases
)

from mocks import (
    MockAula, MockCarrera, MockClase, MockEdificio, MockMateria,
    make_edificios, make_carreras, make_asignaciones
)

@pytest.mark.parametrize(
    argnames=(
        'n_aulas_no_preferidas', 'n_aulas_preferidas',
        'clases',
        'asignaciones_forzadas', 'cota_esperada', 'cantidad_esperada'
        # Los argvalues tienen este mismo layout.
    ),
    argvalues=[
        # Ningún aula en edificio indeseable
        (
            0, 2,
            (MockClase(), MockClase()),
            {}, 1, 0
        ),

        # Un aula en edificio indeseable
        (
            1, 2,
            (MockClase(cantidad_de_alumnos=10), MockClase(cantidad_de_alumnos=23)),
            {}, 10+23, 0
        ),

        # Un edificio indeseable, con asignación forzada
        (
            1, 2,
            (MockClase(cantidad_de_alumnos=10), MockClase(cantidad_de_alumnos=23)),
            {1: 0}, 10+23, 23
        ),

        # Todos los edificios indeseables
        (
            3, 0,
            (MockClase(cantidad_de_alumnos=15), MockClase(cantidad_de_alumnos=23)),
            {}, 15+23, 15+23
        ),
        
        # Algunos edificios indeseables y otros no
        (
            2, 2,
            (MockClase(cantidad_de_alumnos=15), MockClase(cantidad_de_alumnos=23), MockClase(cantidad_de_alumnos=2)),
            {}, 15+23+2, 0
        ),
        
        # Algunos edificios indeseables y otros no, con asignaciones forzadas
        (
            2, 2,
            (MockClase(cantidad_de_alumnos=15), MockClase(cantidad_de_alumnos=23), MockClase(cantidad_de_alumnos=2)),
            {0:2, 2:1}, 23+2, 2
        )
    ]
)
def test_cantidad_de_alumnos_en_aulas_indeseables_y_su_cota_superior(
    n_aulas_no_preferidas: int,
    n_aulas_preferidas: int,
    clases: Sequence[MockClase],
    asignaciones_forzadas: dict[int, int],
    cota_esperada: int,
    cantidad_esperada: int,
    modelo: cp_model.CpModel
):
    edificios: Edificios = make_edificios((
        MockEdificio(nombre='no preferido', preferir_no_usar=True, aulas=(MockAula(),)*n_aulas_no_preferidas),
        MockEdificio(nombre='preferido',   preferir_no_usar=False, aulas=(MockAula(),)*n_aulas_preferidas)
    ))
    aulas_preprocesadas = AulasPreprocesadas(edificios)

    carreras: Carreras = make_carreras(
        edificios,
        carreras=(
            MockCarrera(materias=(MockMateria(clases=clases),)),
        )
    )
    clases_preprocesadas = preprocesar_clases(carreras, aulas_preprocesadas)
    clases_lunes: ClasesPreprocesadas = clases_preprocesadas[Día.Lunes]

    asignaciones = make_asignaciones(len(clases_lunes.clases), len(aulas_preprocesadas.aulas), modelo, asignaciones_forzadas)

    alumnos_en_edificios_indeseables, cota = preferencias.cantidad_de_alumnos_en_edificios_no_deseables(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
    assert cota == cota_esperada

    modelo.minimize(alumnos_en_edificios_indeseables)
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(alumnos_en_edificios_indeseables) == cantidad_esperada
