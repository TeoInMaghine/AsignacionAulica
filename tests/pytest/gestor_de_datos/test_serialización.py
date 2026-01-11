from datetime import time
import pytest
from pathlib import Path
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

@pytest.fixture
def tmp_filename(tmp_path: Path) -> Path:
    '''
    :return: A filename inside a temporary directory created for each  test.
    '''
    return tmp_path / "tmp_file"

def test_roundtrip_vacío(tmp_filename: Path):
    gestor = GestorDeDatos(tmp_filename)
    gestor.guardar()

    gestor2 = GestorDeDatos(tmp_filename)
    assert gestor2.cantidad_de_edificios() == 0
    assert gestor2.cantidad_de_carreras() == 0
    assert gestor2.get_equipamientos_existentes() == []

def test_roundtrip_con_aulas(tmp_filename: Path):
    gestor = GestorDeDatos(tmp_filename)

    gestor.agregar_edificio()
    edificio = gestor.get_edificio(0)
    edificio.preferir_no_usar = True
    edificio.nombre = 'E0'
    edificio.horarios[Día.Martes].fin = time(1,2)

    gestor.agregar_aula(0)
    gestor.agregar_aula(0)
    aula = gestor.get_aula(0, 1)
    aula.nombre = 'A01'
    
    gestor.agregar_edificio()

    gestor.guardar()

    gestor2 = GestorDeDatos(tmp_filename)
    assert gestor2.cantidad_de_edificios() == 2
    edificio2 = gestor2.get_edificio(0)
    assert edificio2.preferir_no_usar is True
    assert edificio2.nombre == 'E0'
    assert edificio2.horarios[Día.Martes].fin == time(1,2)

    assert gestor2.cantidad_de_aulas(0) == 2
    aula2 = gestor2.get_aula(0, 1)
    assert aula2.nombre == 'A01'
    assert aula2.edificio is edificio2

def test_roundtrip_con_clases(tmp_filename: Path):
    gestor = GestorDeDatos(tmp_filename)

    gestor.agregar_carrera('C0')
    gestor.agregar_carrera('C1')

    gestor.agregar_materia(1)
    materia = gestor.get_materia(1, 0)
    materia.nombre = 'M 1 0'
    materia.año = 15
    materia.cuatrimestral_o_anual = 'un string'

    gestor.agregar_clase(1, 0)
    clase = gestor.get_clase(1, 0, 0)
    clase.día = Día.Domingo
    clase.cantidad_de_alumnos = 666
    gestor.agregar_equipamiento_a_clase(1, 0, 0, 'A')

    gestor.guardar()

    gestor2 = GestorDeDatos(tmp_filename)
    assert gestor2.cantidad_de_carreras() == 2
    assert gestor2.get_carrera(0).nombre == 'C0'
    assert gestor2.get_carrera(1).nombre == 'C1'

    assert gestor2.cantidad_de_carreras() == 2
    materia2 = gestor2.get_materia(1, 0)
    assert materia2.carrera is gestor2.get_carrera(1)
    assert materia2.nombre == 'M 1 0'
    assert materia2.año == 15
    assert materia2.cuatrimestral_o_anual == 'un string'

    assert gestor2.cantidad_de_clases(1, 0) == 1
    clase2 = gestor2.get_clase(1, 0, 0)
    assert clase2.materia is materia2
    assert clase2.día == Día.Domingo
    assert clase2.cantidad_de_alumnos == 666
    assert clase2.equipamiento_necesario == {'A'}
    assert gestor2.get_equipamientos_existentes() == ['A']
