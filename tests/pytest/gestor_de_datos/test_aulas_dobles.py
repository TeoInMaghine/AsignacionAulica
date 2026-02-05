import pytest

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos, aula_no_seleccionada
from asignacion_aulica.gestor_de_datos.entidades import Aula

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay edificio, así que no se puede preguntar por las aulas:
    with pytest.raises(IndexError):
        gestor.cantidad_de_aulas_dobles(0)
    
    # Al agregar un edificio, no tiene ningún aula doble:
    gestor.agregar_edificio()
    assert gestor.cantidad_de_aulas_dobles(0) == 0

def test_agregar_aula_doble_genera_valores_default(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula_doble(0)

    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_aula_doble(0, 0).aula_grande == aula_no_seleccionada
    assert gestor.get_aula_doble(0, 0).aula_chica_1 == aula_no_seleccionada
    assert gestor.get_aula_doble(0, 0).aula_chica_2 == aula_no_seleccionada

def test_add_varias_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_edificio()
    for _ in range(3):
        gestor.agregar_aula_doble(1)
    
    assert gestor.cantidad_de_aulas_dobles(0) == 0
    assert gestor.cantidad_de_aulas_dobles(1) == 3

def test_get_fuera_de_rango(gestor: GestorDeDatos):
    with pytest.raises(IndexError):
        gestor.get_aula_doble(0, 0)

    gestor.agregar_edificio()

    with pytest.raises(IndexError):
        gestor.get_aula_doble(0, 0)

def test_ordenar_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.get_aula(0, 0).nombre = 'a'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 1).nombre = 'b'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 2).nombre = 'c'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 3).nombre = 'd'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 4).nombre = 'e'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 5).nombre = 'f'

    # Ordenar cuando no hay aulas dobles no debería tener ningún efecto:
    gestor.ordenar_aulas_dobles(0)
    assert gestor.get_aula(0, 0).nombre == 'a'
    assert gestor.get_aula(0, 1).nombre == 'b'
    assert gestor.get_aula(0, 2).nombre == 'c'
    assert gestor.get_aula(0, 3).nombre == 'd'
    assert gestor.get_aula(0, 4).nombre == 'e'
    assert gestor.get_aula(0, 5).nombre == 'f'

    # Ordenar cuando hay aulas dobles debería ordenar las aulas dobles y no
    # cambiar las aulas comunes:
    aulas: list[Aula] = gestor.get_edificio(0).aulas
    gestor.agregar_aula_doble(0)
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[5]
    gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[3]
    gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[4]
    gestor.get_aula_doble(0, 1).aula_grande = aulas[1]
    gestor.get_aula_doble(0, 1).aula_chica_1 = aulas[2]
    gestor.get_aula_doble(0, 1).aula_chica_2 = aulas[0]

    gestor.ordenar_aulas_dobles(0)
    assert gestor.get_aula(0, 0).nombre == 'a'
    assert gestor.get_aula(0, 1).nombre == 'b'
    assert gestor.get_aula(0, 2).nombre == 'c'
    assert gestor.get_aula(0, 3).nombre == 'd'
    assert gestor.get_aula(0, 4).nombre == 'e'
    assert gestor.get_aula(0, 5).nombre == 'f'

    assert gestor.get_aula_doble(0, 0).aula_grande  is aulas[1]
    assert gestor.get_aula_doble(0, 1).aula_grande  is aulas[5]

def test_borrar_aula_doble(gestor: GestorDeDatos):
    gestor.agregar_edificio()

    gestor.agregar_aula(0)
    gestor.get_aula(0, 0).nombre = 'a'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 1).nombre = 'b'
    gestor.agregar_aula(0)
    gestor.get_aula(0, 2).nombre = 'c'

    aulas: list[Aula] = gestor.get_edificio(0).aulas
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 1).aula_grande = aulas[1]

    # Borrar aula doble que existe
    gestor.borrar_aula_doble(0, 1)
    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_aula_doble(0, 0).aula_grande is aulas[0]

    # Borrar aula doble que no existe
    with pytest.raises(IndexError):
        gestor.borrar_aula_doble(0, 2)
    with pytest.raises(IndexError):
        gestor.borrar_aula_doble(1, 0)

