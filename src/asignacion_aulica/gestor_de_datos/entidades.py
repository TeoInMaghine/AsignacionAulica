from dataclasses import dataclass, field
from typing import Optional
from datetime import time

from asignacion_aulica.gestor_de_datos.día import Día

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

@dataclass
class Edificio:
    nombre: str
    aulas_dobles: dict[str, tuple[str, str]] # Mapea el nombre del aula grande a los nombres de las aulas que la componen
    preferir_no_usar: bool = False # Indica que este edificio no es cómodo, y hay que asignarle pocas clases si es posible.

    horario_lunes: Optional[tuple[time, time]] = None # Los horarios son tuplas (apretura, cierre). None si está cerrado ese día.
    horario_martes: Optional[tuple[time, time]] = None
    horario_miércoles: Optional[tuple[time, time]] = None
    horario_jueves: Optional[tuple[time, time]] = None
    horario_viernes: Optional[tuple[time, time]] = None
    horario_sábado: Optional[tuple[time, time]] = None
    horario_domingo: Optional[tuple[time, time]] = None

@dataclass
class Carrera:
    nombre: str
    edificio_preferido: Optional[str]

@dataclass
class Clase:
    # Datos obligatorios:
    año: int # Año dentro del plan de estudios de la carrera
    materia: str
    carrera: str
    día: Día
    horario_inicio: time
    horario_fin: time
    virtual: bool
    cantidad_de_alumnos: int
    asignación_forzada: bool # Indica si el aula y edificio se tienen que asignar automáticamente o mantener los valores puestos a mano.
    
    # Asignación manual/automática:
    # (None significa que todavía no se asignó)
    edificio: Optional[str] = None
    aula: Optional[str] = None

    # Datos que pueden ser ingresados o no:
    # (no usamos algunos de estos datos, pero los tenemos que guardar para exportarlos)
    equipamiento_necesario: set[str] = field(default_factory=set)
    edificio_preferido: Optional[str] = None
    cuatrimestral_o_anual: Optional[str] = None
    promocionable: Optional[str] = None
    comisión: Optional[str] = None
    teórica_o_práctica: Optional[str] = None
    docente: Optional[str] = None
    auxiliar: Optional[str] = None
