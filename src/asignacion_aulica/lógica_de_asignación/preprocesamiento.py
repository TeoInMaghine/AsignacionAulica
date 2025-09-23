from bisect import bisect_left, bisect_right
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import time

from asignacion_aulica.gestor_de_datos.entidades import (
    Edificio,
    Aula,
    Carrera,
    Materia,
    Clase
)

@dataclass
class AulaPreprocesada:
    '''
    Es como `gestor_de_datos.Aula`, pero con los datos transformados de una
    forma conveniente para `lógica_de_asignación`.

    Por el momento, la única diferencia importante entre `Aula` y
    `AulaPreprocesada` es que los horarios están en una tupla, y que no pueden
    ser `None`.
    '''
    capacidad: int
    equipamiento: set[str]

    # Tuplas (apertura, cierre) para cada día de la semana.
    horarios: tuple[tuple[time, time], tuple[time, time], tuple[time, time],
        tuple[time, time], tuple[time, time], tuple[time, time], tuple[time, time]]


class AulasPreprocesadas:
    '''
    Contiene los datos de edificios y aulas provenientes del gestor de datos,
    preprocesados para que queden en un formato cómodo para la lógica de
    asignación.
    '''
    def __init__(self, edificios: Sequence[Edificio], aulas: Sequence[Aula]):
        '''
        :param edificios: Los edificios disponibles (en orden alfabético).
        :param aulas: Las aulas disponibles en cada uno de los edificios
        (agrupadas por edificio, en el mismo orden que la secuencia de
        edificios).
        '''
        # Datos de aulas preprocesadas, en el mismo orden que la secuencia
        # original.
        self.aulas: Sequence[AulaPreprocesada] = []
        
        # Diccionario de nombre de edificio a rango de índices de sus aulas.
        self.rangos_de_aulas: dict[str, slice] = dict()
        
        # Índices de las aulas de edificios que se prefiere no usar.
        self.preferir_no_usar: list[int] = []
        
        # Diccionario de índice del aula grande a índices de las dos aulas que
        # la componen.
        self.aulas_dobles: dict[int, tuple[int, int]] = {}


        for edificio in edificios:
            inicio_rango = bisect_left(aulas, edificio.nombre, key=lambda a: a.edificio)
            fin_rango = bisect_right(aulas, edificio.nombre, key=lambda a: a.edificio)
            rango = slice(inicio_rango, fin_rango)
            self.rangos_de_aulas[edificio.nombre] = rango

            if edificio.preferir_no_usar:
                self.preferir_no_usar.extend(range(inicio_rango, fin_rango))

            for aula_grande, aulas_chicas in edificio.aulas_dobles.items():
                i_aula_grande = bisect_left(aulas, aula_grande, lo=inicio_rango, hi=fin_rango, key=lambda a: a.nombre)
                i_aula_chica0 = bisect_left(aulas, aulas_chicas[0], lo=inicio_rango, hi=fin_rango, key=lambda a: a.nombre)
                i_aula_chica1 = bisect_left(aulas, aulas_chicas[1], lo=inicio_rango, hi=fin_rango, key=lambda a: a.nombre)
                self.aulas_dobles[i_aula_grande] = (i_aula_chica0, i_aula_chica1)

            for aula in aulas[rango]:
                self.aulas.append(AulaPreprocesada(
                    capacidad=aula.capacidad,
                    equipamiento=aula.equipamiento,
                    horarios=(
                        aula.horario_lunes     or edificio.horario_lunes,
                        aula.horario_martes    or edificio.horario_martes,
                        aula.horario_miércoles or edificio.horario_miércoles,
                        aula.horario_jueves    or edificio.horario_jueves,
                        aula.horario_viernes   or edificio.horario_viernes,
                        aula.horario_sábado    or edificio.horario_sábado,
                        aula.horario_domingo   or edificio.horario_domingo,
                    )
                ))

