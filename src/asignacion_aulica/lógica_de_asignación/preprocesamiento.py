from bisect import bisect_left, bisect_right
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import time

from asignacion_aulica.gestor_de_datos.día import Día
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
    '''
    edificio: int # índice del edificio
    capacidad: int
    equipamiento: set[str]
    preferir_no_usar: bool

    # Tuplas (apertura, cierre) para cada día de la semana.
    horarios: tuple[tuple[time, time], tuple[time, time], tuple[time, time],
        tuple[time, time], tuple[time, time], tuple[time, time], tuple[time, time]]

@dataclass
class ClasePreprocesada:
    '''
    Es como `gestor_de_datos.Clase`, pero con los datos transformados de una
    forma conveniente para `lógica_de_asignación`.

    No hay atributos `virtual` y `no_cambiar_asignación` porque esta clase sólo
    representa clases que han de ser asignadas.
    '''
    carrera: str
    materia: str
    año: int
    día: Día
    horario_inicio: time
    horario_fin: time
    cantidad_de_alumnos: int
    equipamiento_necesario: set[str]
    edificio_preferido: str|None

def calcular_rango_de_aulas_por_edificio(
    edificios: Sequence[Edificio],
    aulas: Sequence[Aula]
) -> dict[str, tuple[int, int]]:
    '''
    Devuelve un diccionario que mapea nombre de edificio a el rango de índices
    de las aulas que pertenecen a ese edificio.

    Los rangos son (inicio, fin), con inicio inclusivo y fin exclusivo.
    '''
    return {
        edificio.nombre: (
            bisect_left(aulas, edificio.nombre, key=lambda a: a.edificio),
            bisect_right(aulas, edificio.nombre, key=lambda a: a.edificio)
        )
        for edificio in edificios
    }

def calcular_índices_de_aulas_dobles(
    edificios: Sequence[Edificio],
    aulas: Sequence[Aula],
    rango_de_aulas_por_edificio: dict[str, tuple[int, int]]
) -> dict[int, tuple[int, int]]:
    '''
    Juntar los diccionarios de aulas dobles de todos los edificios en uno solo,
    y cambiar los nombres de aulas por sus índices.

    :param edificios: Los edificios disponibles (ordenados alfabéticamente).
    :param aulas: Las aulas disponibles en cada uno de los edificios (agrupadas
    por edificio, en el mismo orden que la secuencia de edificios, y dentro de
    cada edificio ordenadas alfabéticamente).
    :param rango_de_aulas_por_edificio: Mapeo de nombre de edificio a rango de
    índices de sus aulas.
    '''
    aulas_dobles: dict[int, tuple[int, int]] = {}

    for edificio in edificios:
        i_min, i_max = rango_de_aulas_por_edificio[edificio.nombre]
        for aula_grande, aulas_chicas in edificio.aulas_dobles.items():
            i_aula_grande = bisect_left(aulas, aula_grande, lo=i_min, hi=i_max, key=lambda a: a.nombre)
            i_aula_chica0 = bisect_left(aulas, aulas_chicas[0], lo=i_min, hi=i_max, key=lambda a: a.nombre)
            i_aula_chica1 = bisect_left(aulas, aulas_chicas[1], lo=i_min, hi=i_max, key=lambda a: a.nombre)
            aulas_dobles[i_aula_grande] = (i_aula_chica0, i_aula_chica1)

    return aulas_dobles

def preprocesar_aulas(
    edificios: Sequence[Edificio],
    aulas: Sequence[Aula],
    rango_de_aulas_por_edificio: dict[str, tuple[int, int]]
) -> Sequence[AulaPreprocesada]:
    '''
    Preprocesar los datos de edificios y aulas provenientes del gestor de datos
    para que queden en un formato cómodo para la lógica de asignación.
    
    :param edificios: Los edificios disponibles.
    :param aulas: Las aulas disponibles en cada uno de los edificios (agrupadas
    por edificio, en el mismo orden que la secuencia de edificios).
    '''
    aulas_preprocesadas: list[AulaPreprocesada] = []

    for i_edificio, edificio in enumerate(edificios):
        i_start, i_end = rango_de_aulas_por_edificio[edificio.nombre]
        for aula in aulas[i_start:i_end]:
            aulas_preprocesadas.append(AulaPreprocesada(
                edificio=i_edificio,
                capacidad=aula.capacidad,
                equipamiento=aula.equipamiento,
                preferir_no_usar=edificio.preferir_no_usar,
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

    return aulas_preprocesadas

def preprocesar_clases(
    clases: Sequence[Clase],
    materias: Sequence[Materia],
    carreras: Sequence[Carrera]
) -> tuple[
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ],
    tuple[ list[ClasePreprocesada], list[int], set[tuple[str, str, time, time]] ]
]:
    '''
    Preprocesar los datos de clases/materias/carreras provenientes del gestor de
    datos para que queden en un formato cómodo para la lógica de asignación.

    Separar los datos de las clases que hay que asignar en cada día de la
    semana, filtrando clases virtuales y clases con asignación manual.

    :return: Para cada día de la semana, una tupla con:
    - Una lista de las clases que hay que asignar ese día.
    - Una lista de los índices de esas clases en la secuencia original.
    - Un set de horarios en los que algunas aulas están ocupadas con las
      asignaciones manuales, expresados en tuplas (edificio, aula, inicio, fin).
    '''
    datos_procesados = (
        (list[ClasePreprocesada](), list[int](), set[tuple[str, str, time, time]]()),
        (list[ClasePreprocesada](), list[int](), set[tuple[str, str, time, time]]()),
        (list[ClasePreprocesada](), list[int](), set[tuple[str, str, time, time]]()),
        (list[ClasePreprocesada](), list[int](), set[tuple[str, str, time, time]]()),
        (list[ClasePreprocesada](), list[int](), set[tuple[str, str, time, time]]()),
        (list[ClasePreprocesada](), list[int](), set[tuple[str, str, time, time]]()),
        (list[ClasePreprocesada](), list[int](), set[tuple[str, str, time, time]]())
    )

    for i, clase in enumerate(clases):
        if clase.virtual:
            continue
        elif clase.no_cambiar_asignación:
            if clase.edificio is not None and clase.aula is not None:
                datos_procesados[clase.día][2].add((clase.edificio, clase.aula, clase.horario_inicio, clase.horario_fin))
        else:
            i_carrera = bisect_left(carreras, clase.carrera, key=lambda c:c.nombre)
            i_materia = bisect_left(materias, clase.carrera+clase.materia, key=lambda m:m.carrera+m.nombre)
            carrera = carreras[i_carrera]
            materia = materias[i_materia]
            
            datos_procesados[clase.día][1].append(i)
            datos_procesados[clase.día][0].append(ClasePreprocesada(
                carrera=clase.carrera,
                materia=clase.materia,
                año=materia.año,
                día=clase.día,
                horario_inicio=clase.horario_inicio,
                horario_fin=clase.horario_fin,
                cantidad_de_alumnos=clase.cantidad_de_alumnos,
                equipamiento_necesario=clase.equipamiento_necesario,
                edificio_preferido=carrera.edificio_preferido
            ))

    return datos_procesados
