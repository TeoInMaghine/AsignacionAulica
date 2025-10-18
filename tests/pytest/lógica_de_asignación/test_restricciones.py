from ortools.sat.python import cp_model
from datetime import time
import pytest

from asignacion_aulica.lógica_de_asignación import restricciones
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

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

@pytest.mark.aulas({})
@pytest.mark.clases(
        dict(día=Día.Lunes, horario_inicio=1, horario_fin=3),
        dict(día=Día.Lunes, horario_inicio=2, horario_fin=4),
        dict(día=Día.Lunes, horario_inicio=5, horario_fin=6)
    )
def test_superposición(aulas_preprocesadas, clases_preprocesadas, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    predicados = list(restricciones.no_superponer_clases(clases_lunes, aulas_preprocesadas, asignaciones))

    # Debería generar solamente un predicado entre las primeras dos clases
    assert len(predicados) == 1
    predicado = predicados[0]
    assert predicado_es_nand_entre_dos_variables(predicado, asignaciones[0,0], asignaciones[1,0])

@pytest.mark.clases( dict(horario_inicio=time(10), horario_fin=time(13), día=Día.Lunes) )
@pytest.mark.aulas(
    dict(horario_lunes=(time(10), time(13))), # Igual que la clase
    dict(horario_lunes=(time(10), time(11))), # Cierra temprano
    dict(horario_lunes=(time(11), time(13))), # Abre tarde
    dict(horario_lunes=(time( 9), time(14))), # Sobra
    dict(horario_lunes=(time(11), time(12))), # Abre tarde y cierra temprano
    dict(horario_lunes=(time( 0), time( 0))), # No abre los lunes
)
def test_aulas_cerradas(clases_preprocesadas, aulas_preprocesadas):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    prohibidas = list(restricciones.no_asignar_en_aula_cerrada(clases_lunes, aulas_preprocesadas))

    # Debería generar restricciones con las aulas 1, 2, 4 y 5
    assert len(prohibidas) == 4
    assert (0, 1) in prohibidas
    assert (0, 2) in prohibidas
    assert (0, 4) in prohibidas
    assert (0, 5) in prohibidas

@pytest.mark.clases( dict(equipamiento_necesario = set(('proyector',))) )
@pytest.mark.aulas(
    dict(equipamiento = set(('proyector',))),
    dict(equipamiento = set(('proyector', 'otra cosa'))),
    dict(equipamiento = set())
)
def test_equipamiento(clases_preprocesadas, aulas_preprocesadas):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    prohibidas = list(restricciones.asignar_aulas_con_el_equipamiento_requerido(clases_lunes, aulas_preprocesadas))

    # Debería generar una sola restricción con el aula 2
    assert len(prohibidas) == 1
    assert (0, 2) in prohibidas

@pytest.mark.edificios(
    dict(nombre='edificio 0', aulas_dobles={'102': ('102A', '102B')})
)
@pytest.mark.aulas(
    dict(edificio='edificio 0', nombre = '102'),
    dict(edificio='edificio 0', nombre = '102A'),
    dict(edificio='edificio 0', nombre = '102B')
)
@pytest.mark.clases(
    dict(día=Día.Lunes, nombre = 'Clase 1'),
    dict(día=Día.Lunes, nombre = 'Clase 2')
)
def test_aulas_dobles(aulas_preprocesadas, clases_preprocesadas, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    predicados = list(restricciones.no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo(clases_lunes, aulas_preprocesadas, asignaciones))
    
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[0, 0], asignaciones[1, 1]) for p in predicados)
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[0, 0], asignaciones[1, 2]) for p in predicados)
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[1, 0], asignaciones[0, 1]) for p in predicados)
    assert any(predicado_es_nand_entre_dos_variables(p, asignaciones[1, 0], asignaciones[0, 2]) for p in predicados)
