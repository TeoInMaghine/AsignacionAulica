from dataclasses import dataclass
from datetime import time

from asignacion_aulica.lógica_de_asignación.día import Día

@dataclass
class Clase:
    '''
    Representa los datos de una clase (una fila del excel).

    La existencia de esta clase es provisoria. Probablemente cambie de lugar o 
    simplemente no exista cuando se defina la interfaz con el módulo de gestión
    de datos.
    '''
    año: int
    materia: str
    cuatrimestral_o_anual: str
    comisión: str
    teórica_o_práctica: str
    día: Día
    horario_inicio: time
    horario_fin: time
    cantidad_de_alumnos: int
    docente: str
    auxiliar: str
    promocionable: str
    virtual: bool
    edificio: str
    aula: str
