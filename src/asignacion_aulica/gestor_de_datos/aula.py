from dataclasses import dataclass, field
from typing import Optional
from datetime import time

@dataclass
class Aula:
    nombre: str
    edificio: str
    capacidad: int
    equipamiento: set[str] = field(default_factory=set)
    horario_lunes: Optional[tuple[time, time]] = None # Los horarios son tuplas (apretura, cierre). None si está cerrado ese día.
    horario_martes: Optional[tuple[time, time]] = None
    horario_miércoles: Optional[tuple[time, time]] = None
    horario_jueves: Optional[tuple[time, time]] = None
    horario_viernes: Optional[tuple[time, time]] = None
    horario_sábado: Optional[tuple[time, time]] = None
    horario_domingo: Optional[tuple[time, time]] = None
