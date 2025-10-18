from datetime import time
import pytest

from asignacion_aulica.lógica_de_asignación.excepciones import AsignaciónImposibleException
from asignacion_aulica.lógica_de_asignación.asignación import asignar
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

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
def test_restricciones_y_preferencias(edificios, aulas, carreras, materias, clases):
    '''
    Verifica que las restricciones tienen prioridad sobre las preferencias,
    y las penalizaciones son minimizadas.
    '''
    asignar(edificios, aulas, carreras, materias, clases)
    asignaciones_esperadas = [1, 0, 0, 1]

    assert all(clase.aula == f'aula {esperada}' for clase, esperada in zip(clases, asignaciones_esperadas))

@pytest.mark.edificios(dict(aulas_dobles={'doble': ('hija 1', 'hija 2')}))
@pytest.mark.aulas(
    dict(capacidad=60, nombre="doble"),
    dict(capacidad=30, nombre="hija 1"),
    dict(capacidad=35, nombre="hija 2"),
    dict(capacidad=1,  nombre="individual"),
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=60),
    dict(cantidad_de_alumnos=35),
    dict(cantidad_de_alumnos=30),
)
def test_aulas_dobles(edificios, aulas, carreras, materias, clases):
    '''
    Verifica que se asignan las aulas dobles correctamente, sin solaparse con
    las aulas que la conforman.
    '''
    # La individual no es preferida, pero es correcto que se asigne alguna
    # clase a esta porque no hay otra alternativa válida (no puede usarse la
    # doble y las hijas al mismo tiempo)
    asignaciones_esperadas = ['individual', 'hija 2', 'hija 1']

    asignar(edificios, aulas, carreras, materias, clases)
    assert all(clase.aula == esperada for clase, esperada in zip(clases, asignaciones_esperadas))

@pytest.mark.aulas({})
@pytest.mark.clases(
    dict(día=Día.Lunes, horario_inicio=time(8), horario_fin=time( 9)),
    dict(día=Día.Lunes, horario_inicio=time(9), horario_fin=time(10))
)
def test_horarios_no_solapan(edificios, aulas, carreras, materias, clases):
    '''
    Verifica que asigna con horarios que entran justo, incluyendo que si una
    clase empieza en una hora y otra termina a la misma hora que no tome que se
    están superponiendo.
    '''
    asignar(edificios, aulas, carreras, materias, clases)
    assert clases[0].aula == 'aula 0'
    assert clases[1].aula == 'aula 0'

@pytest.mark.aulas({})
@pytest.mark.clases(
        dict(horario_inicio=time(8), horario_fin=time(10), día=Día.Lunes),
        dict(horario_inicio=time(9), horario_fin=time(11), día=Día.Lunes)
    )
def test_asignación_imposible_por_solapamiento_inevitable(edificios, aulas, carreras, materias, clases):
    with pytest.raises(AsignaciónImposibleException):
        asignar(edificios, aulas, carreras, materias, clases)

@pytest.mark.aulas( dict(horario_lunes=(time(8), time(23))) )
@pytest.mark.clases( dict(horario_inicio=time(7), horario_fin=time(9), día=Día.Lunes) )
def test_asignación_imposible_por_aula_cerrada(edificios, aulas, carreras, materias, clases):
    with pytest.raises(AsignaciónImposibleException):
        asignar(edificios, aulas, carreras, materias, clases)

@pytest.mark.aulas( dict(capacidad=60) )
@pytest.mark.clases( dict(cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}) )
def test_asignación_imposible_por_equipamiento_y_capacidad(edificios, aulas, carreras, materias, clases):
    with pytest.raises(AsignaciónImposibleException):
        asignar(edificios, aulas, carreras, materias, clases)

@pytest.mark.edificios(
    dict(nombre='este no', preferir_no_usar=True),
    dict(nombre='este si', preferir_no_usar=False)
)
@pytest.mark.aulas(
    dict(edificio='este no'),
    dict(edificio='este no'),
    dict(edificio='este si'),
    dict(edificio='este si'),
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=15),
    dict(cantidad_de_alumnos=23),
    dict(cantidad_de_alumnos=2)
)
def test_evita_edificios_no_deseables(edificios, aulas, carreras, materias, clases):
    asignar(edificios, aulas, carreras, materias, clases)

    # Debería minimizar el uso de edificios no deseables poniendo las dos
    # clases grandes en aulas buenas y la clase chica en un aula mala.
    assert clases[0].edificio == 'este si'
    assert clases[1].edificio == 'este si'
    assert clases[2].edificio == 'este no'
