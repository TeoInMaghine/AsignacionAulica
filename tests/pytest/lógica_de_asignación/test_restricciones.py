from ortools.sat.python import cp_model
from datetime import time
import numpy as np
import pytest

from asignacion_aulica.lógica_de_asignación.preprocesamiento import AulasPreprocesadas, ClasesPreprocesadasPorDía
from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.lógica_de_asignación import restricciones

from mocks import MockAula, MockClase, MockEdificio

def predicado_es_nand_entre_dos_variables(predicado, variable1, variable2) -> bool:
    '''
    Devuelve `True` si `predicado` es una expresión de la forma
    `variable1 + variable2 <= 1`, donde `variable1` y `variable2` son variables
    booleanas de un `CpModel`.
    '''
    return (
        isinstance(predicado, cp_model.BoundedLinearExpression)
        and len(predicado.vars) == 2
        and variable1 in predicado.vars
        and variable2 in predicado.vars
        and predicado.coeffs == [1, 1]
        and predicado.offset == 0
        and predicado.bounds.max() == 1
    )

@pytest.mark.aulas(MockAula())
@pytest.mark.clases(
    MockClase(día=Día.Lunes, horario=RangoHorario(time(1), time(3))),
    MockClase(día=Día.Lunes, horario=RangoHorario(time(2), time(4))),
    MockClase(día=Día.Lunes, horario=RangoHorario(time(5), time(6)))
)
def test_superposición(
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía,
    asignaciones: np.ndarray
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    predicados = list(restricciones.no_superponer_clases(clases_lunes, aulas_preprocesadas, asignaciones))

    # Debería generar solamente un predicado entre las primeras dos clases
    assert len(predicados) == 1
    predicado = predicados[0]
    assert predicado_es_nand_entre_dos_variables(predicado, asignaciones[0,0], asignaciones[1,0])

@pytest.mark.clases(
    MockClase(horario=RangoHorario(time(10), time(13)), día=Día.Lunes)
)
@pytest.mark.aulas(
    MockAula(horario_lunes=RangoHorario(time(10), time(13))), # Igual que la clase
    MockAula(horario_lunes=RangoHorario(time(10), time(11))), # Cierra temprano
    MockAula(horario_lunes=RangoHorario(time(11), time(13))), # Abre tarde
    MockAula(horario_lunes=RangoHorario(time( 9), time(14))), # Sobra
    MockAula(horario_lunes=RangoHorario(time(11), time(12))), # Abre tarde y cierra temprano
    MockAula(horario_lunes=RangoHorario(time( 0), time( 0))), # No abre los lunes
)
def test_aulas_cerradas(
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    prohibidas = list(restricciones.no_asignar_en_aula_cerrada(clases_lunes, aulas_preprocesadas))

    # Debería generar restricciones con las aulas 1, 2, 4 y 5
    assert len(prohibidas) == 4
    assert (0, 1) in prohibidas
    assert (0, 2) in prohibidas
    assert (0, 4) in prohibidas
    assert (0, 5) in prohibidas

@pytest.mark.clases(
    MockClase(equipamiento_necesario = set(('proyector',)))
)
@pytest.mark.aulas(
    MockAula(equipamiento = set(('proyector',))),
    MockAula(equipamiento = set(('proyector', 'otra cosa'))),
    MockAula(equipamiento = set())
)
def test_equipamiento(
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    prohibidas = list(restricciones.asignar_aulas_con_el_equipamiento_requerido(clases_lunes, aulas_preprocesadas))

    # Debería generar una sola restricción con el aula 2
    assert len(prohibidas) == 1
    assert (0, 2) in prohibidas

@pytest.mark.edificios(
    MockEdificio(
        aulas=(MockAula(),)*3,
        aulas_dobles={0: (1, 2)}
    )
)
@pytest.mark.clases(
    MockClase(día=Día.Lunes),
    MockClase(día=Día.Lunes)
)
def test_aulas_dobles(
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía,
    asignaciones: np.ndarray
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    predicados = list(restricciones.no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo(clases_lunes, aulas_preprocesadas, asignaciones))
    
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[0, 0], asignaciones[1, 1]) for p in predicados)
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[0, 0], asignaciones[1, 2]) for p in predicados)
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[1, 0], asignaciones[0, 1]) for p in predicados)
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[1, 0], asignaciones[0, 2]) for p in predicados)
