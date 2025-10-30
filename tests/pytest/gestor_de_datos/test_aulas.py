from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import HorariosSemanalesOpcionales, RangoHorario
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Edificio

from conftest import campo_Edificio, campo_Aula

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay edificio, así que no se puede preguntar por las aulas:
    with pytest.raises(IndexError):
        gestor.cantidad_de_aulas(0)
    with pytest.raises(IndexError):
        gestor.get_aulas(0)
    
    # Al agregar un edificio, no tiene ningún aula:
    gestor.add_edificio()
    assert gestor.cantidad_de_aulas(0) == 0
    assert gestor.get_aulas(0) == []

def test_add_aula_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula(0)

    assert gestor.cantidad_de_aulas(0) == 1
    assert len(gestor.get_aulas(0)) == 1
    assert 'sin nombre' in gestor.get_aulas(0)[0]

    assert 'sin nombre' in gestor.get_from_aula(0, 0, campo_Aula['nombre'])
    assert isinstance(gestor.get_from_aula(0, 0, campo_Aula['edificio']), Edificio)
    assert gestor.get_from_aula(0, 0, campo_Aula['capacidad']) >= 0
    assert gestor.get_from_aula(0, 0, campo_Aula['equipamiento']) == set()
    assert gestor.get_from_aula(0, 0, campo_Aula['horarios']) == (None,)*7

    # Segundo aula pertenece al mismo edificio:
    gestor.add_aula(0)
    assert gestor.get_from_aula(0, 0, campo_Aula['edificio']) is gestor.get_from_aula(0, 1, campo_Aula['edificio'])

def test_add_varias_aulas(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varias aulas, todas se agregan con nombres
    distintos y todas dicen 'sin nombre'.
    '''
    gestor.add_edificio()
    gestor.add_edificio()
    for _ in range(10):
        gestor.add_aula(0)
    for _ in range(4):
        gestor.add_aula(1)
    
    nombres0 = gestor.get_aulas(0)
    nombres1 = gestor.get_aulas(1)
    
    assert len(nombres0) == 10
    assert gestor.cantidad_de_aulas(0) == 10
    assert all('sin nombre' in nombre for nombre in nombres0)
    assert len(nombres0) == len(set(nombres0)) # No hay repetidos

    assert len(nombres1) == 4
    assert gestor.cantidad_de_aulas(1) == 4
    assert all('sin nombre' in nombre for nombre in nombres1)
    assert len(nombres1) == len(set(nombres1)) # No hay repetidos

    # Chequear que se crearon dos edificios
    assert gestor.get_from_aula(0, 0, campo_Aula['edificio']) is not gestor.get_from_aula(1, 0, campo_Aula['edificio'])

def test_aula_existe_o_no(gestor: GestorDeDatos):
    gestor.add_edificio()
    assert not gestor.existe_aula(0, 'pepito')

    gestor.add_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'pepe')
    assert not gestor.existe_aula(0, 'pepito')

    gestor.add_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'pepito')
    assert gestor.existe_aula(0, 'pepito')

def test_get_set_fuera_de_rango(gestor: GestorDeDatos):
    gestor.add_edificio()

    with pytest.raises(IndexError):
        gestor.get_from_aula(0, 0, campo_Aula['capacidad'])
    
    with pytest.raises(IndexError):
        gestor.set_in_aula(0, 0, campo_Edificio['nombre'], None)

    gestor.add_aula_doble(0)
    with pytest.raises(IndexError):
        gestor.get_from_aula(0, 0, 100)

def test_get_set_aula_existente(gestor: GestorDeDatos):
    nombre = 'nombresito'
    capacidad = 15
    equipamiento = {'a', 'b'}
    horarios = HorariosSemanalesOpcionales(RangoHorario(time(i), time(i+1)) for i in range(7))

    gestor.add_edificio()
    gestor.add_aula(0)
    gestor.set_in_aula(0,0, campo_Aula['nombre'], nombre)
    gestor.set_in_aula(0,0, campo_Aula['capacidad'], capacidad)
    gestor.set_in_aula(0,0, campo_Aula['equipamiento'], equipamiento)
    gestor.set_in_aula(0,0, campo_Aula['horarios'], horarios)

    assert gestor.cantidad_de_edificios() == 1
    assert gestor.cantidad_de_aulas(0) == 1
    assert len(gestor.get_aulas(0)) == 1
    assert gestor.get_aulas(0) == [nombre]

    assert gestor.get_from_aula(0,0, campo_Aula['nombre']) == nombre
    assert gestor.get_from_aula(0,0, campo_Aula['capacidad']) == capacidad
    assert gestor.get_from_aula(0,0, campo_Aula['equipamiento']) == equipamiento
    assert gestor.get_from_aula(0,0, campo_Aula['horarios']) == horarios

def test_get_aulas_orden_afabético(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'b')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'a')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 2, campo_Aula['nombre'], 'd')

    assert gestor.get_aulas(0) == ['a', 'b', 'd']

def test_ordenar_aulas(gestor: GestorDeDatos):
    gestor.add_edificio()

    # Ordenar cuando no hay aulas no debería tener ningún efecto:
    gestor.ordenar_aulas(0)

    # Ordenar cuando hay aulas debería ordenar las aulas:
    gestor.add_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'b')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'a')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 2, campo_Aula['nombre'], 'd')

    assert gestor.get_from_aula(0, 0, campo_Aula['nombre']) == 'b'
    assert gestor.get_from_aula(0, 1, campo_Aula['nombre']) == 'a'
    assert gestor.get_from_aula(0, 2, campo_Aula['nombre']) == 'd'

    gestor.ordenar_aulas(0)

    assert gestor.get_from_aula(0, 0, campo_Aula['nombre']) == 'a'
    assert gestor.get_from_aula(0, 1, campo_Aula['nombre']) == 'b'
    assert gestor.get_from_aula(0, 2, campo_Aula['nombre']) == 'd'

def test_borrar_aula(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'a')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'b')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 2, campo_Aula['nombre'], 'c')

    # Borrar aula que existe
    gestor.borrar_aula(0, 1)
    assert gestor.cantidad_de_aulas(0) == 2
    assert gestor.get_aulas(0) == ['a', 'c']

    # Borrar aula que no existe
    with pytest.raises(IndexError):
        gestor.borrar_aula(0, 2)
    with pytest.raises(IndexError):
        gestor.borrar_aula(1, 0)