from __future__ import annotations  # Para soportar referencias circulares en los type hints
from dataclasses import dataclass, field
from datetime import time

from asignacion_aulica.gestor_de_datos.día import Día

@dataclass
class RangoHorario:
    inicio: time
    fin: time

    @staticmethod
    def cerrado()-> RangoHorario:
        return RangoHorario(time(0), time(0))
    
    def es_cerrado(self) -> bool:
        return self.inicio == self.fin

@dataclass
class Edificio:
    nombre: str
    aulas: list[Aula] = field(default_factory=list)
    aulas_dobles: list[AulaDoble] = field(default_factory=list)

    # Indica que este edificio no es cómodo, y hay que evitarlo si es posible.
    preferir_no_usar: bool = False
    
    horario_lunes:     RangoHorario = field(default_factory=RangoHorario.cerrado)
    horario_martes:    RangoHorario = field(default_factory=RangoHorario.cerrado)
    horario_miércoles: RangoHorario = field(default_factory=RangoHorario.cerrado)
    horario_jueves:    RangoHorario = field(default_factory=RangoHorario.cerrado)
    horario_viernes:   RangoHorario = field(default_factory=RangoHorario.cerrado)
    horario_sábado:    RangoHorario = field(default_factory=RangoHorario.cerrado)
    horario_domingo:   RangoHorario = field(default_factory=RangoHorario.cerrado)

@dataclass
class Aula:
    nombre: str
    edificio: Edificio
    capacidad: int
    equipamiento: set[str] = field(default_factory=set)
    horario_lunes:     RangoHorario|None = None # None significa que se usa el horario del edificio.
    horario_martes:    RangoHorario|None = None
    horario_miércoles: RangoHorario|None = None
    horario_jueves:    RangoHorario|None = None
    horario_viernes:   RangoHorario|None = None
    horario_sábado:    RangoHorario|None = None
    horario_domingo:   RangoHorario|None = None

@dataclass
class AulaDoble:
    aula_grande: Aula
    aula_chica_1: Aula
    aula_chica_2: Aula

@dataclass
class Carrera:
    nombre: str
    edificio_preferido: Edificio|None = None
    materias: list[Materia] = field(default_factory=list)

@dataclass
class Materia:
    nombre: str
    carrera: Carrera
    año: int # Año dentro del plan de estudios de la carrera
    clases: list[Clase] = field(default_factory=list)
    
    # Datos que pueden ser ingresados o no:
    # (no usamos estos datos, pero los tenemos que guardar para exportarlos)
    # (son strings con contenido libre, el usuario puede escribir cualquier cosa)
    cuatrimestral_o_anual: str|None = None

@dataclass
class Clase:
    # Datos obligatorios:
    materia: Materia
    día: Día
    horario: RangoHorario
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