def test_borrar_aula_borra_aulas_dobles_que_usan_ese_aula(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    for i in range(11):
        gestor.agregar_aula(0)
        gestor.get_aula(0, i).nombre = str(i)
    
    aulas: list[Aula] = list(gestor.get_edificio(0).aulas)

    # Crear cuatro aulas dobles
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = aulas[0]
    gestor.get_aula_doble(0, 0).aula_chica_1 = aulas[1]
    gestor.get_aula_doble(0, 0).aula_chica_2 = aulas[2]
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 1).aula_grande = aulas[3]
    gestor.get_aula_doble(0, 1).aula_chica_1 = aulas[4]
    gestor.get_aula_doble(0, 1).aula_chica_2 = aulas[5]
    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 2).aula_grande = aulas[6]
    gestor.get_aula_doble(0, 2).aula_chica_1 = aulas[7]
    gestor.get_aula_doble(0, 2).aula_chica_2 = aulas[8]
    gestor.agregar_aula_doble(0) # Esta queda con un par de aulas sin elegir
    gestor.get_aula_doble(0, 3).aula_chica_1 = aulas[9]
    
    assert gestor.cantidad_de_aulas_dobles(0) == 4

    # Borrar el aula 10 y ver que no se borre ningún aula doble
    gestor.borrar_aula(0, 10)
    assert gestor.cantidad_de_aulas_dobles(0) == 4

    # Borrar un aula que está siendo usada como aula grande
    assert gestor.get_aula_doble(0, 0).aula_grande.nombre == '0'
    gestor.borrar_aula(0, 0)
    assert gestor.cantidad_de_aulas_dobles(0) == 3
    assert gestor.get_aula_doble(0, 0).aula_grande.nombre == '3' # Se borró la que inicialmente era la primer aula doble

    # Borrar un aula que está siendo usada como aula chica 1
    assert gestor.get_aula_doble(0, -1).aula_chica_1.nombre == '9'
    gestor.borrar_aula(0, 8)
    assert gestor.cantidad_de_aulas_dobles(0) == 2
    assert gestor.get_aula_doble(0, -1).aula_chica_1.nombre == '7' # Se borró la que inicialmente era el último aula doble

    # Borrar un aula que está siendo usada como aula chica 2
    assert gestor.get_aula_doble(0, 0).aula_chica_2.nombre == '5'
    gestor.borrar_aula(0, 4)
    assert gestor.cantidad_de_aulas_dobles(0) == 1
    assert gestor.get_aula_doble(0, 0).aula_chica_2.nombre == '8' # Se borró la que inicialmente era la segunda aula doble

def test_existe_o_no_aula_en_aulas_dobles(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_edificio()

    for i in range(4):
        gestor.agregar_aula(0)
        gestor.agregar_aula(1)
        gestor.get_aula(0, i).nombre = f'aula{i}'
        gestor.get_aula(1, i).nombre = f'aula{i}'

    gestor.agregar_aula_doble(0)
    gestor.get_aula_doble(0, 0).aula_grande = gestor.get_aula(0, 0)
    gestor.get_aula_doble(0, 0).aula_chica_1 = gestor.get_aula(0, 1)
    gestor.get_aula_doble(0, 0).aula_chica_2 = gestor.get_aula(0, 2)

    gestor.agregar_aula_doble(1)
    gestor.get_aula_doble(1, 0).aula_grande = gestor.get_aula(1, 1)
    gestor.get_aula_doble(1, 0).aula_chica_1 = gestor.get_aula(1, 2)
    gestor.get_aula_doble(1, 0).aula_chica_2 = gestor.get_aula(1, 3)

    assert gestor.existe_aula_en_aulas_dobles(0, 0)
    assert gestor.existe_aula_en_aulas_dobles(0, 1)
    assert gestor.existe_aula_en_aulas_dobles(0, 2)
    assert not gestor.existe_aula_en_aulas_dobles(0, 3)

    assert gestor.existe_aula_en_aulas_dobles(1, 1)
    assert gestor.existe_aula_en_aulas_dobles(1, 2)
    assert gestor.existe_aula_en_aulas_dobles(1, 3)
    assert not gestor.existe_aula_en_aulas_dobles(1, 0)
