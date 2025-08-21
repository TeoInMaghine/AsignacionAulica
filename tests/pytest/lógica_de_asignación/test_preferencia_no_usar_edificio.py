from ortools.sat.python import cp_model
import pytest

from asignacion_aulica.lógica_de_asignación import preferencias

from conftest import make_aulas, make_clases, make_asignaciones

@pytest.mark.parametrize(
    ('aulas_params', 'clases_params', 'asignaciones_forzadas', 'cota_esperada', 'cantidad_esperada'),
    [
        # Ningún edificio indeseable
        (
            (dict(preferir_no_usar=False), dict(preferir_no_usar=False)),
            ({}, {}),
            {},
            1,
            0
        ),

        # Un edificio indeseable
        (
            (dict(preferir_no_usar=False), dict(preferir_no_usar=True), dict(preferir_no_usar=False)),
            (dict(cantidad_de_alumnos=10), dict(cantidad_de_alumnos=23)),
            {},
            10+23,
            0
        ),

        # Un edificio indeseable, con asignación forzada
        (
            (dict(preferir_no_usar=False), dict(preferir_no_usar=True), dict(preferir_no_usar=False)),
            (dict(cantidad_de_alumnos=10), dict(cantidad_de_alumnos=23)),
            {1: 1},
            10+23,
            23
        ),

        # Todos los edificios indeseables
        (
            (dict(preferir_no_usar=True), dict(preferir_no_usar=True), dict(preferir_no_usar=True)),
            (dict(cantidad_de_alumnos=15), dict(cantidad_de_alumnos=23)),
            {},
            15+23,
            15+23
        ),
        
        # Algunos edificios indeseables y otros no
        (
            (dict(preferir_no_usar=True), dict(preferir_no_usar=False), dict(preferir_no_usar=True), dict(preferir_no_usar=False)),
            (dict(cantidad_de_alumnos=15), dict(cantidad_de_alumnos=23), dict(cantidad_de_alumnos=2)),
            {},
            15+23+2,
            0
        ),
        
        # Algunos edificios indeseables y otros no, con asignaciones forzadas
        (
            (dict(preferir_no_usar=True), dict(preferir_no_usar=False), dict(preferir_no_usar=True), dict(preferir_no_usar=False)),
            (dict(cantidad_de_alumnos=15), dict(cantidad_de_alumnos=23), dict(cantidad_de_alumnos=2)),
            {0:1, 2:2},
            23+2,
            2
        ),
    ]
)
def test_cantidad_de_alumnos_en_aulas_indeseables_y_su_cota_superior(aulas_params, clases_params, asignaciones_forzadas, cota_esperada, cantidad_esperada, modelo):
    aulas = make_aulas(aulas_params)
    clases = make_clases(clases_params)
    asignaciones = make_asignaciones(clases, aulas, modelo, asignaciones_forzadas)

    alumnos_en_edificios_indeseables, cota = preferencias.obtener_cantidad_de_alumnos_en_edificios_no_deseables(clases, aulas, modelo, asignaciones)
    assert cota == cota_esperada

    modelo.minimize(alumnos_en_edificios_indeseables)
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(alumnos_en_edificios_indeseables) == cantidad_esperada
