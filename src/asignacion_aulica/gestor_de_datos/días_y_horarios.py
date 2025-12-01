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

def crear_horarios_semanales() -> HorariosSemanales:
    return HorariosSemanales(
        RangoHorario(time(7), time(22), d == Día.Domingo or d == Día.Sábado)
        for d in Día
    )

def crear_horarios_semanales_opcionales() -> HorariosSemanalesOpcionales:
    return HorariosSemanalesOpcionales([None,]*len(Día))
