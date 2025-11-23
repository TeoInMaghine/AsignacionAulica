from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    HorariosSemanales, RangoHorario, crear_horarios_semanales
)

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    assert gestor.get_carreras() == []

def test_agregar_carrera_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.agregar_carrera()

    assert len(gestor.get_carreras()) == 1
    assert 'sin nombre' in gestor.get_carreras()[0]

    assert 'sin nombre' in gestor.get_carrera(0).nombre
    assert gestor.get_carrera(0).edificio_preferido is None
    assert gestor.get_carrera(0).materias == []

def test_add_varias_carreras(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varias carreras, todas se agregan con nombres
    distintos y todas dicen 'sin nombre'.
    '''
    for _ in range(10):
        gestor.agregar_carrera()
    
    nombres = gestor.get_carreras()
    
    assert len(nombres) == 10
    assert all('sin nombre' in nombre for nombre in nombres)
    assert len(nombres) == len(set(nombres)) # No hay repetidos

def test_carrera_existe_o_no(gestor: GestorDeDatos):
    # Al principio no existe
    assert not gestor.existe_carrera('pepito')

    # Al agregar una carrera sin nombre sigue sin existir
    gestor.agregar_carrera()
    assert not gestor.existe_carrera('pepito')

    # Al agregar una carrera con otro nombre sigue sin existir
    gestor.set_carrera_nombre(0, 'pepe')
    assert not gestor.existe_carrera('pepito')

    # Al agregar una carrera con ese nombre sí existe
    gestor.agregar_carrera()
    gestor.set_carrera_nombre(1, 'pepito')
    assert gestor.existe_carrera('pepito')

def test_get_set_fuera_de_rango(gestor: GestorDeDatos):
    # Cuando no existe ninguna carrera:
    with pytest.raises(IndexError):
        gestor.get_carrera(0)
    with pytest.raises(IndexError):
        gestor.set_carrera_edificio_preferido(0, None)
    with pytest.raises(IndexError):
        gestor.set_carrera_nombre(0, 'a')
    
    # Cuando existen carreras pero el índice está fuera de rango:
    gestor.agregar_carrera()
    gestor.agregar_carrera()
    gestor.agregar_carrera()

    with pytest.raises(IndexError):
        gestor.get_carrera(3)
    with pytest.raises(IndexError):
        gestor.set_carrera_edificio_preferido(3, None)
    with pytest.raises(IndexError):
        gestor.set_carrera_nombre(3, 'a')

def test_get_set_carrera_existente(gestor: GestorDeDatos):
    nombre = 'nombresito'
    edificio_preferido = 'uno'

    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.set_in_edificio(0, campo_Edificio['nombre'], edificio_preferido)
    el_edificio = gestor.get_from_aula(0, 0, campo_Aula['edificio'])

    gestor.agregar_carrera()
    gestor.set_carrera_nombre(0, nombre)
    gestor.set_carrera_edificio_preferido(0, edificio_preferido)

    assert len(gestor.get_carreras()) == 1

    carrera = gestor.get_carrera(0)
    assert carrera.nombre == nombre
    assert carrera.edificio_preferido is el_edificio

def test_cambiar_nombre_mantiene_orden_afabético(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    nuevo_índice = gestor.set_carrera_nombre(0, 'b')
    assert nuevo_índice == 0
    assert gestor.get_carreras() == ['b']

    gestor.agregar_carrera()
    nuevo_índice = gestor.set_carrera_nombre(1, 'a')
    assert nuevo_índice == 0
    assert gestor.get_carreras() == ['a', 'b']

    gestor.agregar_carrera()
    nuevo_índice = gestor.set_carrera_nombre(2, 'c')
    assert nuevo_índice == 2
    assert gestor.get_carreras() == ['a', 'b', 'c']

    gestor.agregar_carrera()
    nuevo_índice = gestor.set_carrera_nombre(3, 'a2')
    assert nuevo_índice == 1
    assert gestor.get_carreras() == ['a', 'a2', 'b', 'c']

def test_borrar_carrera(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_carrera()
    gestor.agregar_carrera()
    gestor.set_carrera_nombre(0, 'a')
    gestor.set_carrera_nombre(1, 'b')
    gestor.set_carrera_nombre(2, 'c')

    # Borrar carrera que existe
    gestor.borrar_carrera(1)
    assert gestor.get_carreras() == ['a', 'c']

    # Borrar carrera que no existe
    with pytest.raises(IndexError):
        gestor.borrar_carrera(2)

def test_borrar_edificio_borra_edificio_preferido_de_las_carreras_que_preferían_ese_edificio(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_edificio()
    gestor.agregar_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'a')
    gestor.set_in_edificio(1, campo_Edificio['nombre'], 'b')
    gestor.set_in_edificio(2, campo_Edificio['nombre'], 'c')
    gestor.agregar_aula(1)
    gestor.agregar_aula(2)
    edificio_b = gestor.get_from_aula(1, 0, campo_Aula['edificio'])
    edificio_c = gestor.get_from_aula(2, 0, campo_Aula['edificio'])

    gestor.agregar_carrera()
    gestor.agregar_carrera()
    gestor.set_carrera_edificio_preferido(0, 'c')
    gestor.set_carrera_edificio_preferido(1, 'b')

    assert gestor.get_carrera(0).edificio_preferido is edificio_c
    assert gestor.get_carrera(1).edificio_preferido is edificio_b

    gestor.borrar_edificio(1)

    assert gestor.get_carrera(0).edificio_preferido is edificio_c
    assert gestor.get_carrera(1).edificio_preferido is None

