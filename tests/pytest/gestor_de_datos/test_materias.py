import pytest

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Carrera

from conftest import campo_Materia

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay carreras, así que no se puede preguntar por las materias:
    with pytest.raises(IndexError):
        gestor.cantidad_de_materias(0)
    
    # Al agregar una carrera, no tiene ninguna materia:
    gestor.add_carrera()
    assert gestor.cantidad_de_materias(0) == 0

def test_add_materia_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.add_carrera()
    gestor.add_materia(0)

    assert gestor.cantidad_de_materias(0) == 1
    assert 'sin nombre' in gestor.get_from_materia(0, 0, campo_Materia['nombre'])
    assert isinstance(gestor.get_from_materia(0, 0, campo_Materia['carrera']), Carrera)
    assert gestor.get_from_materia(0, 0, campo_Materia['año']) >= 0
    assert gestor.get_from_materia(0, 0, campo_Materia['clases']) == []
    assert gestor.get_from_materia(0, 0, campo_Materia['cuatrimestral_o_anual']) == None

    # Segunda materia pertenece a la misma carrera:
    gestor.add_materia(0)
    assert gestor.get_from_materia(0, 0, campo_Materia['carrera']) is gestor.get_from_materia(0, 1, campo_Materia['carrera'])

def test_add_varias_materias(gestor: GestorDeDatos):
    '''
    Probar que si se agregan varias materias, todas se agregan con nombres
    distintos y todas dicen 'sin nombre'.
    '''
    gestor.add_carrera()
    gestor.add_carrera()
    for _ in range(10):
        gestor.add_materia(0)
    for _ in range(4):
        gestor.add_materia(1)
    
    assert gestor.cantidad_de_materias(0) == 10
    assert gestor.cantidad_de_materias(1) == 4

    nombres0 = [gestor.get_from_materia(0, i, campo_Materia['nombre']) for i in range(10)]
    assert all('sin nombre' in nombre for nombre in nombres0)
    assert len(nombres0) == len(set(nombres0)) # No hay repetidos

    nombres1 = [gestor.get_from_materia(1, i, campo_Materia['nombre']) for i in range(4)]
    assert all('sin nombre' in nombre for nombre in nombres1)
    assert len(nombres1) == len(set(nombres1)) # No hay repetidos

    # Chequear que se crearon dos carreras
    assert gestor.get_from_materia(0, 0, campo_Materia['carrera']) is not gestor.get_from_materia(1, 0, campo_Materia['carrera'])

def test_materia_existe_o_no(gestor: GestorDeDatos):
    gestor.add_carrera()

    # Al principio no existe
    assert not gestor.existe_materia(0, 'pepito')

    # Al agregar una materia sin nombre sigue sin existir
    gestor.add_materia(0)
    assert not gestor.existe_materia(0, 'pepito')

    # Al agregar una materia con otro nombre sigue sin existir
    gestor.set_in_materia(0, 0, campo_Materia['nombre'], 'pepe')
    assert not gestor.existe_materia(0, 'pepito')

    # Al agregar una materia con ese nombre sí existe
    gestor.add_materia(0)
    gestor.set_in_materia(0, 1, campo_Materia['nombre'], 'pepito')
    assert gestor.existe_materia(0, 'pepito')

def test_get_set_fuera_de_rango(gestor: GestorDeDatos):
    gestor.add_carrera()

    with pytest.raises(IndexError):
        gestor.get_from_materia(0, 0, campo_Materia['año'])
    
    with pytest.raises(IndexError):
        gestor.set_in_materia(0, 0, campo_Materia['año'], 0)

    gestor.add_materia(0)
    with pytest.raises(IndexError):
        gestor.get_from_materia(0, 0, 100)
    with pytest.raises(IndexError):
        gestor.set_in_materia(0, 0, 100, None)

def test_get_set_materia_existente(gestor: GestorDeDatos):
    nombre = 'nombresito'
    año = 15
    cuatrimestral_o_anual = 'qué sé yo'

    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.set_in_materia(0,0, campo_Materia['nombre'], nombre)
    gestor.set_in_materia(0,0, campo_Materia['año'], año)
    gestor.set_in_materia(0,0, campo_Materia['cuatrimestral_o_anual'], cuatrimestral_o_anual)

    assert len(gestor.get_carreras()) == 1
    assert gestor.cantidad_de_materias(0) == 1

    assert gestor.get_from_materia(0,0, campo_Materia['nombre']) == nombre
    assert gestor.get_from_materia(0,0, campo_Materia['año']) == año
    assert gestor.get_from_materia(0,0, campo_Materia['cuatrimestral_o_anual']) == cuatrimestral_o_anual

def test_ordenar_materias(gestor: GestorDeDatos):
    gestor.add_carrera()

    # Ordenar cuando no hay materias no debería tener ningún efecto:
    gestor.ordenar_materias(0)

    # Ordenar cuando hay materias debería ordenar las materias:
    gestor.add_materia(0)
    gestor.set_in_materia(0, 0, campo_Materia['nombre'], 'b')
    gestor.add_materia(0)
    gestor.set_in_materia(0, 1, campo_Materia['nombre'], 'a')
    gestor.add_materia(0)
    gestor.set_in_materia(0, 2, campo_Materia['nombre'], 'd')

    assert gestor.get_from_materia(0, 0, campo_Materia['nombre']) == 'b'
    assert gestor.get_from_materia(0, 1, campo_Materia['nombre']) == 'a'
    assert gestor.get_from_materia(0, 2, campo_Materia['nombre']) == 'd'

    gestor.ordenar_materias(0)
    assert gestor.get_from_materia(0, 0, campo_Materia['nombre']) == 'a'
    assert gestor.get_from_materia(0, 1, campo_Materia['nombre']) == 'b'
    assert gestor.get_from_materia(0, 2, campo_Materia['nombre']) == 'd'

def test_borrar_materia(gestor: GestorDeDatos):
    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.set_in_materia(0, 0, campo_Materia['nombre'], 'a')
    gestor.add_materia(0)
    gestor.set_in_materia(0, 1, campo_Materia['nombre'], 'b')
    gestor.add_materia(0)
    gestor.set_in_materia(0, 2, campo_Materia['nombre'], 'c')

    # Borrar materia que existe
    gestor.borrar_materia(0, 1)
    assert gestor.cantidad_de_materias(0) == 2
    assert gestor.get_from_materia(0, 0, campo_Materia['nombre']) == 'a'
    assert gestor.get_from_materia(0, 1, campo_Materia['nombre']) == 'c'

    # Borrar aula que no existe
    with pytest.raises(IndexError):
        gestor.borrar_materia(0, 2)
    with pytest.raises(IndexError):
        gestor.borrar_materia(1, 0)