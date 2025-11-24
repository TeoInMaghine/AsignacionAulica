import pytest

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificio

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay edificio, así que no se puede preguntar por las aulas:
    with pytest.raises(IndexError):
        gestor.cantidad_de_aulas(0)
    with pytest.raises(IndexError):
        gestor.get_aulas(0)
    
    # Al agregar un edificio, no tiene ningún aula:
    gestor.agregar_edificio()
    assert gestor.cantidad_de_aulas(0) == 0
    assert gestor.get_aulas(0) == []

def test_agregar_aula_genera_valores_default(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula(0)

    assert gestor.cantidad_de_aulas(0) == 1
    assert len(gestor.get_aulas(0)) == 1

    aula_1: Aula = gestor.get_aula(0, 0)
    assert isinstance(aula_1.nombre, str)
    assert isinstance(aula_1.edificio, Edificio)
    assert aula_1.capacidad >= 0
    assert aula_1.equipamiento == set()
    assert aula_1.horarios == [None,]*7

    # Segundo aula pertenece al mismo edificio:
    gestor.agregar_aula(0)
    aula_2: Aula = gestor.get_aula(0, 1)
    assert aula_1.edificio is aula_2.edificio

def test_add_varias_aulas(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varias aulas, todas se agregan con nombres
    distintos.
    '''
    gestor.agregar_edificio()
    gestor.agregar_edificio()
    for _ in range(10):
        gestor.agregar_aula(0)
    for _ in range(4):
        gestor.agregar_aula(1)
    
    nombres0 = gestor.get_aulas(0)
    nombres1 = gestor.get_aulas(1)
    
    assert len(nombres0) == 10
    assert gestor.cantidad_de_aulas(0) == 10
    assert all(isinstance(nombre, str) for nombre in nombres0)
    assert len(nombres0) == len(set(nombres0)) # No hay repetidos

    assert len(nombres1) == 4
    assert gestor.cantidad_de_aulas(1) == 4
    assert all(isinstance(nombre, str) for nombre in nombres1)
    assert len(nombres1) == len(set(nombres1)) # No hay repetidos

    # Chequear que se crearon dos edificios
    assert gestor.get_aula(0, 0).edificio is not gestor.get_aula(1, 0).edificio

def test_aula_existe_o_no(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    assert not gestor.existe_aula(0, 'pepito')

    gestor.agregar_aula(0)
    gestor.get_aula(0, 0).nombre = 'pepe'
    assert not gestor.existe_aula(0, 'pepito')

    gestor.agregar_aula(0)
    gestor.get_aula(0, 1).nombre = 'pepito'
    assert gestor.existe_aula(0, 'pepito')

def test_get_fuera_de_rango(gestor: GestorDeDatos):
    with pytest.raises(IndexError):
        gestor.get_aula(0, 0)

    gestor.agregar_edificio()

    with pytest.raises(IndexError):
        gestor.get_aula(0, 0)
    
def test_get_aulas_orden_afabético(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.get_aula(0, 0).nombre = 'b'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 1).nombre = 'a'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 2).nombre = 'd'

    assert gestor.get_aulas(0) == ['a', 'b', 'd']

def test_ordenar_aulas(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    # Ordenar cuando no hay aulas, no debería tener ningún efecto:
    gestor.ordenar_aulas(0)

    # Ordenar cuando hay aulas, debería ordenar las aulas:
    gestor.agregar_aula(0)
    gestor.get_aula(0, 0).nombre = 'b'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 1).nombre = 'a'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 2).nombre = 'd'

    assert gestor.get_aula(0, 0).nombre == 'b'
    assert gestor.get_aula(0, 1).nombre == 'a'
    assert gestor.get_aula(0, 2).nombre == 'd'

    gestor.ordenar_aulas(0)

    assert gestor.get_aula(0, 0).nombre == 'a'
    assert gestor.get_aula(0, 1).nombre == 'b'
    assert gestor.get_aula(0, 2).nombre == 'd'

def test_borrar_aula(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.get_aula(0, 0).nombre = 'a'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 1).nombre = 'b'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 2).nombre = 'c'

    # Borrar aula que existe
    gestor.borrar_aula(0, 1)
    assert gestor.cantidad_de_aulas(0) == 2
    assert gestor.get_aulas(0) == ['a', 'c']

    # Borrar aula que no existe
    with pytest.raises(IndexError):
        gestor.borrar_aula(0, 2)
    with pytest.raises(IndexError):
        gestor.borrar_aula(1, 0)
