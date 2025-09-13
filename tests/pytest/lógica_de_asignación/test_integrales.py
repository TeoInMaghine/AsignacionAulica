import pytest

from asignacion_aulica import lógica_de_asignación
from asignacion_aulica.gestor_de_datos import Día

@pytest.mark.aulas(
    dict(capacidad=60),
    dict(capacidad=40, equipamiento={"proyector"}),
)
@pytest.mark.clases(
    dict(día=Día.Lunes, cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}),
    dict(día=Día.Lunes, cantidad_de_alumnos=50),
    dict(día=Día.Miércoles, cantidad_de_alumnos=56),
    dict(día=Día.Miércoles, cantidad_de_alumnos=55),
)
def test_restricciones_y_preferencias(aulas, clases):
    '''
    Verifica que las restricciones tienen prioridad sobre las preferencias,
    y las penalizaciones son minimizadas.
    '''
    lógica_de_asignación.asignar(clases, aulas)
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

    lógica_de_asignación.asignar(clases, aulas, aulas_dobles)
    assert all(clases['aula_asignada'] == asignaciones_esperadas)

@pytest.mark.aulas( dict(horarios={Día.Lunes: (8, 10)}) )
@pytest.mark.clases(
    dict(horario_inicio=8, horario_fin=9, día=Día.Lunes),
    dict(horario_inicio=9, horario_fin=10, día=Día.Lunes)
)
def test_horarios_no_solapan(aulas, clases):
    '''
    Verifica que asigna con horarios que entran justo, incluyendo que si una
    clase empieza en una hora y otra termina a la misma hora que no tome que se
    están superponiendo.
    '''
    asignaciones_esperadas = [0, 0]

    lógica_de_asignación.asignar(clases, aulas)
    assert all(clases['aula_asignada'] == asignaciones_esperadas)

@pytest.mark.aulas( dict(horarios={Día.Lunes: (8, 10)}) )
@pytest.mark.clases(
        dict(horario_inicio=8, horario_fin=10, día=Día.Lunes),
        dict(horario_inicio=9, horario_fin=11, día=Día.Lunes)
    )
def test_asignación_imposible_por_solapamiento_inevitable(aulas, clases):
    with pytest.raises(lógica_de_asignación.AsignaciónImposibleException):
        lógica_de_asignación.asignar(clases, aulas)

@pytest.mark.aulas( dict(horarios={Día.Lunes: (8, 23)}) )
@pytest.mark.clases( dict(horario_inicio=7, horario_fin=9, día=Día.Lunes) )
def test_asignación_imposible_por_aula_cerrada(aulas, clases):
    with pytest.raises(lógica_de_asignación.AsignaciónImposibleException):
        lógica_de_asignación.asignar(clases, aulas)

@pytest.mark.aulas( dict(capacidad=60) )
@pytest.mark.clases( dict(día=Día.Lunes, cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}) )
def test_asignación_imposible_por_equipamiento(aulas, clases):
    with pytest.raises(lógica_de_asignación.AsignaciónImposibleException):
        lógica_de_asignación.asignar(clases, aulas)

@pytest.mark.aulas(
    dict(preferir_no_usar=True),
    dict(preferir_no_usar=False),
    dict(preferir_no_usar=True),
    dict(preferir_no_usar=False)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=15),
    dict(cantidad_de_alumnos=23),
    dict(cantidad_de_alumnos=2)
)
def test_evita_edificios_no_deseables(aulas, clases):
    lógica_de_asignación.asignar(clases, aulas)

    # Debería minimizar el uso de edificios no deseables poniendo las dos
    # clases grandes en aulas buenas y la clase chica en un aula mala.
    assert clases.at[0, 'aula_asignada'] in {1, 3}
    assert clases.at[1, 'aula_asignada'] in {1, 3}
    assert clases.at[2, 'aula_asignada'] in {0, 2}