@dataclass
class ClasesPreprocesadas:
    '''
    Contiene los datos de un conjunto de clases/materias/carreras provenientes
    del gestor de datos, preprocesados para que queden en un formato cómodo para
    la lógica de asignación.

    Cada instancia de `ClasesPreprocesadas` contiene un subconjunto de clases
    que forma un problema de asignación independiente del resto de las clases.
    
    Cada instancia de `ClasesPreprocesadas` contiene clases de un solo día de la
    semana (porque esa es la forma más fácil de separar las clases en problemas
    independientes). Sería posible sub-dividir cada día en más de una instancia
    de `ClasesPreprocesadas`, pero por el momento eso no se está haciendo.
    '''
    # Un conjunto de clases que han de ser asignadas. Las clases en este
    # conjunto son presenciales y no tienen asignación manual.
    clases: Sequence[Clase]

    # Los índices que tienen las clases de este conjunto en la secuencia de
    # clases completa.
    índices_originales: Sequence[int]

    # Tuplas (rango de clases, rango de aulas) que indican que las clases del
    # primer rango pertenecen a una carrera que tiene un edificio preferido con
    # aulas contenidas en el segundo rango.
    rangos_de_aulas_preferidas: Iterable[tuple[slice, slice]]

    # Horarios en los que algunas aulas están ocupadas con clases que tienen
    # asignación manual, expresados en tuplas (edificio, aula, inicio, fin).
    aulas_ocupadas: Iterable[tuple[str, str, time, time]]

def preprocesar_clases(
    carreras: Sequence[Carrera],
    materias: Sequence[Materia],
    clases: Sequence[Clase],
    aulas: AulasPreprocesadas
) -> tuple[
    ClasesPreprocesadas, ClasesPreprocesadas, ClasesPreprocesadas,
    ClasesPreprocesadas, ClasesPreprocesadas, ClasesPreprocesadas,
    ClasesPreprocesadas
]:
    '''
    Preprocesar los datos de clases/materias/carreras provenientes del gestor de
    datos para que queden en un formato cómodo para la lógica de asignación.

    Separar por día de la semana los datos de las clases que hay que asignar,
    filtrando clases virtuales y clases con asignación manual.

    :param carreras: Las carreras que existen, en orden alfabético.
    :param materias: Las materias de todas las carreras (agrupadas por carrera
    en el mismo orden que la secuencia de carreras).
    :param clases: Las clases de todas las materias (agrupadas por materia, en
    el mismo orden que la secuencia de materias).
    :param aulas: El conjunto de aulas disponibles, preprocesadas.

    :return: Una tupla con un objeto `ClasesPreprocesadas` para cada día de la
    semana.
    '''
    datos_procesados = (
        ClasesPreprocesadas(list(), list(), list(), list()),
        ClasesPreprocesadas(list(), list(), list(), list()),
        ClasesPreprocesadas(list(), list(), list(), list()),
        ClasesPreprocesadas(list(), list(), list(), list()),
        ClasesPreprocesadas(list(), list(), list(), list()),
        ClasesPreprocesadas(list(), list(), list(), list()),
        ClasesPreprocesadas(list(), list(), list(), list())
    )

    # Filtrar clases virtuales, construir listas de aulas ocupadas, y clases a asignar
    for i_clase, clase in enumerate(clases):
        if clase.virtual:
            continue
        elif clase.no_cambiar_asignación:
            if clase.edificio is not None and clase.aula is not None:
                datos_procesados[clase.día].aulas_ocupadas.append(
                    (clase.edificio, clase.aula, clase.horario_inicio, clase.horario_fin)
                )
        else:
            datos_procesados[clase.día].clases.append(clase)
            datos_procesados[clase.día].índices_originales.append(i_clase)
    
    # Construir los rangos de clases con aulas preferidas
    for carrera in carreras:
        if carrera.edificio_preferido:
            rango_de_aulas: slice = aulas.rangos_de_aulas[carrera.edificio_preferido]
            for día in datos_procesados:
                inicio_rango = bisect_left(día.clases, carrera.nombre, key=lambda c: c.carrera)
                fin_rango = bisect_right(día.clases, carrera.nombre, key=lambda c: c.carrera)
                if inicio_rango != fin_rango:
                    rango_de_clases = slice(inicio_rango, fin_rango)
                    día.rangos_de_aulas_preferidas.append((rango_de_clases, rango_de_aulas))

    return datos_procesados
