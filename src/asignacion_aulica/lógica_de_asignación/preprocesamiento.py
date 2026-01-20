from dataclasses import dataclass, field
from typing import TypeAlias
import itertools

from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    HorariosSemanales,
    RangoHorario,
    Día
)
from asignacion_aulica.gestor_de_datos.entidades import (
    Edificios,
    Edificio,
    Aula,
    Carreras,
    Clase
)

@dataclass
class AulaPreprocesada:
    '''
    Es como `gestor_de_datos.entidades.Aula`, pero con los horarios
    preprocesados para que ya no sean opcionales.
    '''
    nombre: str
    edificio: Edificio
    capacidad: int
    equipamiento: set[str]
    horarios: HorariosSemanales
    aula_original: Aula

class AulasPreprocesadas:
    '''
    Contiene los datos de edificios y aulas provenientes del gestor de datos,
    preprocesados para que queden en un formato cómodo para la lógica de
    asignación.
    '''
    def __init__(self, edificios: Edificios):
        '''
        :param edificios: Los edificios disponibles.
        '''
        # Las aulas de todos los edificios, concatenadas en el mismo orden que
        # la secuencia de edificios, y preprocesadas.
        self.aulas: list[AulaPreprocesada] = []
        
        # Diccionario de nombre de edificio a rango de índices de sus aulas.
        self.rangos_de_aulas: dict[str, slice] = dict()
        
        # Índices de las aulas de edificios que se prefiere no usar.
        self.preferir_no_usar: list[int] = []
        
        # Diccionario de índice del aula grande a índices de las dos aulas que
        # la componen.
        self.aulas_dobles: dict[int, tuple[int, int]] = {}

        # Popular las variables con los datos de las aulas:
        for edificio in edificios:
            inicio_rango = len(self.aulas)
            fin_rango = inicio_rango + len(edificio.aulas)
            rango = slice(inicio_rango, fin_rango)
            self.rangos_de_aulas[edificio.nombre] = rango

            if edificio.preferir_no_usar:
                self.preferir_no_usar.extend(range(inicio_rango, fin_rango))

            for aula_doble in edificio.aulas_dobles:
                i_aula_grande = inicio_rango + edificio.aulas.index(aula_doble.aula_grande)
                i_aula_chica_1 = inicio_rango + edificio.aulas.index(aula_doble.aula_chica_1)
                i_aula_chica_2 = inicio_rango + edificio.aulas.index(aula_doble.aula_chica_2)
                self.aulas_dobles[i_aula_grande] = (i_aula_chica_1, i_aula_chica_2)

            for aula in edificio.aulas:
                self.aulas.append(AulaPreprocesada(
                    nombre=aula.nombre,
                    edificio=edificio,
                    capacidad=aula.capacidad,
                    equipamiento=aula.equipamiento,
                    aula_original=aula,
                    horarios=HorariosSemanales((
                        aula.horarios[día] or edificio.horarios[día]
                        for día in Día
                    ))
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
    clases: list[Clase] = field(default_factory=list)

    # Tuplas (rango de clases, rango de aulas) que indican que las clases del
    # primer rango pertenecen a una carrera que tiene un edificio preferido con
    # aulas contenidas en el segundo rango.
    rangos_de_aulas_preferidas: list[tuple[slice, slice]] = field(default_factory=list)

    # Horarios en los que algunas aulas están ocupadas con clases que tienen
    # asignación manual.
    aulas_ocupadas: list[tuple[int, RangoHorario]] = field(default_factory=list)

ClasesPreprocesadasPorDía: TypeAlias = tuple[
    ClasesPreprocesadas, ClasesPreprocesadas, ClasesPreprocesadas,
    ClasesPreprocesadas, ClasesPreprocesadas, ClasesPreprocesadas,
    ClasesPreprocesadas
]
'''
Tupla con una instancia de ClasesPreprocesadas para cada día de la semana.
'''

def preprocesar_clases(
    carreras: Carreras,
    aulas: AulasPreprocesadas
) -> ClasesPreprocesadasPorDía:
    '''
    Preprocesar los datos de clases/materias/carreras provenientes del gestor de
    datos para que queden en un formato cómodo para la lógica de asignación.

    Separar por día de la semana los datos de las clases que hay que asignar,
    filtrando clases virtuales y clases con asignación manual.

    :param carreras: Las carreras que existen.
    :param aulas: El conjunto de aulas disponibles, preprocesadas.
    '''
    clases_preprocesadas = ClasesPreprocesadasPorDía((
        ClasesPreprocesadas(), ClasesPreprocesadas(), ClasesPreprocesadas(),
        ClasesPreprocesadas(), ClasesPreprocesadas(), ClasesPreprocesadas(),
        ClasesPreprocesadas()
    ))

    for carrera in carreras:
        clases_en_cada_día_antes_de_procesar_esta_carrera = tuple(len(día.clases) for día in clases_preprocesadas)

        # Popular clases y aulas ocupadas:
        clases_de_la_carrera = itertools.chain.from_iterable(
            materia.clases for materia in carrera.materias
        )
        for clase in clases_de_la_carrera:
            if clase.virtual:
                continue
            elif clase.no_cambiar_asignación:
                if clase.aula_asignada:
                    edificio = clase.aula_asignada.edificio
                    rango_del_edificio: slice = aulas.rangos_de_aulas[edificio.nombre]
                    i_aula: int = rango_del_edificio.start + edificio.aulas.index(clase.aula_asignada)
                    clases_preprocesadas[clase.día].aulas_ocupadas.append(
                        (i_aula, clase.horario)
                    )
            else:
                clases_preprocesadas[clase.día].clases.append(clase)
    
        # Popular rangos de aulas preferidas:
        if carrera.edificio_preferido:
            rango_de_aulas: slice = aulas.rangos_de_aulas[carrera.edificio_preferido.nombre]
            for día in Día:
                inicio_rango_esta_carrera = clases_en_cada_día_antes_de_procesar_esta_carrera[día]
                fin_rango_esta_carrera = len(clases_preprocesadas[día].clases)
                if fin_rango_esta_carrera != inicio_rango_esta_carrera:
                    rango_de_clases = slice(inicio_rango_esta_carrera, fin_rango_esta_carrera)
                    clases_preprocesadas[día].rangos_de_aulas_preferidas.append((rango_de_clases, rango_de_aulas))

    return clases_preprocesadas
