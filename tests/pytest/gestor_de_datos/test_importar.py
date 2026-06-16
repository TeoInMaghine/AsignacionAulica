from datetime import time
from pathlib import Path
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.validación_de_datos.excepciones import DatoInválidoException
from mocks import MockAula, MockEdificio

def este_callback_no_debería_ser_llamado(_: list[str]) -> bool:
    raise AssertionError('Este callback no debería haber sido llamado.')

@pytest.mark.archivo('clases_nominal.xlsx')
def test_importar_clases_pero_no_existe_el_edificio(gestor: GestorDeDatos, archivo: Path):
    with pytest.raises(DatoInválidoException) as exc_info:
        gestor.importar_clases_de_excel(archivo, este_callback_no_debería_ser_llamado)
    
    mensaje = str(exc_info.value)
    assert 'Anasagasti 7' in mensaje

@pytest.mark.archivo('clases_nominal.xlsx')
@pytest.mark.edificios(MockEdificio(nombre='Anasagasti 7'))
def test_importar_clases_pero_no_existe_el_aula(gestor: GestorDeDatos, archivo: Path):
    with pytest.raises(DatoInválidoException) as exc_info:
        gestor.importar_clases_de_excel(archivo, este_callback_no_debería_ser_llamado)
    
    mensaje = str(exc_info.value)
    assert 'B202' in mensaje

@pytest.mark.archivo('clases_nominal.xlsx')
@pytest.mark.edificios(MockEdificio(nombre='Anasagasti 7', aulas=(MockAula(nombre='B202'),)))
def test_importar_datos_de_una_carrera(gestor: GestorDeDatos, archivo: Path):
    gestor.importar_clases_de_excel(archivo, lambda x: False)

    assert gestor.cantidad_de_carreras() == 1
    assert gestor.get_carreras() == ['Acá va el nombre de la carrera']
    assert gestor.cantidad_de_materias(0) == 2

    materia0 = gestor.get_materia(0, 0)
    assert materia0.nombre == 'Intoducción a cosas'
    assert materia0.año == 1
    assert materia0.cuatrimestral_o_anual == 'Cuatrimestral'
    
    assert gestor.cantidad_de_clases(0, 0) == 2
    clase0_0 = gestor.get_clase(0, 0, 0)
    assert clase0_0.comisión == 'COM1B'
    assert clase0_0.cantidad_de_alumnos == 100
    assert clase0_0.día == Día.Lunes
    assert clase0_0.horario == RangoHorario(time(15, 30), time(18))
    assert clase0_0.aula_asignada == TODO
    assert clase0_0.teórica_o_práctica == 'Las dos cosas'
    assert clase0_0.docente == 'Charly García'
    assert clase0_0.auxiliar == 'Nadie'
    assert clase0_0.promocionable == 'Si (8)'

    # TODO: etc
