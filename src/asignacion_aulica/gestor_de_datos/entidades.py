from dataclasses import dataclass, field
from datetime import time

from asignacion_aulica.gestor_de_datos.día import Día

@dataclass
class Edificio:
    nombre: str
    aulas_dobles: dict[str, tuple[str, str]] # Mapea el nombre del aula grande a los nombres de las aulas que la componen
    preferir_no_usar: bool = False # Indica que este edificio no es cómodo, y hay que evitarlo si es posible.

    horario_lunes: tuple[time, time]|None = None # Los horarios son tuplas (apretura, cierre). None si está cerrado ese día.
    horario_martes: tuple[time, time]|None = None
    horario_miércoles: tuple[time, time]|None = None
    horario_jueves: tuple[time, time]|None = None
    horario_viernes: tuple[time, time]|None = None
    horario_sábado: tuple[time, time]|None = None
    horario_domingo: tuple[time, time]|None = None

@dataclass
class Aula:
    nombre: str
    edificio: str
    capacidad: int
    equipamiento: set[str] = field(default_factory=set)
    horario_lunes: tuple[time, time]|None = None # Los horarios son tuplas (apretura, cierre). None si está cerrado ese día.
    horario_martes: tuple[time, time]|None = None
    horario_miércoles: tuple[time, time]|None = None
    horario_jueves: tuple[time, time]|None = None
    horario_viernes: tuple[time, time]|None = None
    horario_sábado: tuple[time, time]|None = None
    horario_domingo: tuple[time, time]|None = None


@dataclass
class Carrera:
    nombre: str
    edificio_preferido: str|None = None

@dataclass
class Materia:
    nombre: str
    carrera: str
    año: int # Año dentro del plan de estudios de la carrera
    
    # Datos que pueden ser ingresados o no:
    # (no usamos estos datos, pero los tenemos que guardar para exportarlos)
    # (son strings con contenido libre, el usuario puede escribir cualquier cosa)
    cuatrimestral_o_anual: str|None = None

@dataclass
class Clase:
    id: int # Identificador para distinguir entre distintas clases de la misma materia. No es para que lo vea el usuario.

    # Datos obligatorios:
    materia: str
    día: Día
    horario_inicio: time
    horario_fin: time
    virtual: bool
    cantidad_de_alumnos: int
    asignación_forzada: bool = False # Indica si el aula y edificio se tienen que asignar automáticamente o mantener los valores puestos a mano.
    equipamiento_necesario: set[str] = field(default_factory=set)
    
    # Asignación manual/automática:
    # (None significa que todavía no se asignó)
    edificio: str|None = None
    aula: str|None = None

    # Datos que pueden ser ingresados o no:
    # (no usamos estos datos, pero los tenemos que guardar para exportarlos)
    # (son strings con contenido libre, el usuario puede escribir cualquier cosa)
    comisión: str|None = None
    teórica_o_práctica: str|None = None
    promocionable: str|None = None
    docente: str|None = None
    auxiliar: str|None = None
