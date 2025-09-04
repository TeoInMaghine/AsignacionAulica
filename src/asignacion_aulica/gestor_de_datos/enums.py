from enum import Enum, StrEnum, auto

class Día(StrEnum):
    LUNES = 'Lunes'
    MARTES = 'Martes'
    MIÉRCOLES = 'Miércoles'
    JUEVES = 'Jueves'
    VIERNES = 'Viernes'
    SÁBADO = 'Sábado'
    DOMINGO = 'Domingo'

class PeriodoDeClases(Enum):
    CUATRIMESTRAL = auto()
    ANUAL = auto()
