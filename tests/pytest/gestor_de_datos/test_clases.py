import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Materia, Clase

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay carrera ni materia, así que no se puede preguntar por
    # las clases:
    with pytest.raises(IndexError):
        gestor.cantidad_de_clases(0, 0)
    
    gestor.agregar_carrera()
    with pytest.raises(IndexError):
        gestor.cantidad_de_clases(0, 0)
    
    # Al agregar una materia, no tiene ningún aula:
    gestor.agregar_materia(0)
    assert gestor.cantidad_de_clases(0, 0) == 0

def test_agregar_clase_genera_valores_default(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)

    assert gestor.cantidad_de_clases(0, 0) == 1

    clase_1: Clase = gestor.get_clase(0, 0, 0)
    assert isinstance(clase_1.materia, Materia)
    assert isinstance(clase_1.día, Día)
    assert isinstance(clase_1.horario, RangoHorario)
    assert isinstance(clase_1.virtual, bool)
    assert clase_1.cantidad_de_alumnos >= 0
    assert clase_1.equipamiento_necesario == set()
    assert clase_1.aula_asignada is None
    assert clase_1.no_cambiar_asignación == False
    assert isinstance(clase_1.comisión, str)
    assert isinstance(clase_1.teórica_o_práctica, str)
    assert isinstance(clase_1.promocionable, str)
    assert isinstance(clase_1.docente, str)
    assert isinstance(clase_1.auxiliar, str)

    # Segunda clase pertenece a la misma materia:
    gestor.agregar_clase(0, 0)
    clase_2: Clase = gestor.get_clase(0, 0, 1)
    assert clase_1.materia is clase_2.materia

    # Clase en otra materia no pertenece a la misma materia:
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 1)
    clase_3: Clase = gestor.get_clase(0, 1, 0)
    assert clase_1.materia is not clase_3.materia


def test_add_varias_clases(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_materia(0)
    for _ in range(10):
        gestor.agregar_clase(0, 0)
    for _ in range(4):
        gestor.agregar_clase(0, 1)
    
    assert gestor.cantidad_de_clases(0, 0) == 10
    assert gestor.cantidad_de_clases(0, 1) == 4

def test_get_fuera_de_rango(gestor: GestorDeDatos):
    with pytest.raises(IndexError):
        gestor.get_clase(0, 0, 0)

    gestor.agregar_carrera()

    with pytest.raises(IndexError):
        gestor.get_clase(0, 0, 0)

    gestor.agregar_materia(0)

    with pytest.raises(IndexError):
        gestor.get_clase(0, 0, 0)

def test_borrar_clase(gestor: GestorDeDatos):
    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    gestor.get_clase(0, 0, 0).día = Día.Lunes
    gestor.agregar_clase(0, 0)
    gestor.get_clase(0, 0, 1).día = Día.Martes
    gestor.agregar_clase(0, 0)
    gestor.get_clase(0, 0, 2).día = Día.Miércoles

    # Borrar clase que existe
    gestor.borrar_clase(0, 0, 1)
    assert gestor.cantidad_de_clases(0, 0) == 2
    assert gestor.get_clase(0, 0, 0).día == Día.Lunes
    assert gestor.get_clase(0, 0, 1).día == Día.Miércoles

    # Borrar clase que no existe
    with pytest.raises(IndexError):
        gestor.borrar_clase(0, 0,  2)
    with pytest.raises(IndexError):
        gestor.borrar_clase(0, 1,  0)
    with pytest.raises(IndexError):
        gestor.borrar_clase(1, 0,  0)

def test_borrar_aula_borra_asignación_de_clases_que_tenían_ese_aula(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.agregar_aula(0)
    aula0, aula1 = gestor.get_edificio(0).aulas

    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_clase(0, 0)

    gestor.get_clase(0, 0, 0).aula_asignada = aula1
    gestor.get_clase(0, 0, 1).aula_asignada = aula0
    gestor.get_clase(0, 0, 2).aula_asignada = aula1

    assert gestor.get_clase(0, 0, 0).aula_asignada is aula1
    assert gestor.get_clase(0, 0, 1).aula_asignada is aula0
    assert gestor.get_clase(0, 0, 2).aula_asignada is aula1
    assert gestor.get_clase(0, 0, 3).aula_asignada is None

    gestor.borrar_aula(0, 1)

    assert gestor.get_clase(0, 0, 0).aula_asignada is None
    assert gestor.get_clase(0, 0, 1).aula_asignada is aula0
    assert gestor.get_clase(0, 0, 2).aula_asignada is None
    assert gestor.get_clase(0, 0, 3).aula_asignada is None

def test_borrar_edificio_borra_asignación_de_clases_que_tenían_aula_en_ese_edificio(gestor: GestorDeDatos):
    gestor.agregar_edificio()
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    gestor.agregar_aula(1)
    aula0 = gestor.get_edificio(0).aulas[0]
    aula1 = gestor.get_edificio(1).aulas[0]

    gestor.agregar_carrera()
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_clase(0, 0)
    gestor.agregar_clase(0, 0)

    gestor.get_clase(0, 0, 0).aula_asignada = aula1
    gestor.get_clase(0, 0, 1).aula_asignada = aula0
    gestor.get_clase(0, 0, 2).aula_asignada = aula1

    assert gestor.get_clase(0, 0, 0).aula_asignada is aula1
    assert gestor.get_clase(0, 0, 1).aula_asignada is aula0
    assert gestor.get_clase(0, 0, 2).aula_asignada is aula1
    assert gestor.get_clase(0, 0, 3).aula_asignada is None

    gestor.borrar_edificio(1)

    assert gestor.get_clase(0, 0, 0).aula_asignada is None
    assert gestor.get_clase(0, 0, 1).aula_asignada is aula0
    assert gestor.get_clase(0, 0, 2).aula_asignada is None
    assert gestor.get_clase(0, 0, 3).aula_asignada is None
