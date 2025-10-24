from ortools.sat.python.cp_model import CpModel
from dataclasses import dataclass, field
from collections.abc import Sequence
from datetime import time
import numpy as np


from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.entidades import (
    Carreras,
    Edificios,
    Edificio,
    Aula,
    AulaDoble,
    Carrera,
    Clase,
    Materia
)

horario_24_hs = lambda: RangoHorario(time(0), time(23, 59))
horario_default_para_clases = lambda: RangoHorario(time(10), time(11))

@dataclass
class MockAula:
    nombre: str|None = None
    capacidad: int = 1
    equipamiento: set[str] = field(default_factory=set)
    horario_lunes:     RangoHorario|None = None
    horario_martes:    RangoHorario|None = None
    horario_miércoles: RangoHorario|None = None
    horario_jueves:    RangoHorario|None = None
    horario_viernes:   RangoHorario|None = None
    horario_sábado:    RangoHorario|None = None
    horario_domingo:   RangoHorario|None = None

@dataclass
class MockEdificio:
    nombre: str|None = None
    preferir_no_usar: bool = False
    horario_lunes:     RangoHorario = field(default_factory=horario_24_hs)
    horario_martes:    RangoHorario = field(default_factory=horario_24_hs)
    horario_miércoles: RangoHorario = field(default_factory=horario_24_hs)
    horario_jueves:    RangoHorario = field(default_factory=horario_24_hs)
    horario_viernes:   RangoHorario = field(default_factory=horario_24_hs)
    horario_sábado:    RangoHorario = field(default_factory=horario_24_hs)
    horario_domingo:   RangoHorario = field(default_factory=horario_24_hs)
    aulas: Sequence[MockAula] = field(default_factory=tuple)
    aulas_dobles: dict[int, tuple[int, int]] = field(default_factory=dict)

@dataclass
class MockClase:
    virtual: bool = False
    día: Día = Día.Lunes
    horario: RangoHorario = field(default_factory=horario_default_para_clases)
    cantidad_de_alumnos: int = 1
    no_cambiar_asignación: bool = False
    equipamiento_necesario: set[str] = field(default_factory=set)
    aula_asignada: tuple[int, int]|None = None # índices del edificio y del aula 

@dataclass
class MockMateria:
    nombre: str|None = None
    año: int = 1
    clases: Sequence[MockClase] = field(default_factory=list)

@dataclass
class MockCarrera:
    nombre: str|None = None
    edificio_preferido: int|None = None
    materias: Sequence[MockMateria] = field(default_factory=list)


def make_edificios(edificios: Sequence[MockEdificio]) -> Edificios:
    '''
    Recibe datos (posiblemente incompletos) de los edificios y aulas, y los
    rellena con valores por defecto.

    :param edificios: Datos de edificios y aulas.
    :return: La secuencia de edificios esperada por lógica_de_asignación.
    '''
    edificios_de_verdad: list[Edificio] = []

    for i_edificio, edificio in enumerate(edificios):
        edificio_de_verdad = Edificio(
            nombre=edificio.nombre or f'edificio {i_edificio}',
            preferir_no_usar=edificio.preferir_no_usar,
            horarios=(
                edificio.horario_lunes, edificio.horario_martes,
                edificio.horario_miércoles, edificio.horario_jueves,
                edificio.horario_viernes, edificio.horario_sábado,
                edificio.horario_domingo
            )
        )
        edificio_de_verdad.aulas = [
            Aula(
                nombre=aula.nombre or f'aula {i_aula}',
                edificio=edificio_de_verdad,
                capacidad=aula.capacidad,
                equipamiento=aula.equipamiento,
                horarios=(
                    aula.horario_lunes,
                    aula.horario_martes,
                    aula.horario_miércoles,
                    aula.horario_jueves,
                    aula.horario_viernes,
                    aula.horario_sábado,
                    aula.horario_domingo
                )
            )
            for i_aula, aula in enumerate(edificio.aulas)
        ]
        edificio_de_verdad.aulas_dobles = [
            AulaDoble(
                edificio_de_verdad.aulas[aula_grande],
                edificio_de_verdad.aulas[aulas_chicas[0]],
                edificio_de_verdad.aulas[aulas_chicas[1]]
            )
            for aula_grande, aulas_chicas in edificio.aulas_dobles.items()
        ]

        edificios_de_verdad.append(edificio_de_verdad)
    
    return edificios_de_verdad

def make_carreras(edificios: Edificios, carreras: Sequence[MockCarrera]) -> Carreras:
    '''
    Recibe datos (posiblemente incompletos) de las carreras/materias/clases, y
    los rellena con valores por defecto.

    :param edificios: Los edificios disponibles.
    :param carreras: Datos de carreras/materias/clases.
    :return: La secuencia de carreras esperada por lógica_de_asignación.
    '''
    carreras_de_verdad: list[Carrera] = []

    for i_carrera, carrera in enumerate(carreras):
        carrera_de_verdad = Carrera(
            nombre=carrera.nombre or f'carrera {i_carrera}',
            edificio_preferido=edificios[carrera.edificio_preferido] if carrera.edificio_preferido is not None else None
        )
        for i_materia, materia in enumerate(carrera.materias):
            materia_de_verdad = Materia(
                nombre=materia.nombre or f'materia {i_materia}',
                carrera=carrera_de_verdad,
                año=materia.año,
            )
            for clase in materia.clases:
                if clase.aula_asignada:
                    i_edificio, i_aula = clase.aula_asignada
                    aula_asignada: Aula|None = edificios[i_edificio].aulas[i_aula]
                else:
                    aula_asignada: Aula|None = None

                materia_de_verdad.clases.append(Clase(
                    materia=materia_de_verdad,
                    día=clase.día,
                    horario=clase.horario,
                    virtual=clase.virtual,
                    cantidad_de_alumnos=clase.cantidad_de_alumnos,
                    equipamiento_necesario=clase.equipamiento_necesario,
                    aula_asignada=aula_asignada,
                    no_cambiar_asignación=clase.no_cambiar_asignación
                ))

            carrera_de_verdad.materias.append(materia_de_verdad)

        carreras_de_verdad.append(carrera_de_verdad)
    
    return carreras_de_verdad

def make_asignaciones(
    n_clases: int,
    n_aulas: int,
    modelo: CpModel,
    asignaciones_forzadas: dict[int, int]
) -> np.ndarray:
    '''
    Genera una matriz con las variables de asignación. No hay constantes, todas
    son variables que se agregan al modelo, a menos que se especifiquen
    asignaciones forzadas, en cuyo caso se colocan los ceros donde corresponda
    (no unos, para simular como ocurriría en la asignación real).

    También se agregan restricciones para que cada clase se asigne exactamente a
    un aula.

    :param asignaciones_forzadas: Diccionario de índices de clases a índices de
    aulas.
    :return: Matriz con los datos de asignaciones.
    '''
    asignaciones = np.empty(shape=(n_clases, n_aulas), dtype=object)
    
    for clase, aula in np.ndindex(asignaciones.shape):
        if clase not in asignaciones_forzadas or asignaciones_forzadas[clase] == aula:
            asignaciones[clase, aula] = modelo.new_bool_var(f'clase_{clase}_asignada_al_aula_{aula}')
        else:
            asignaciones[clase, aula] = 0
    
    # Asegurar que cada clase se asigna a exactamente un aula
    for clase in range(asignaciones.shape[0]):
        modelo.add_exactly_one(asignaciones[clase,:])
    
    return asignaciones