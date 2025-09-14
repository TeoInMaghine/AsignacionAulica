from bisect import bisect_left, bisect_right
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import time

from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificio

@dataclass
class AulaPreprocesada:
    '''
    Es como `gestor_de_datos.Aula`, pero con los datos transformados de una
    forma conveniente para `lógica_de_asignación`.
    '''
    edificio: int # índice del edificio
    capacidad: int
    equipamiento: set[str]
    preferir_no_usar: bool

    # Tuplas (apertura, cierre) para cada día de la semana.
    # Los horarios son en minutos desde las 0AM.
    horarios: tuple[tuple[int, int], tuple[int, int], tuple[int, int],
        tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]

def preprocesar_aulas(edificios: Sequence[Edificio], aulas: Sequence[Aula]) -> Sequence[AulaPreprocesada]:
    '''
    Preprocesar los datos de edificios y aulas provenientes del gestor de datos
    para que queden en un formato cómodo para la lógica de asignación.
    
    :param edificios: Los edificios disponibles.
    :param aulas: Las aulas disponibles en cada uno de los edificios (agrupadas
    por edificio, en el mismo orden que la secuencia de edificios).
    '''
    aulas_preprocesadas: list[AulaPreprocesada] = []

    i_aula = 0
    for i_edificio, edificio in enumerate(edificios):
        while i_aula < len(aulas) and aulas[i_aula].edificio == edificio.nombre:
            aula = aulas[i_aula]
            aulas_preprocesadas.append(AulaPreprocesada(
                edificio=i_edificio,
                capacidad=aula.capacidad,
                equipamiento=aula.equipamiento,
                preferir_no_usar=edificio.preferir_no_usar,
                horarios=(
                    _time_a_minutos(aula.horario_lunes     or edificio.horario_lunes),
                    _time_a_minutos(aula.horario_martes    or edificio.horario_martes),
                    _time_a_minutos(aula.horario_miércoles or edificio.horario_miércoles),
                    _time_a_minutos(aula.horario_jueves    or edificio.horario_jueves),
                    _time_a_minutos(aula.horario_viernes   or edificio.horario_viernes),
                    _time_a_minutos(aula.horario_sábado    or edificio.horario_sábado),
                    _time_a_minutos(aula.horario_domingo   or edificio.horario_domingo),
                )
            ))
            i_aula += 1

    return aulas_preprocesadas

def calcular_índices_de_aulas_dobles(edificios: Sequence[Edificio], aulas: Sequence[Aula]) -> dict[int, tuple[int, int]]:
    '''
    Juntar los diccionarios de aulas dobles de todos los edificios en uno solo,
    y cambiar los nombres de aulas por sus índices.

    :param edificios: Los edificios disponibles (ordenados alfabéticamente).
    :param aulas: Las aulas disponibles en cada uno de los edificios (agrupadas
    por edificio, en el mismo orden que la secuencia de edificios, y dentro de
    cada edificio ordenadas alfabéticamente).
    '''
    aulas_dobles: dict[int, tuple[int, int]] = {}

    for edificio in edificios:
        i_min = bisect_left(aulas, edificio.nombre, key=lambda a: a.edificio)
        i_max = bisect_right(aulas, edificio.nombre, lo=i_min, key=lambda a: a.edificio)
        print(edificio.nombre, i_min, i_max)
        for aula_grande, aulas_chicas in edificio.aulas_dobles.items():
            i_aula_grande = bisect_left(aulas, aula_grande, lo=i_min, hi=i_max, key=lambda a: a.nombre)
            i_aula_chica0 = bisect_left(aulas, aulas_chicas[0], lo=i_min, hi=i_max, key=lambda a: a.nombre)
            i_aula_chica1 = bisect_left(aulas, aulas_chicas[1], lo=i_min, hi=i_max, key=lambda a: a.nombre)
            aulas_dobles[i_aula_grande] = (i_aula_chica0, i_aula_chica1)

    return aulas_dobles

def _time_a_minutos(t: tuple[time, time]) -> tuple[int, int]:
    return t[0].minute + 60*t[0].hour, t[1].minute + 60*t[1].hour
