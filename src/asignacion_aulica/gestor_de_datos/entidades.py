from __future__ import annotations  # Para soportar referencias circulares en los type hints
from dataclasses import dataclass, field, fields
from collections.abc import Iterable, Sequence
from typing import TypeAlias
import itertools
import typing

from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    Día,
    RangoHorario,
    HorariosSemanales,
    crear_horarios_semanales,
    HorariosSemanalesOpcionales,
    crear_horarios_semanales_opcionales
)

@dataclass
class Edificio:
    nombre: str
    aulas: list[Aula] = field(default_factory=list)
    aulas_dobles: list[AulaDoble] = field(default_factory=list)
    horarios: HorariosSemanales = field(default_factory=crear_horarios_semanales)

    # Indica que este edificio no es cómodo, y hay que evitarlo si es posible.
    preferir_no_usar: bool = False

Edificios: TypeAlias = Sequence[Edificio]

@dataclass
class Aula:
    nombre: str
    edificio: Edificio
    capacidad: int
    equipamiento: set[str] = field(default_factory=set)

    # None significa que se usa el horario del edificio.
    horarios: HorariosSemanalesOpcionales = field(default_factory=crear_horarios_semanales_opcionales)

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

Carreras: TypeAlias = Sequence[Carrera]

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
    aula_asignada: Aula|None = None # None significa que todavía no se asignó
    no_cambiar_asignación: bool = False # Indica si el aula se tiene que asignar automáticamente o mantener el valor puesto a mano.

    # Datos que pueden ser ingresados o no:
    # (no usamos estos datos, pero los tenemos que guardar para exportarlos)
    # (son strings con contenido libre, el usuario puede escribir cualquier cosa)
    comisión: str|None = None
    teórica_o_práctica: str|None = None
    promocionable: str|None = None
    docente: str|None = None
    auxiliar: str|None = None

def todas_las_clases(carreras: Iterable[Carrera]) -> Iterable[Clase]:
    return itertools.chain.from_iterable(materia.clases for carrera in carreras for materia in carrera.materias)


# Definimos mapeos para acceder por índice a los campos de las entidades.
# Hacemos esto porque en los modelos de QT los campos se identifican con índices
# (llamados "roles").

fieldnames_Edificio:  tuple[str, ...] = tuple(f.name for f in fields(Edificio))
fieldnames_Aula:      tuple[str, ...] = tuple(f.name for f in fields(Aula))
fieldnames_AulaDoble: tuple[str, ...] = tuple(f.name for f in fields(AulaDoble))
fieldnames_Carrera:   tuple[str, ...] = tuple(f.name for f in fields(Carrera))
fieldnames_Materia:   tuple[str, ...] = tuple(f.name for f in fields(Materia))
fieldnames_Clase:     tuple[str, ...] = tuple(f.name for f in fields(Clase))

# Tipos de dato (sin parametrizar) de los campos.
# Usamos esto para chequear que los tipos de dato que llegan de QT son correctos
# para el campo al que van dirigidos (porlas).
# Guardamos las versiones no parametrizadas de los tipos (`get_origin`) porque
# python no soporta chequear tipos de datos parametrizados en runtime.
# Usamos `eval` porque los tipos de dato están guardados como strings.
fieldtypes_Edificio:  tuple[type, ...] = tuple(typing.get_origin(eval(f.type)) or eval(f.type) for f in fields(Edificio))
fieldtypes_Aula:      tuple[type, ...] = tuple(typing.get_origin(eval(f.type)) or eval(f.type) for f in fields(Aula))
fieldtypes_AulaDoble: tuple[type, ...] = tuple(typing.get_origin(eval(f.type)) or eval(f.type) for f in fields(AulaDoble))
fieldtypes_Carrera:   tuple[type, ...] = tuple(typing.get_origin(eval(f.type)) or eval(f.type) for f in fields(Carrera))
fieldtypes_Materia:   tuple[type, ...] = tuple(typing.get_origin(eval(f.type)) or eval(f.type) for f in fields(Materia))
fieldtypes_Clase:     tuple[type, ...] = tuple(typing.get_origin(eval(f.type)) or eval(f.type) for f in fields(Clase))