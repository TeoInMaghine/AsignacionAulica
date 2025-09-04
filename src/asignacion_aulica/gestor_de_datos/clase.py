from dataclasses import dataclass, field
from typing import Optional
from datetime import time

from asignacion_aulica.gestor_de_datos.enums import Día, PeriodoDeClases

@dataclass
class Clase:
    # Datos obligatorios:
    año: int # Año dentro del plan de estudios de la carrera
    materia: str
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
    periodo_de_clases: Optional[PeriodoDeClases] = None
    promocionable: Optional[str] = None
    comisión: Optional[str] = None
    teórica_o_práctica: Optional[str] = None
    docente: Optional[str] = None
    auxiliar: Optional[str] = None
