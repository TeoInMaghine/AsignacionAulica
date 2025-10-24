from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.entidades import Carreras, Edificios
from asignacion_aulica.lógica_de_asignación.asignación import asignar

from mocks import MockAula, MockClase, MockEdificio

@pytest.mark.aulas(
    MockAula(capacidad=60),
    MockAula(capacidad=40, equipamiento={"proyector"}),
)
@pytest.mark.clases(
    MockClase(día=Día.Lunes, cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}),
    MockClase(día=Día.Lunes, cantidad_de_alumnos=50),
    MockClase(día=Día.Miércoles, cantidad_de_alumnos=56),
    MockClase(día=Día.Miércoles, cantidad_de_alumnos=55),
)
def test_restricciones_y_preferencias(edificios: Edificios, carreras: Carreras):
    '''
    Verifica que las restricciones tienen prioridad sobre las preferencias,
    y las penalizaciones son minimizadas.
    '''
    resultado = asignar(edificios, carreras)
    assert resultado.todo_ok()

    asignaciones_esperadas = [1, 0, 0, 1]

    assert all(clase.aula_asignada.nombre == f'aula {esperada}' for clase, esperada in zip(carreras[0].materias[0].clases, asignaciones_esperadas))

@pytest.mark.edificios(MockEdificio(
    aulas=(
        MockAula(capacidad=60, nombre="doble"),
        MockAula(capacidad=30, nombre="hija 1"),
        MockAula(capacidad=35, nombre="hija 2"),
        MockAula(capacidad=1,  nombre="individual")
    ),
    aulas_dobles={0: (1, 2)}
))
@pytest.mark.clases(
    MockClase(cantidad_de_alumnos=60),
    MockClase(cantidad_de_alumnos=35),
    MockClase(cantidad_de_alumnos=30),
)
def test_aulas_dobles(edificios: Edificios, carreras: Carreras):
    '''
    Verifica que se asignan las aulas dobles correctamente, sin solaparse con
    las aulas que la conforman.
    '''
    # La individual no es preferida, pero es correcto que se asigne alguna
    # clase a esta porque no hay otra alternativa válida (no puede usarse la
    # doble y las hijas al mismo tiempo)
    asignaciones_esperadas = ['individual', 'hija 2', 'hija 1']

    resultado = asignar(edificios, carreras)
    assert resultado.todo_ok()

    assert all(clase.aula_asignada.nombre == esperada for clase, esperada in zip(carreras[0].materias[0].clases, asignaciones_esperadas))

@pytest.mark.aulas(MockAula())
@pytest.mark.clases(
    MockClase(día=Día.Lunes, horario=RangoHorario(time(8), time( 9))),
    MockClase(día=Día.Lunes, horario=RangoHorario(time(9), time(10)))
)
def test_horarios_no_solapan(edificios: Edificios, carreras: Carreras):
    '''
    Verifica que asigna con horarios que entran justo, incluyendo que si una
    clase empieza en una hora y otra termina a la misma hora que no tome que se
    están superponiendo.
    '''
    resultado = asignar(edificios, carreras)
    assert resultado.todo_ok()
    
    assert carreras[0].materias[0].clases[0].aula_asignada.nombre == 'aula 0'
    assert carreras[0].materias[0].clases[1].aula_asignada.nombre == 'aula 0'

@pytest.mark.aulas(MockAula())
@pytest.mark.clases(
        MockClase(horario=RangoHorario(time(8), time(10)), día=Día.Lunes),
        MockClase(horario=RangoHorario(time(9), time(11)), día=Día.Lunes)
    )
def test_asignación_imposible_por_solapamiento_inevitable(edificios: Edificios, carreras: Carreras):
    resultado = asignar(edificios, carreras)
    assert not resultado.todo_ok()
    assert resultado.días_sin_asignar == [Día.Lunes]

@pytest.mark.aulas( MockAula(horario_viernes=RangoHorario(time(8), time(23))) )
@pytest.mark.clases( MockClase(horario=RangoHorario(time(7), time(9)), día=Día.Viernes) )
def test_asignación_imposible_por_aula_cerrada(edificios: Edificios, carreras: Carreras):
    resultado = asignar(edificios, carreras)
    assert not resultado.todo_ok()
    assert resultado.días_sin_asignar == [Día.Viernes]

@pytest.mark.aulas( MockAula(capacidad=60) )
@pytest.mark.clases( MockClase(cantidad_de_alumnos=70, equipamiento_necesario={"proyector"}, día=Día.Martes) )
def test_asignación_imposible_por_equipamiento_y_capacidad(edificios: Edificios, carreras: Carreras):
    resultado = asignar(edificios, carreras)
    assert not resultado.todo_ok()
    assert resultado.días_sin_asignar == [Día.Martes]

@pytest.mark.edificios(
    MockEdificio(
        nombre='este no',
        preferir_no_usar=True,
        aulas=(MockAula(), MockAula())
    ),
    MockEdificio(
        nombre='este si',
        preferir_no_usar=False,
        aulas=(MockAula(), MockAula())
    )
)
@pytest.mark.clases(
    MockClase(cantidad_de_alumnos=15),
    MockClase(cantidad_de_alumnos=23),
    MockClase(cantidad_de_alumnos=2)
)
def test_evita_edificios_no_deseables(edificios: Edificios, carreras: Carreras):
    resultado = asignar(edificios, carreras)
    assert resultado.todo_ok()

    # Debería minimizar el uso de edificios no deseables poniendo las dos
    # clases grandes en aulas buenas y la clase chica en un aula mala.
    assert carreras[0].materias[0].clases[0].aula_asignada.edificio.nombre == 'este si'
    assert carreras[0].materias[0].clases[1].aula_asignada.edificio.nombre == 'este si'
    assert carreras[0].materias[0].clases[2].aula_asignada.edificio.nombre == 'este no'
