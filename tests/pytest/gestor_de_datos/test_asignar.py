from datetime import time
from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día, crear_horarios_semanales_opcionales
from asignacion_aulica.gestor_de_datos.entidades import Aula, Clase
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

def test_asignar(gestor: GestorDeDatos):
    '''
    La asignación se prueba en detalle en el módulo lógica_de_asignación. Acá
    solamente verificamos que se esté completando el circuito.
    '''
    gestor.agregar_edificio()
    gestor.agregar_aula(0)
    horarios_aula = crear_horarios_semanales_opcionales()
    horarios_aula[Día.Lunes] = RangoHorario(time(9), time(12))
    aula: Aula = gestor.get_aula(0, 0)
    aula.horarios = horarios_aula

    gestor.agregar_carrera('0')
    gestor.agregar_materia(0)
    gestor.agregar_clase(0, 0)
    clase: Clase = gestor.get_clase(0, 0, 0)
    clase.día = Día.Lunes
    clase.horario = RangoHorario(time(10), time(11))

    assert clase.aula_asignada is None

    info = gestor.asignar_aulas()

    assert info.todo_ok()
    assert clase.aula_asignada is not None
