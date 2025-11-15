from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    HorariosSemanales, RangoHorario, crear_horarios_semanales
)

from conftest import campo_Edificio

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    assert gestor.get_edificios() == []
    assert gestor.cantidad_de_edificios() == 0

def test_agregar_edificio_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    assert gestor.cantidad_de_edificios() == 1
    assert len(gestor.get_edificios()) == 1
    assert 'sin nombre' in gestor.get_edificios()[0]

    assert 'sin nombre' in gestor.get_from_edificio(0, campo_Edificio['nombre'])
    assert gestor.get_from_edificio(0, campo_Edificio['aulas']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['aulas_dobles']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['horarios']) == crear_horarios_semanales()
    assert gestor.get_from_edificio(0, campo_Edificio['preferir_no_usar']) == False

def test_edificio_no_existe(gestor: GestorDeDatos):
    assert not gestor.existe_edificio('pepito')

    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'pepe')

    assert not gestor.existe_edificio('pepito')

def test_edificio_si_existe(gestor: GestorDeDatos):
    assert not gestor.existe_edificio('pepito')

    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'pepito')

    assert gestor.existe_edificio('pepito')

def test_get_set_edificio_inexistente(gestor: GestorDeDatos):
    with pytest.raises(IndexError):
        gestor.get_from_edificio(0, campo_Edificio['nombre'])
    
    with pytest.raises(IndexError):
        gestor.set_in_edificio(0, campo_Edificio['nombre'], None)

def test_get_set_campo_inexistente(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    with pytest.raises(IndexError):
        gestor.get_from_edificio(0, 100)

def test_get_set_edificio_existente(gestor: GestorDeDatos):
    nombre = 'nombresito'
    preferir_no_usar = True
    horarios = HorariosSemanales(RangoHorario(time(i), time(i+1)) for i in range(7))

    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], nombre)
    gestor.set_in_edificio(0, campo_Edificio['horarios'], horarios)
    gestor.set_in_edificio(0, campo_Edificio['preferir_no_usar'], preferir_no_usar)

    assert gestor.cantidad_de_edificios() == 1
    assert len(gestor.get_edificios()) == 1
    assert gestor.get_edificios() == [nombre]

    assert gestor.get_from_edificio(0, campo_Edificio['nombre']) == nombre
    assert gestor.get_from_edificio(0, campo_Edificio['aulas']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['aulas_dobles']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['horarios']) == horarios
    assert gestor.get_from_edificio(0, campo_Edificio['preferir_no_usar']) == preferir_no_usar

def test_agregar_edificios_nombres_distintos(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varios edificios, todos se agregan con nombres
    distintos y todos dicen 'sin nombre'.
    '''
    for _ in range(10):
        gestor.agregar_edificio()
    
    nombres = gestor.get_edificios()
    
    assert len(nombres) == 10
    assert gestor.cantidad_de_edificios() == 10
    assert all('sin nombre' in nombre for nombre in nombres)
    assert len(nombres) == len(set(nombres)) # No hay repetidos

def test_set_nombre_repetido(gestor: GestorDeDatos):
    '''
    Verificar que el gestor de datos no permite nombres de edificios repetidos.
    '''
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'A')
    gestor.agregar_edificio()
    gestor.set_in_edificio(1, campo_Edificio['nombre'], 'B')
    gestor.agregar_edificio()
    gestor.set_in_edificio(2, campo_Edificio['nombre'], 'C')

    # Setear el mismo nombre que ya tiene está bien
    gestor.set_in_edificio(2, campo_Edificio['nombre'], 'C')

    with pytest.raises(ValueError):
        gestor.set_in_edificio(2, campo_Edificio['nombre'], 'A')

def test_get_edificios_orden_afabético(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'b')
    gestor.agregar_edificio()
    gestor.set_in_edificio(1, campo_Edificio['nombre'], 'a')
    gestor.agregar_edificio()
    gestor.set_in_edificio(2, campo_Edificio['nombre'], 'd')

    assert gestor.get_edificios() == ['a', 'b', 'd']

def test_borrar_edificio(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'a')
    gestor.agregar_edificio()
    gestor.set_in_edificio(1, campo_Edificio['nombre'], 'b')
    gestor.agregar_edificio()
    gestor.set_in_edificio(2, campo_Edificio['nombre'], 'c')

    # Borrar edificio que existe
    gestor.borrar_edificio(1)
    assert gestor.cantidad_de_edificios() == 2
    assert gestor.get_edificios() == ['a', 'c']

    # Borrar edificio que no existe
    with pytest.raises(IndexError):
        gestor.borrar_edificio(2)

def test_ordenar_edificios(gestor: GestorDeDatos):
    # Ordenar cuando no hay edificios no debería tener ningún efecto:
    gestor.ordenar_edificios()

    # Ordenar cuando hay edificios debería ordenar los edificios:
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'b')
    gestor.agregar_edificio()
    gestor.set_in_edificio(1, campo_Edificio['nombre'], 'a')
    gestor.agregar_edificio()
    gestor.set_in_edificio(2, campo_Edificio['nombre'], 'd')

    assert gestor.get_from_edificio(0, campo_Edificio['nombre']) == 'b'
    assert gestor.get_from_edificio(1, campo_Edificio['nombre']) == 'a'
    assert gestor.get_from_edificio(2, campo_Edificio['nombre']) == 'd'

    gestor.ordenar_edificios()

    assert gestor.get_from_edificio(0, campo_Edificio['nombre']) == 'a'
    assert gestor.get_from_edificio(1, campo_Edificio['nombre']) == 'b'
    assert gestor.get_from_edificio(2, campo_Edificio['nombre']) == 'd'
