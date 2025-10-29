from datetime import time
from asignacion_aulica.gestor_de_datos.días_y_horarios import HorariosSemanales, RangoHorario, crear_horarios_semanales
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

import pytest

@pytest.fixture
def gestor() -> GestorDeDatos:
    '''
    Devuelve un gestor de datos inicialmente vacío.
    '''
    return GestorDeDatos()

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    assert gestor.get_edificios() == []
    assert gestor.cantidad_de_edificios() == 0

def test_edificio_no_existe(gestor: GestorDeDatos):
    assert not gestor.existe_edificio('pepito')

def test_get_set_edificio_inexistente(gestor: GestorDeDatos):
    with pytest.raises(IndexError):
        gestor.get_from_edificio(0, 0)
    
    with pytest.raises(IndexError):
        gestor.set_in_edificio(0, 0, None)

def test_add_edificio_valores_deafult(gestor: GestorDeDatos):
    gestor.add_edificio()

    assert gestor.cantidad_de_edificios() == 1
    assert len(gestor.get_edificios()) == 1
    assert 'sin nombre' in gestor.get_edificios()[0]

    assert 'sin nombre' in gestor.get_from_edificio(0, 0) # Nombre
    assert gestor.get_from_edificio(0, 1) == [] # Aulas
    assert gestor.get_from_edificio(0, 2) == [] # Aulas dobles
    assert gestor.get_from_edificio(0, 3) == crear_horarios_semanales() # Horarios
    assert gestor.get_from_edificio(0, 4) == False # Preferir no usar

def test_get_set_edificio_existente(gestor: GestorDeDatos):
    horarios = HorariosSemanales(RangoHorario(time(i), time(i+1)) for i in range(7))
    nombre = 'nombresito'
    preferir_no_usar = True

    gestor.add_edificio()
    gestor.set_in_edificio(0, 0, nombre)
    gestor.set_in_edificio(0, 3, horarios)
    gestor.set_in_edificio(0, 4, preferir_no_usar)

    assert gestor.cantidad_de_edificios() == 1
    assert len(gestor.get_edificios()) == 1
    assert nombre in gestor.get_edificios()[0]

    assert gestor.get_from_edificio(0, 0) == nombre
    assert gestor.get_from_edificio(0, 1) == [] # Aulas
    assert gestor.get_from_edificio(0, 2) == [] # Aulas dobles
    assert gestor.get_from_edificio(0, 3) == horarios
    assert gestor.get_from_edificio(0, 4) == preferir_no_usar
