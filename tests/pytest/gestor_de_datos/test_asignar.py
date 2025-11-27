from datetime import time
from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día, crear_horarios_semanales_opcionales
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

from conftest import campo_Aula, campo_Clase

def test_asignar(gestor: GestorDeDatos):
    '''
    La asignación se prueba en detalle en el módulo lógica_de_asignación. Acá
    solamente verificamos que se esté completando el circuito.
    '''
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    horarios_aula = crear_horarios_semanales_opcionales()
    horarios_aula[Día.Lunes] = RangoHorario(time(9), time(12))
    gestor.set_in_aula(0, 0, campo_Aula['horarios'], horarios_aula)

    gestor.agregar_carrera('0')
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    gestor.set_in_clase(0, 0, 0, campo_Clase['día'], Día.Lunes)
    gestor.set_in_clase(0, 0, 0, campo_Clase['horario'], RangoHorario(time(10), time(11)))

    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) is None

    info = gestor.asignar_aulas()

    assert info.todo_ok()
    assert gestor.get_from_clase(0, 0, 0, campo_Clase['aula_asignada']) is not None
