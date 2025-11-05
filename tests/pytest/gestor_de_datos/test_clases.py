from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import HorariosSemanalesOpcionales, RangoHorario, Día
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Edificio, Materia

from conftest import campo_Clase, campo_Edificio, campo_Aula

def test_empieza_estando_todo_vacío(gestor: GestorDeDatos):
    # Al principio no hay carrera ni materia, así que no se puede preguntar por
    # las clases:
    with pytest.raises(IndexError):
        gestor.cantidad_de_clases(0, 0)
    
    gestor.add_carrera()
    with pytest.raises(IndexError):
        gestor.cantidad_de_clases(0, 0)
    
    # Al agregar una materia, no tiene ningún aula:
    gestor.add_materia(0)
    assert gestor.cantidad_de_clases(0, 0) == 0

def test_add_clase_genera_valores_deafult(gestor: GestorDeDatos):
    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.add_clase(0, 0)

    assert gestor.cantidad_de_clases(0, 0) == 1

    assert isinstance(gestor.get_from_clase(0, 0, 0, campo_Clase['materia']), Materia)
    assert isinstance(gestor.get_from_clase(0, 0, 0, campo_Clase['día']), Día)
    assert isinstance(gestor.get_from_clase(0, 0, 0, campo_Clase['horario']), RangoHorario)
    assert isinstance(gestor.get_from_clase(0, 0, 0, campo_Clase['virtual']), bool)
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['cantidad_de_alumnos']) >= 0
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['equipamiento_necesario']) == set()
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) is None
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['no_cambiar_asignación']) == False
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['comisión']) is None
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['teórica_o_práctica']) is None
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['promocionable']) is None
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['docente']) is None
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['auxiliar']) is None

    # Segunda clase pertenece a la misma materia:
    gestor.add_clase(0, 0)
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['materia']) is gestor.get_from_clase(0, 0, 1, campo_Clase['materia'])

    # Clase en otra materia no pertenece a la misma materia:
    gestor.add_materia(0)
    gestor.add_clase(0, 1)
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['materia']) is not  gestor.get_from_clase(0, 1, 0, campo_Clase['materia'])


def test_add_varias_clases(gestor: GestorDeDatos):
    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.add_materia(0)
    for _ in range(10):
        gestor.add_clase(0, 0)
    for _ in range(4):
        gestor.add_clase(0, 1)
    
    assert gestor.cantidad_de_clases(0, 0) == 10
    assert gestor.cantidad_de_clases(0, 1) == 4

def test_get_set_fuera_de_rango(gestor: GestorDeDatos):
    gestor.add_carrera()
    gestor.add_materia(0)

    with pytest.raises(IndexError):
        gestor.get_from_clase(0, 0, 0, campo_Clase['horario'])
    
    with pytest.raises(IndexError):
        gestor.set_in_clase(0, 0, 0, campo_Clase['virtual'], True)
    
    gestor.add_clase(0, 0)
    with pytest.raises(IndexError):
        gestor.set_in_clase(0, 0, 0, 100, None)

def test_get_set_clase_existente(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula(0)

    día = Día.Martes
    horario = RangoHorario(time(5), time(20))
    virutal = False
    cantidad_de_alumnos = 69
    equipamiento_necesario = {'4', '20'}
    aula_asignada = gestor.get_from_edificio(0, campo_Edificio['aulas'])[0]
    no_cambiar_asignación = True
    comisión = 'aaaaaaagh'
    teórica_o_práctica = 'las dos'
    promicionable = 'ponele'
    docente = 'nadie'
    auxiliar = 'auxilioo!'

    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.add_clase(0, 0)

    gestor.set_in_clase(0, 0, 0, campo_Clase['día'], día)
    gestor.set_in_clase(0, 0, 0, campo_Clase['horario'], horario)
    gestor.set_in_clase(0, 0, 0, campo_Clase['virtual'], virutal)
    gestor.set_in_clase(0, 0, 0, campo_Clase['cantidad_de_alumnos'], cantidad_de_alumnos)
    gestor.set_in_clase(0, 0, 0, campo_Clase['equipamiento_necesario'], equipamiento_necesario)
    gestor.set_in_clase(0, 0, 0, campo_Clase['aula_asignada'], aula_asignada)
    gestor.set_in_clase(0, 0, 0, campo_Clase['no_cambiar_asignación'], no_cambiar_asignación)
    gestor.set_in_clase(0, 0, 0, campo_Clase['comisión'], comisión)
    gestor.set_in_clase(0, 0, 0, campo_Clase['teórica_o_práctica'], teórica_o_práctica)
    gestor.set_in_clase(0, 0, 0, campo_Clase['promocionable'], promicionable)
    gestor.set_in_clase(0, 0, 0, campo_Clase['docente'], docente)
    gestor.set_in_clase(0, 0, 0, campo_Clase['auxiliar'], auxiliar)

    assert gestor.cantidad_de_clases(0, 0) == 1

    assert gestor.get_from_clase(0, 0, 0, campo_Clase['materia']) is gestor.get_carrera(0).materias[0]
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['día']) == día
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['horario']) == horario
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['virtual']) == virutal
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['cantidad_de_alumnos']) == cantidad_de_alumnos
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['equipamiento_necesario']) == equipamiento_necesario
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) == aula_asignada
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['no_cambiar_asignación']) == no_cambiar_asignación
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['comisión']) == comisión
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['teórica_o_práctica']) == teórica_o_práctica
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['promocionable']) == promicionable
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['docente']) == docente
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['auxiliar']) == auxiliar

