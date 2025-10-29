from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    HorariosSemanales, RangoHorario, crear_horarios_semanales
)
from asignacion_aulica.gestor_de_datos.entidades import (
    fieldnames_Aula, fieldnames_AulaDoble, fieldnames_Carrera, fieldnames_Clase,
    fieldnames_Edificio, fieldnames_Materia
)
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

# Índices de los campos, en diccionarios para más legibilidad:
campo_Edificio:  dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Edificio)}
campo_Aula:      dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Aula)}
campo_AulaDoble: dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_AulaDoble)}
campo_Carrera:   dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Carrera)}
campo_Materia:   dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Materia)}
campo_Clase:     dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Clase)}

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
        gestor.get_from_edificio(0, campo_Edificio['nombre'])
    
    with pytest.raises(IndexError):
        gestor.set_in_edificio(0, campo_Edificio['nombre'], None)

def test_add_edificio_valores_deafult(gestor: GestorDeDatos):
    gestor.add_edificio()

    assert gestor.cantidad_de_edificios() == 1
    assert len(gestor.get_edificios()) == 1
    assert 'sin nombre' in gestor.get_edificios()[0]

    assert 'sin nombre' in gestor.get_from_edificio(0, campo_Edificio['nombre'])
    assert gestor.get_from_edificio(0, campo_Edificio['aulas']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['aulas_dobles']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['horarios']) == crear_horarios_semanales()
    assert gestor.get_from_edificio(0, campo_Edificio['preferir_no_usar']) == False

def test_add_edificios_nombres_distintos(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varios edificios, todos se agregan con nombres
    distintos y todos dicen 'sin nombre'.
    '''
    for _ in range(10):
        gestor.add_edificio()
    
    nombres = gestor.get_edificios()
    
    assert len(nombres) == 10
    assert all('sin nombre' in nombre for nombre in nombres)
    assert len(nombres) == len(set(nombres)) # No hay repetidos

def test_get_set_edificio_existente(gestor: GestorDeDatos):
    nombre = 'nombresito'
    preferir_no_usar = True
    horarios = HorariosSemanales(RangoHorario(time(i), time(i+1)) for i in range(7))

    gestor.add_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], nombre)
    gestor.set_in_edificio(0, campo_Edificio['horarios'], horarios)
    gestor.set_in_edificio(0, campo_Edificio['preferir_no_usar'], preferir_no_usar)

    assert gestor.cantidad_de_edificios() == 1
    assert len(gestor.get_edificios()) == 1
    assert nombre in gestor.get_edificios()[0]

    assert gestor.get_from_edificio(0, campo_Edificio['nombre']) == nombre
    assert gestor.get_from_edificio(0, campo_Edificio['aulas']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['aulas_dobles']) == []
    assert gestor.get_from_edificio(0, campo_Edificio['horarios']) == horarios
    assert gestor.get_from_edificio(0, campo_Edificio['preferir_no_usar']) == preferir_no_usar

def test_get_edificios_orden_afabético(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.set_in_edificio(0, campo_Edificio['nombre'], 'b')
    gestor.add_edificio()
    gestor.set_in_edificio(1, campo_Edificio['nombre'], 'a')
    gestor.add_edificio()
    gestor.set_in_edificio(2, campo_Edificio['nombre'], 'd')

    assert gestor.get_edificios() == ['a', 'b', 'd']