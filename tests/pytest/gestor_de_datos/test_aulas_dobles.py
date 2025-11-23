from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import HorariosSemanalesOpcionales, RangoHorario
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos, aula_no_seleccionada
from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificio

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay edificio, así que no se puede preguntar por las aulas:
    with pytest.raises(IndexError):
        gestor.cantidad_de_aulas_dobles(0)
    
    # Al agregar un edificio, no tiene ningún aula doble:
    gestor.agregar_edificio()
    assert gestor.cantidad_de_aulas_dobles(0) == 0

def test_agregar_aula_doble_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula_doble(0)

    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande']) is aula_no_seleccionada
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_1']) is aula_no_seleccionada
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_2']) is aula_no_seleccionada

def test_add_varias_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_edificio()
    for _ in range(3):
        gestor.agregar_aula_doble(1)
    
    assert gestor.cantidad_de_aulas_dobles(0) == 0
    assert gestor.cantidad_de_aulas_dobles(1) == 3

def test_get_set_fuera_de_rango(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    with pytest.raises(IndexError):
        gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande'])
    
    with pytest.raises(IndexError):
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], None)

    gestor.agregar_aula_doble(0)
    with pytest.raises(IndexError):
        gestor.get_from_aula_doble(0, 0, 100)

def test_get_set_aula_doble_existente(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.agregar_aula(0)
    gestor.agregar_aula(0)
    gestor.agregar_aula_doble(0)

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
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'a')
    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'b')
    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 2, campo_Aula['nombre'], 'c')
    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 3, campo_Aula['nombre'], 'd')
    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 4, campo_Aula['nombre'], 'e')
    gestor.agregar_aula(0)
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
    gestor.agregar_aula_doble(0)
    gestor.agregar_aula_doble(0)
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
    gestor.agregar_edificio()

    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 0, campo_Aula['nombre'], 'a')
    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 1, campo_Aula['nombre'], 'b')
    gestor.agregar_aula(0)
    gestor.set_in_aula(0, 2, campo_Aula['nombre'], 'c')

    aulas: list[Aula] = gestor.get_from_edificio(0, campo_Edificio['aulas'])
    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.agregar_aula_doble(0)
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
    gestor.agregar_edificio()
    for i in range(11):
        gestor.agregar_aula(0)
        gestor.set_in_aula(0, i, campo_Aula['nombre'], str(i))
    
    aulas: list[Aula] = list(gestor.get_from_edificio(0, campo_Edificio['aulas']))

    # Crear cuatro aulas dobles
    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])
    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_grande'], aulas[3])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_1'], aulas[4])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_2'], aulas[5])
    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 2, campo_AulaDoble['aula_grande'], aulas[6])
    gestor.set_in_aula_doble(0, 2, campo_AulaDoble['aula_chica_1'], aulas[7])
    gestor.set_in_aula_doble(0, 2, campo_AulaDoble['aula_chica_2'], aulas[8])
    gestor.agregar_aula_doble(0) # Esta queda con un par de aulas sin elegir
    gestor.set_in_aula_doble(0, 3, campo_AulaDoble['aula_chica_1'], aulas[9])
    
    assert gestor.cantidad_de_aulas_dobles(0) == 4

    # Borrar el aula 10 y ver que no se borre ningún aula doble
    gestor.borrar_aula(0, 10)
    assert gestor.cantidad_de_aulas_dobles(0) == 4

    # Borrar un aula que está siendo usada como aula grande
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande']).nombre == '0'
    gestor.borrar_aula(0, 0)
    assert gestor.cantidad_de_aulas_dobles(0) == 3
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_grande']).nombre == '3' # Se borró la que inicialmente era la primer aula doble

    # Borrar un aula que está siendo usada como aula chica 1
    assert gestor.get_from_aula_doble(0, -1, campo_AulaDoble['aula_chica_1']).nombre == '9'
    gestor.borrar_aula(0, 8)
    assert gestor.cantidad_de_aulas_dobles(0) == 2
    assert gestor.get_from_aula_doble(0, -1, campo_AulaDoble['aula_chica_1']).nombre == '7' # Se borró la que inicialmente era el último aula doble

    # Borrar un aula que está siendo usada como aula chica 2
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_2']).nombre == '5'
    gestor.borrar_aula(0, 4)
    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_from_aula_doble(0, 0, campo_AulaDoble['aula_chica_2']).nombre == '8' # Se borró la que inicialmente era la segunda aula doble

def test_setear_aulas_repetidas_en_la_misma_aula_doble(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    for i in range(3):
        gestor.agregar_aula(0)
        gestor.set_in_aula(0, i, campo_Aula['nombre'], f'aula{i}')
    aulas = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    # Valores iniciales sin repetir
    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])

    # Asignar una de las aulas chicas como aula grande
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[1])
    assert 'aula doble' in str(error)
    assert 'aula1' in str(error)
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[2])
    assert 'aula doble' in str(error)
    assert 'aula2' in str(error)

    # Asignar el aula grande a una de las chicas
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[0])
    assert 'aula doble' in str(error)
    assert 'aula0' in str(error)
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[0])
    assert 'aula doble' in str(error)
    assert 'aula0' in str(error)

    # Asignar las aulas chicas entre sí
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[2])
    assert 'aula doble' in str(error)
    assert 'aula2' in str(error)
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[1])
    assert 'aula doble' in str(error)
    assert 'aula1' in str(error)

    # ...Pero si asignás un aula a sí misma está todo bien
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])

def test_setear_aulas_repetidas_en_la_distintas_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    for i in range(6):
        gestor.agregar_aula(0)
        gestor.set_in_aula(0, i, campo_Aula['nombre'], f'aula{i}')
    aulas = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    # Valores iniciales sin repetir
    gestor.agregar_aula_doble(0)
    gestor.agregar_aula_doble(0)
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[0])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_1'], aulas[1])
    gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_chica_2'], aulas[2])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_grande'], aulas[3])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_1'], aulas[4])
    gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_chica_2'], aulas[5])

    # Asignar el aula grande de un aula doble a otra aula doble
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[3])
    assert 'aula doble' in str(error)
    assert 'aula3' in str(error)

    # Asignar el aula chica 1 de un aula doble a otra aula doble
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 1, campo_AulaDoble['aula_grande'], aulas[1])
    assert 'aula doble' in str(error)
    assert 'aula1' in str(error)

    # Asignar el aula chica 2 de un aula doble a otra aula doble
    with pytest.raises(ValueError) as error:
        gestor.set_in_aula_doble(0, 0, campo_AulaDoble['aula_grande'], aulas[5])
    assert 'aula doble' in str(error)
    assert 'aula5' in str(error)
