from ortools.sat.python import cp_model
from collections.abc import Sequence
import pytest

from conftest import clases_preprocesadas, make_aulas, make_clases, make_asignaciones

from asignacion_aulica.gestor_de_datos.entidades import Aula, Clase
from asignacion_aulica.lógica_de_asignación import preferencias
from asignacion_aulica.gestor_de_datos.día import Día

from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulaPreprocesada, ClasePreprocesada, calcular_rango_de_aulas_por_edificio,
    preprocesar_aulas, preprocesar_clases
)

@pytest.mark.edificios(
    dict(nombre='no preferido', preferir_no_usar=True),
    dict(nombre='preferido', preferir_no_usar=False)
)
@pytest.mark.carreras(dict(nombre='c', edificio_preferido='preferido'))
@pytest.mark.materias(dict(nombre='m', carrera='c'))
@pytest.mark.parametrize(
    ('aulas_params', 'clases_params', 'asignaciones_forzadas', 'cota_esperada', 'cantidad_esperada'),
    [
        # Ningún edificio indeseable
        (
            (dict(edificio='preferido'), dict(edificio='preferido')),
            ({}, {}),
            {},
            1,
            0
        ),

        # Un edificio indeseable
        (
            (dict(edificio='no preferido'), dict(edificio='preferido'), dict(edificio='preferido')),
            (dict(cantidad_de_alumnos=10), dict(cantidad_de_alumnos=23)),
            {},
            10+23,
            0
        ),

        # Un edificio indeseable, con asignación forzada
        (
            (dict(edificio='no preferido'), dict(edificio='preferido'), dict(edificio='preferido')),
            (dict(cantidad_de_alumnos=10), dict(cantidad_de_alumnos=23)),
            {1: 0},
            10+23,
            23
        ),

        # Todos los edificios indeseables
        (
            (dict(edificio='no preferido'), dict(edificio='no preferido'), dict(edificio='no preferido')),
            (dict(cantidad_de_alumnos=15), dict(cantidad_de_alumnos=23)),
            {},
            15+23,
            15+23
        ),
        
        # Algunos edificios indeseables y otros no
        (
            (dict(edificio='no preferido'), dict(edificio='no preferido'), dict(edificio='preferido'), dict(edificio='preferido')),
            (dict(cantidad_de_alumnos=15), dict(cantidad_de_alumnos=23), dict(cantidad_de_alumnos=2)),
            {},
            15+23+2,
            0
        ),
        
        # Algunos edificios indeseables y otros no, con asignaciones forzadas
        (
            (dict(edificio='no preferido'), dict(edificio='no preferido'), dict(edificio='preferido'), dict(edificio='preferido')),
            (dict(cantidad_de_alumnos=15), dict(cantidad_de_alumnos=23), dict(cantidad_de_alumnos=2)),
            {0:2, 2:1},
            23+2,
            2
        ),
    ]
)
def test_cantidad_de_alumnos_en_aulas_indeseables_y_su_cota_superior(
    aulas_params, clases_params, asignaciones_forzadas, cota_esperada,
    cantidad_esperada, carreras, materias, edificios, modelo
):
    aulas: list[Aula] = make_aulas(aulas_params)
    rangos_de_aulas = calcular_rango_de_aulas_por_edificio(edificios, aulas)
    aulas_preprocesadas: Sequence[AulaPreprocesada] = preprocesar_aulas(edificios, aulas, rangos_de_aulas)

    clases: list[Clase] = make_clases(tuple(clase|dict(carrera='c', materia='m', día=Día.Lunes) for clase in clases_params))
    clases_preprocesadas = preprocesar_clases(clases, materias, carreras)
    clases_lunes: list[ClasePreprocesada] = clases_preprocesadas[Día.Lunes][0]

    asignaciones = make_asignaciones(len(clases), len(aulas), modelo, asignaciones_forzadas)

    alumnos_en_edificios_indeseables, cota = preferencias.cantidad_de_alumnos_en_edificios_no_deseables(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    assert cota == cota_esperada

    modelo.minimize(alumnos_en_edificios_indeseables)
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(alumnos_en_edificios_indeseables) == cantidad_esperada
