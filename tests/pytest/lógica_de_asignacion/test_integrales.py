import pytest

from asignacion_aulica import backend
from asignacion_aulica.backend.dia import Día

@pytest.mark.aulas(
    dict(capacidad=60),
    dict(capacidad=40, equipamiento={"proyector"}),
)
@pytest.mark.clases(
    dict(día=Día.LUNES, cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}),
    dict(día=Día.LUNES, cantidad_de_alumnos=50),
    dict(día=Día.MIÉRCOLES, cantidad_de_alumnos=56),
    dict(día=Día.MIÉRCOLES, cantidad_de_alumnos=55),
)
def test_restricciones_y_preferencias(aulas, clases):
    '''
    Verifica que las restricciones tienen prioridad sobre las preferencias,
    y las penalizaciones son minimizadas.
    '''
    backend.asignar(clases, aulas)
    asignaciones_esperadas = [1, 0, 0, 1]

    assert all(clases['aula_asignada'] == asignaciones_esperadas)

@pytest.mark.aulas(
    dict(capacidad=1, nombre="individual"),
    dict(capacidad=30, nombre="hija 1"),
    dict(capacidad=35, nombre="hija 2"),
    dict(capacidad=60, nombre="doble"),
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=60),
    dict(cantidad_de_alumnos=35),
    dict(cantidad_de_alumnos=30),
)
def test_aulas_dobles(aulas, clases):
    '''
    Verifica que se asignan las aulas dobles correctamente, sin solaparse con
    las aulas que la conforman.
    '''
    aulas_dobles = { 3: (1, 2) }

    # La individual no es preferida, pero es correcto que se asigne alguna
    # clase a esta porque no hay otra alternativa válida (no puede usarse la
    # doble y las hijas al mismo tiempo)
    asignaciones_esperadas = [2, 1, 0]

    backend.asignar(clases, aulas, aulas_dobles)
    assert all(clases['aula_asignada'] == asignaciones_esperadas)

@pytest.mark.aulas( dict(horarios={Día.LUNES: (8, 10)}) )
@pytest.mark.clases(
    dict(horario_inicio=8, horario_fin=9, día=Día.LUNES),
    dict(horario_inicio=9, horario_fin=10, día=Día.LUNES)
)
def test_horarios_no_solapan(aulas, clases):
    '''
    Verifica que asigna con horarios que entran justo, incluyendo que si una
    clase empieza en una hora y otra termina a la misma hora que no tome que se
    están superponiendo.
    '''
    asignaciones_esperadas = [0, 0]

    backend.asignar(clases, aulas)
    assert all(clases['aula_asignada'] == asignaciones_esperadas)

@pytest.mark.aulas( dict(horarios={Día.LUNES: (8, 10)}) )
@pytest.mark.clases(
        dict(horario_inicio=8, horario_fin=10, día=Día.LUNES),
        dict(horario_inicio=9, horario_fin=11, día=Día.LUNES)
    )
def test_asignación_imposible_por_solapamiento_inevitable(aulas, clases):
    with pytest.raises(backend.ImposibleAssignmentException):
        backend.asignar(clases, aulas)

@pytest.mark.aulas( dict(horarios={Día.LUNES: (8, 23)}) )
@pytest.mark.clases( dict(horario_inicio=7, horario_fin=9, día=Día.LUNES) )
def test_asignación_imposible_por_aula_cerrada(aulas, clases):
    with pytest.raises(backend.ImposibleAssignmentException):
        backend.asignar(clases, aulas)

@pytest.mark.aulas( dict(capacidad=60) )
@pytest.mark.clases( dict(día=Día.LUNES, cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}) )
def test_asignación_imposible_por_equipamiento(aulas, clases):
    with pytest.raises(backend.ImposibleAssignmentException):
        backend.asignar(clases, aulas)
