import pytest

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Carrera

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay carreras, así que no se puede preguntar por las materias:
    with pytest.raises(IndexError):
        gestor.cantidad_de_materias(0)
    
    # Al agregar una carrera, no tiene ninguna materia:
    gestor.agregar_carrera()
    assert gestor.cantidad_de_materias(0) == 0

def test_agregar_materia_genera_valores_default(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)

    assert gestor.cantidad_de_materias(0) == 1
    assert isinstance(gestor.get_materia(0, 0).nombre, str)
    assert isinstance(gestor.get_materia(0, 0).carrera, Carrera)
    assert gestor.get_materia(0, 0).año >= 0
    assert gestor.get_materia(0, 0).clases == []
    assert isinstance(gestor.get_materia(0, 0).cuatrimestral_o_anual, str)

    # Segunda materia pertenece a la misma carrera:
    gestor.agregar_materia(0)
    assert gestor.get_materia(0, 0).carrera is gestor.get_materia(0, 1).carrera

def test_add_varias_materias(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varias materias, todas se agregan con nombres
    distintos.
    '''
    gestor.agregar_carrera()
    gestor.agregar_carrera()
    for _ in range(10):
        gestor.agregar_materia(0)
    for _ in range(4):
        gestor.agregar_materia(1)
    
    assert gestor.cantidad_de_materias(0) == 10
    assert gestor.cantidad_de_materias(1) == 4

    nombres0 = [gestor.get_materia(0, i).nombre for i in range(10)]
    assert all(isinstance(nombre, str) for nombre in nombres0)
    assert len(nombres0) == len(set(nombres0)) # No hay repetidos

    nombres1 = [gestor.get_materia(1, i).nombre for i in range(4)]
    assert all(isinstance(nombre, str) for nombre in nombres1)
    assert len(nombres1) == len(set(nombres1)) # No hay repetidos

    # Chequear que se crearon dos carreras
    assert gestor.get_materia(0, 0).carrera is not gestor.get_materia(1, 0).carrera

def test_materia_existe_o_no(gestor: GestorDeDatos):
    gestor.agregar_carrera()

    # Al principio no existe
    assert not gestor.existe_materia(0, 'pepito')

    # Al agregar una materia sin nombre sigue sin existir
    gestor.agregar_materia(0)
    assert not gestor.existe_materia(0, 'pepito')

    # Al agregar una materia con otro nombre sigue sin existir
    gestor.get_materia(0, 0).nombre = 'pepe'
    assert not gestor.existe_materia(0, 'pepito')

    # Al agregar una materia con ese nombre sí existe
    gestor.agregar_materia(0)
    gestor.get_materia(0, 1).nombre = 'pepito'
    assert gestor.existe_materia(0, 'pepito')

def test_get_fuera_de_rango(gestor: GestorDeDatos):
    with pytest.raises(IndexError):
        gestor.get_materia(0, 0)

    gestor.agregar_carrera()

    with pytest.raises(IndexError):
        gestor.get_materia(0, 0)

def test_ordenar_materias(gestor: GestorDeDatos):
    gestor.agregar_carrera()

    # Ordenar cuando no hay materias no debería tener ningún efecto:
    gestor.ordenar_materias(0)

    # Ordenar cuando hay materias debería ordenar las materias:
    gestor.agregar_materia(0)
    gestor.get_materia(0, 0).nombre = 'b'
    gestor.agregar_materia(0)
    gestor.get_materia(0, 1).nombre = 'a'
    gestor.agregar_materia(0)
    gestor.get_materia(0, 2).nombre = 'd'

    assert gestor.get_materia(0, 0).nombre == 'b'
    assert gestor.get_materia(0, 1).nombre == 'a'
    assert gestor.get_materia(0, 2).nombre == 'd'

    gestor.ordenar_materias(0)
    assert gestor.get_materia(0, 0).nombre == 'a'
    assert gestor.get_materia(0, 1).nombre == 'b'
    assert gestor.get_materia(0, 2).nombre == 'd'

def test_borrar_materia(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.get_materia(0, 0).nombre = 'a'
    gestor.agregar_materia(0)
    gestor.get_materia(0, 1).nombre = 'b'
    gestor.agregar_materia(0)
    gestor.get_materia(0, 2).nombre = 'c'

    # Borrar materia que existe
    gestor.borrar_materia(0, 1)
    assert gestor.cantidad_de_materias(0) == 2
    assert gestor.get_materia(0, 0).nombre == 'a'
    assert gestor.get_materia(0, 1).nombre == 'c'

    # Borrar aula que no existe
    with pytest.raises(IndexError):
        gestor.borrar_materia(0, 2)
    with pytest.raises(IndexError):
        gestor.borrar_materia(1, 0)