def test_borrar_clase(gestor: GestorDeDatos):
    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.add_clase(0, 0)
    gestor.set_in_clase(0, 0, 0, campo_Clase['día'], Día.Lunes)
    gestor.add_clase(0, 0)
    gestor.set_in_clase(0, 0, 1, campo_Clase['día'], Día.Martes)
    gestor.add_clase(0, 0)
    gestor.set_in_clase(0, 0, 2, campo_Clase['día'], Día.Miércoles)

    # Borrar clase que existe
    gestor.borrar_clase(0, 0, 1)
    assert gestor.cantidad_de_clases(0, 0) == 2
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['día']) == Día.Lunes
    assert gestor.get_from_clase(0, 0, 1, campo_Clase['día']) == Día.Miércoles

    # Borrar aula que no existe
    with pytest.raises(IndexError):
        gestor.borrar_clase(0, 0,  2)
    with pytest.raises(IndexError):
        gestor.borrar_clase(0, 1,  0)
    with pytest.raises(IndexError):
        gestor.borrar_clase(1, 0,  0)

def test_borrar_aula_borra_asignación_de_clases_que_tenían_ese_aula(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_aula(0)
    gestor.add_aula(0)
    aula0, aula1 = gestor.get_from_edificio(0, campo_Edificio['aulas'])

    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.add_clase(0, 0)
    gestor.add_clase(0, 0)
    gestor.add_clase(0, 0)
    gestor.add_clase(0, 0)

    gestor.set_in_clase(0, 0, 0, campo_Clase['aula_asignada'], aula1)
    gestor.set_in_clase(0, 0, 1, campo_Clase['aula_asignada'], aula0)
    gestor.set_in_clase(0, 0, 2, campo_Clase['aula_asignada'], aula1)

    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) is aula1
    assert gestor.get_from_clase(0, 0, 1, campo_Clase['aula_asignada']) is aula0
    assert gestor.get_from_clase(0, 0, 2, campo_Clase['aula_asignada']) is aula1
    assert gestor.get_from_clase(0, 0, 3, campo_Clase['aula_asignada']) is None

    gestor.borrar_aula(0, 1)

    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) is None
    assert gestor.get_from_clase(0, 0, 1, campo_Clase['aula_asignada']) is aula0
    assert gestor.get_from_clase(0, 0, 2, campo_Clase['aula_asignada']) is None
    assert gestor.get_from_clase(0, 0, 3, campo_Clase['aula_asignada']) is None

def test_borrar_edificio_borra_asignación_de_clases_que_tenían_aula_en_ese_edificio(gestor: GestorDeDatos):
    gestor.add_edificio()
    gestor.add_edificio()
    gestor.add_aula(0)
    gestor.add_aula(1)
    aula0 = gestor.get_from_edificio(0, campo_Edificio['aulas'])[0]
    aula1 = gestor.get_from_edificio(1, campo_Edificio['aulas'])[0]

    gestor.add_carrera()
    gestor.add_materia(0)
    gestor.add_clase(0, 0)
    gestor.add_clase(0, 0)
    gestor.add_clase(0, 0)
    gestor.add_clase(0, 0)

    gestor.set_in_clase(0, 0, 0, campo_Clase['aula_asignada'], aula1)
    gestor.set_in_clase(0, 0, 1, campo_Clase['aula_asignada'], aula0)
    gestor.set_in_clase(0, 0, 2, campo_Clase['aula_asignada'], aula1)

    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) is aula1
    assert gestor.get_from_clase(0, 0, 1, campo_Clase['aula_asignada']) is aula0
    assert gestor.get_from_clase(0, 0, 2, campo_Clase['aula_asignada']) is aula1
    assert gestor.get_from_clase(0, 0, 3, campo_Clase['aula_asignada']) is None

    gestor.borrar_edificio(1)

    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) is None
    assert gestor.get_from_clase(0, 0, 1, campo_Clase['aula_asignada']) is aula0
    assert gestor.get_from_clase(0, 0, 2, campo_Clase['aula_asignada']) is None
    assert gestor.get_from_clase(0, 0, 3, campo_Clase['aula_asignada']) is None
