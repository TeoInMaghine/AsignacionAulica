from dataclasses import dataclass, field
from datetime import time

from asignacion_aulica.gestor_de_datos.día import Día

@dataclass
class Edificio:
    nombre: str
    
    # Los horarios son tuplas (apretura, cierre).
    # La tupla (time(0), time(0)) indica que está cerrado.
    horario_lunes:     tuple[time, time]
    horario_martes:    tuple[time, time]
    horario_miércoles: tuple[time, time]
    horario_jueves:    tuple[time, time]
    horario_viernes:   tuple[time, time]
    horario_sábado:    tuple[time, time]
    horario_domingo:   tuple[time, time]

    # Mapea el nombre del aula grande a los nombres de las aulas que la componen
    aulas_dobles: dict[str, tuple[str, str]] = field(default_factory=dict)
    # Indica que este edificio no es cómodo, y hay que evitarlo si es posible.
    preferir_no_usar: bool = False

@dataclass
class Aula:
    nombre: str
    edificio: str
    capacidad: int
    equipamiento: set[str] = field(default_factory=set)
    horario_lunes:     tuple[time, time]|None = None # Los horarios son tuplas (apretura, cierre).
    horario_martes:    tuple[time, time]|None = None # None significa que se usa el horario del edificio.
    horario_miércoles: tuple[time, time]|None = None
    horario_jueves:    tuple[time, time]|None = None
    horario_viernes:   tuple[time, time]|None = None
    horario_sábado:    tuple[time, time]|None = None
    horario_domingo:   tuple[time, time]|None = None

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
    carrera: str
    día: Día
    horario_inicio: time
    horario_fin: time
    virtual: bool
    cantidad_de_alumnos: int
    equipamiento_necesario: set[str] = field(default_factory=set)
    
    # Asignación manual/automática:
    # (None significa que todavía no se asignó)
    no_cambiar_asignación: bool = False # Indica si el aula y edificio se tienen que asignar automáticamente o mantener los valores puestos a mano.
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
