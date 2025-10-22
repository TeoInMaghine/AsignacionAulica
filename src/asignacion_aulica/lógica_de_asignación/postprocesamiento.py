'''
Funciones para analizar la asignación de aulas a posteriori.
'''
from dataclasses import dataclass, field

from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

@dataclass 
class InfoPostAsignación:
    '''
    Datos para informarle al usuario cómo salió la asignación.
    '''

    días_sin_asignar: list[Día] = field(default_factory=list)