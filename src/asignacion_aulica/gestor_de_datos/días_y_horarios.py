from __future__ import annotations  # Para soportar referencias circulares en los type hints
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TypeAlias
from datetime import time

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

    def se_superpone_con(self, otro: RangoHorario) -> bool:
        return self.inicio < otro.fin and otro.inicio < self.fin

    @staticmethod
    def cerrado()-> RangoHorario:
        return RangoHorario(time(0), time(0))
    
    def es_cerrado(self) -> bool:
        return self.inicio == self.fin

HorariosSemanales: TypeAlias = tuple[
    RangoHorario, RangoHorario, RangoHorario, RangoHorario, RangoHorario,
    RangoHorario, RangoHorario
]
'''
Tupla con un RangoHorario para cada día de la semana.
'''

HorariosSemanalesOpcionales: TypeAlias = tuple[
    RangoHorario|None, RangoHorario|None, RangoHorario|None, RangoHorario|None,
    RangoHorario|None, RangoHorario|None, RangoHorario|None
]
'''
Tupla con un RangoHorario o None para cada día de la semana.
'''

def crear_horarios_semanales() -> HorariosSemanales:
    return HorariosSemanales(RangoHorario.cerrado() for _ in range(len(Día)))

def crear_horarios_semanales_opcionales() -> HorariosSemanalesOpcionales:
    return HorariosSemanalesOpcionales((None,)*len(Día))