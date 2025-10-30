from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import HorariosSemanalesOpcionales, RangoHorario
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos, aula_no_seleccionada
from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificio

from conftest import campo_AulaDoble, campo_Edificio, campo_Aula

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay edificio, así que no se puede preguntar por las aulas:
    with pytest.raises(IndexError):
        gestor.cantidad_de_aulas_dobles(0)
    
    # Al agregar un edificio, no tiene ningún aula doble:
    gestor.add_edificio()
    assert gestor.cantidad_de_aulas_dobles(0) == 0

def test_add_aula_doble_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula_doble(0)

    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande']) is aula_no_seleccionada
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_1']) is aula_no_seleccionada
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_2']) is aula_no_seleccionada

def test_add_varias_aulas_dobles(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_edificio()
    for _ in range(3):
        gestor.add_aula_doble(1)
    
    assert gestor.cantidad_de_aulas_dobles(0) == 0
    assert gestor.cantidad_de_aulas_dobles(1) == 3

def test_get_set_fuera_de_rango(gestor: GestorDeDatos):
    gestor.add_edificio()

    with pytest.raises(IndexError):
        gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande'])
    
    with pytest.raises(IndexError):
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], None)

    gestor.add_aula_doble(0)
    with pytest.raises(IndexError):
        gestor.get_from_aula_doble(0, 0, 100)

def test_get_set_aula_doble_existente(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula(0)
    gestor.add_aula(0)
    gestor.add_aula(0)
    gestor.add_aula_doble(0)

    aulas: list[Aula] = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    gestor.set_in_aula_doble(0,0, campo_AulaDoble['aula_grande'], aulas[1])
    gestor.set_in_aula_doble(0,0, campo_AulaDoble['aula_chica_1'], aulas[2])
    gestor.set_in_aula_doble(0,0, campo_AulaDoble['aula_chica_2'], aulas[0])

    assert gestor.cantidad_de_edificios() == 1
    assert gestor.cantidad_de_aulas(0) == 3
    assert gestor.cantidad_de_aulas_dobles(0) == 1

    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande']) is aulas[1]
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_1']) is aulas[2]
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_2']) is aulas[0]

def test_ordenar_aulas_dobles(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'a')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'b')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 2, campo_Aula['nombre'], 'c')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 3, campo_Aula['nombre'], 'd')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 4, campo_Aula['nombre'], 'e')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 5, campo_Aula['nombre'], 'f')

    # Ordenar cuando no hay aulas dobles no debería tener ningún efecto:
    gestor.ordenar_aulas_dobles(0)
    assert gestor.get_from_aula(0, 0, campo_Aula['nombre']) == 'a'
    assert gestor.get_from_aula(0, 1, campo_Aula['nombre']) == 'b'
    assert gestor.get_from_aula(0, 2, campo_Aula['nombre']) == 'c'
    assert gestor.get_from_aula(0, 3, campo_Aula['nombre']) == 'd'
    assert gestor.get_from_aula(0, 4, campo_Aula['nombre']) == 'e'
    assert gestor.get_from_aula(0, 5, campo_Aula['nombre']) == 'f'

    # Ordenar cuando hay aulas dobles debería ordenar las aulas dobles y no
    # cambiar las aulas comunes:
    aulas: list[Aula] = gestor.get_from_edificio(0, campo_Edificio['aulas'])
    gestor.add_aula_doble(0)
    gestor.add_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[5])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[3])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[4])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_grande'], aulas[1])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_1'], aulas[2])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_2'], aulas[0])

    gestor.ordenar_aulas_dobles(0)
    assert gestor.get_from_aula(0, 0, campo_Aula['nombre']) == 'a'
    assert gestor.get_from_aula(0, 1, campo_Aula['nombre']) == 'b'
    assert gestor.get_from_aula(0, 2, campo_Aula['nombre']) == 'c'
    assert gestor.get_from_aula(0, 3, campo_Aula['nombre']) == 'd'
    assert gestor.get_from_aula(0, 4, campo_Aula['nombre']) == 'e'
    assert gestor.get_from_aula(0, 5, campo_Aula['nombre']) == 'f'

    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande'])  is aulas[1]
    assert gestor.get_from_aula_doble(0, 1, campo_AulaDoble['aula_grande'])  is aulas[5]

def test_borrar_aula_doble(gestor: GestorDeDatos):
    gestor.add_edificio()

    gestor.add_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'a')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'b')
    gestor.add_aula(0)
    gestor.set_in_aula(0, 2, campo_Aula['nombre'], 'c')

    aulas: list[Aula] = gestor.get_from_edificio(0, campo_Edificio['aulas'])
    gestor.add_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.add_aula_doble(0)
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_grande'], aulas[1])

    # Borrar aula doble que existe
    gestor.borrar_aula_doble(0, 1)
    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande']) is aulas[0]

    # Borrar aula doble que no existe
    with pytest.raises(IndexError):
        gestor.borrar_aula_doble(0, 2)
    with pytest.raises(IndexError):
        gestor.borrar_aula_doble(1, 0)

def test_borrar_aula_borra_aulas_dobles_que_usan_ese_aula(gestor: GestorDeDatos):
    gestor.add_edificio()
    for i in range(7):
        gestor.add_aula(0)
        gestor.set_in_aula(0, i, campo_Aula['nombre'], str(i))
    
    # Crear aulas dobles con el aula 0 en las tres posiciones:
    aulas: list[Aula] = gestor.get_from_edificio(0, campo_Edificio['aulas'])
    gestor.add_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])
    gestor.add_aula_doble(0)
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_grande'], aulas[3])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_1'], aulas[0])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_2'], aulas[4])
    gestor.add_aula_doble(0)
    gestor.set_in_aula_doble(0, 2, campo_AulaDoble['aula_grande'], aulas[5])
    gestor.set_in_aula_doble(0, 2, campo_AulaDoble['aula_chica_1'], aulas[6])
    gestor.set_in_aula_doble(0, 2, campo_AulaDoble['aula_chica_2'], aulas[0])

    # Y un aula doble que no tiene a la 0:
    gestor.add_aula_doble(0)
    gestor.set_in_aula_doble(0, 3, campo_AulaDoble['aula_grande'], aulas[4])
    gestor.set_in_aula_doble(0, 3, campo_AulaDoble['aula_chica_1'], aulas[6])
    gestor.set_in_aula_doble(0, 3, campo_AulaDoble['aula_chica_2'], aulas[2])

    # Borrar el aula 0 y ver que se borren las aulas dobles correspondientes:
    gestor.borrar_aula(0, 0)

    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande']) is not aulas[0]
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_1']) is not aulas[0]
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_2']) is not aulas[0]
