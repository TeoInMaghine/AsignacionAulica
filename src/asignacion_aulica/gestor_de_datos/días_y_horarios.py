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

    @staticmethod
    def abierto()-> RangoHorario:
        return RangoHorario(time(7), time(22))
    
    def es_cerrado(self) -> bool:
        return self.inicio == self.fin

    def cerrar(self):
        self.inicio = time(0)
        self.fin = time(0)

    def abrir(self):
        self.inicio = time(7)
        self.fin = time(22)

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
        RangoHorario.cerrado() if d == Día.Domingo or d == Día.Sábado else
        RangoHorario.abierto()
        for d in Día
    )

def crear_horarios_semanales_opcionales() -> HorariosSemanalesOpcionales:
    return HorariosSemanalesOpcionales([None,]*len(Día))
