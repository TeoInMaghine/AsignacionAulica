import pytest

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Edificio
from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    crear_horarios_semanales
)

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    assert gestor.get_edificios() == []
    assert gestor.cantidad_de_edificios() == 0

def test_agregar_edificio_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    assert gestor.cantidad_de_edificios() == 1
    assert len(gestor.get_edificios()) == 1
    assert isinstance(gestor.get_edificios()[0], str)

    edificio: Edificio = gestor.get_edificio(0)
    assert isinstance(edificio.nombre, str)
    assert edificio.aulas == []
    assert edificio.aulas_dobles == []
    assert edificio.horarios == crear_horarios_semanales()
    assert edificio.preferir_no_usar == False

def test_edificio_no_existe(gestor: GestorDeDatos):
    assert not gestor.existe_edificio('pepito')

    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'pepe'

    assert not gestor.existe_edificio('pepito')

def test_edificio_si_existe(gestor: GestorDeDatos):
    assert not gestor.existe_edificio('pepito')

    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'pepito'

    assert gestor.existe_edificio('pepito')

def test_get_edificio_inexistente(gestor: GestorDeDatos):
    with pytest.raises(IndexError):
        gestor.get_edificio(0)

def test_agregar_edificios_nombres_distintos(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varios edificios, todos se agregan con nombres
    distintos.
    '''
    for _ in range(10):
        gestor.agregar_edificio()
    
    nombres = gestor.get_edificios()
    
    assert len(nombres) == 10
    assert gestor.cantidad_de_edificios() == 10
    assert all(isinstance(nombre, str) for nombre in nombres)
    assert len(nombres) == len(set(nombres)) # No hay repetidos

def test_get_edificios_orden_afabético(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'b'
    gestor.agregar_edificio()
    gestor.get_edificio(1).nombre = 'a'
    gestor.agregar_edificio()
    gestor.get_edificio(2).nombre = 'd'

    assert gestor.get_edificios() == ['a', 'b', 'd']

def test_borrar_edificio(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.get_edificio(0).nombre = 'a'
    gestor.agregar_edificio()
    gestor.get_edificio(1).nombre = 'b'
    gestor.agregar_edificio()
    gestor.get_edificio(2).nombre = 'c'

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
    gestor.get_edificio(0).nombre = 'b'
    gestor.agregar_edificio()
    gestor.get_edificio(1).nombre = 'a'
    gestor.agregar_edificio()
    gestor.get_edificio(2).nombre = 'd'

    assert gestor.get_edificio(0).nombre == 'b'
    assert gestor.get_edificio(1).nombre == 'a'
    assert gestor.get_edificio(2).nombre == 'd'

    gestor.ordenar_edificios()

    assert gestor.get_edificio(0).nombre == 'a'
    assert gestor.get_edificio(1).nombre == 'b'
    assert gestor.get_edificio(2).nombre == 'd'
