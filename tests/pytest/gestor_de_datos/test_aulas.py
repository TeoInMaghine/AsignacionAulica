import pytest

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


def test_aula_existe_o_no(gestor: GestorDeDatos):
    gestor.add_edificio()
    assert not gestor.existe_aula(0, 'pepito')

    gestor.add_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'pepe')
    assert not gestor.existe_aula(0, 'pepito')

    gestor.add_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'pepito')
    assert gestor.existe_aula(0, 'pepito')