import pytest

from asignacion_aulica import backend
from helper_functions import *

def test_restricciones_y_preferencias():
    '''
    Verifica que las restricciones tienen prioridad sobre las preferencias,
    y las penalizaciones son minimizadas.
    '''

    aulas = make_aulas(
        dict(capacidad=60),
        dict(capacidad=40, equipamiento={"proyector"}),
    )

    clases = make_clases(
        dict(día="lunes", cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}),
        dict(día="lunes", cantidad_de_alumnos=50),
        dict(día="miércoles", cantidad_de_alumnos=56),
        dict(día="miércoles", cantidad_de_alumnos=55),
    )

    asignaciones = backend.asignar(clases, aulas)
    asignaciones_esperadas = [1, 0, 0, 1]

    for asignación, asignación_esperada in zip(asignaciones, asignaciones_esperadas):
        assert asignación == asignación_esperada

def test_aulas_dobles():
    '''
    Verifica que se asignan las aulas dobles correctamente, sin solaparse con
    las aulas que la conforman.
    '''

    # La individual no es preferida, pero es correcto que se asigne alguna
    # clase a esta porque no hay otra alternativa válida (no puede usarse la
    # doble y las hijas al mismo tiempo)
    aulas = make_aulas(
        dict(capacidad=1, nombre="individual"),
        dict(capacidad=30, nombre="hija 1"),
        dict(capacidad=35, nombre="hija 2"),
        dict(capacidad=60, nombre="doble"),
    )

    clases = make_clases(
        dict(cantidad_de_alumnos=60),
        dict(cantidad_de_alumnos=35),
        dict(cantidad_de_alumnos=30),
    )

    aulas_dobles = { 3: (1, 2) }

    asignaciones = backend.asignar(clases, aulas, aulas_dobles)
    asignaciones_esperadas = [2, 1, 0]

    for asignación, asignación_esperada in zip(asignaciones, asignaciones_esperadas):
        assert asignación == asignación_esperada

def test_horarios_no_solapan():
    '''
    Verifica que asigna con horarios que entran justo, incluyendo que si una
    clase empieza en una hora y otra termina a la misma hora que no tome que se
    están superponiendo.
    '''
    aulas = make_aulas(
        dict(horario_apertura=8, horario_cierre=10)
    )

    clases = make_clases(
        dict(horario_inicio=8, horario_fin=9),
        dict(horario_inicio=9, horario_fin=10)
    )

    asignaciones = backend.asignar(clases, aulas)
    asignaciones_esperadas = [0, 0]

    for asignación, asignación_esperada in zip(asignaciones, asignaciones_esperadas):
        assert asignación == asignación_esperada

def test_asignación_imposible_por_solapamiento_inevitable():
    aulas = make_aulas(
        dict(horario_apertura=8, horario_cierre=10)
    )

    clases = make_clases(
        dict(horario_inicio=8, horario_fin=10),
        dict(horario_inicio=9, horario_fin=11)
    )

    with pytest.raises(backend.ImposibleAssignmentException):
        asignaciones = backend.asignar(clases, aulas)

def test_asignación_imposible_por_aula_cerrada():
    aulas = make_aulas(
        dict(horario_apertura=8, horario_cierre=23)
    )

    clases = make_clases(
        dict(horario_inicio=7, horario_fin=9),
    )

    with pytest.raises(backend.ImposibleAssignmentException):
        asignaciones = backend.asignar(clases, aulas)

def test_asignación_imposible_por_equipamiento():

    aulas = make_aulas(
        dict(capacidad=60),
    )

    clases = make_clases(
        dict(día="lunes", cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}),
    )

    with pytest.raises(backend.ImposibleAssignmentException):
        asignaciones = backend.asignar(clases, aulas)

