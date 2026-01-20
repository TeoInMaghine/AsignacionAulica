from __future__ import annotations  # Para soportar referencias circulares en los type hints
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TypeAlias
from datetime import datetime, time

class Día(IntEnum):
    Lunes = 0
    Martes = auto()
    Miércoles = auto()
    Jueves = auto()
    Viernes = auto()
    Sábado = auto()
    Domingo = auto()

@dataclass
class RangoHorario:
    inicio: time
    fin: time
    cerrado: bool = False

    def se_superpone_con(self, otro: RangoHorario) -> bool:
        return self.inicio < otro.fin and otro.inicio < self.fin

HorariosSemanales: TypeAlias = tuple[
    RangoHorario, RangoHorario, RangoHorario, RangoHorario, RangoHorario,
    RangoHorario, RangoHorario
]
'''
Tupla con un RangoHorario para cada día de la semana.
'''

HorariosSemanalesOpcionales: TypeAlias = list[RangoHorario|None] # El largo debe ser 7.
'''
Tupla con un RangoHorario o None para cada día de la semana.
'''

EQUIVALENTE_24_HORAS: time = time.max
'''
'24:00' no puede parsearse como time, lo tratamos como si fuera `time.max`.
'''

def parse_string_horario_to_time(value: str) -> time:
    '''
    Transformar string con formato HH:MM a time.
    '''
    if value == '24:00':
        return EQUIVALENTE_24_HORAS

    return datetime.strptime(value, '%H:%M').time()

def time_to_string_horario(horario: time) -> str:
    '''
    Transformar time a string con formato HH:MM.
    '''
    if horario == EQUIVALENTE_24_HORAS:
        return '24:00'

    return horario.strftime('%H:%M')

def crear_horarios_semanales() -> HorariosSemanales:
    return HorariosSemanales(
        RangoHorario(time(7), time(22), d == Día.Domingo or d == Día.Sábado)
        for d in Día
    )

def crear_horarios_semanales_opcionales() -> HorariosSemanalesOpcionales:
    return HorariosSemanalesOpcionales([None,]*len(Día))
