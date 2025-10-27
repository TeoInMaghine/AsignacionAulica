'''
En este módulo se definen las restricciones del sistema de asignación.

Las restricciones son condiciones rígidas que tiene que cumplir la asignación de
aulas para ser válida.

Hay algunas restricciones que se pueden calcular conociendo solamente los datos
de las clases y los datos de las aulas, y que permiten anular algunas variables
del modelo. Estas restricciones se calculan con la función `aulas_prohibidas`.

Hay otras restricciones que para calcularlas se necesita comparar las variables
del modelo. Estas restricciones se calculan con la función
`restricciones_con_variables`.
'''
from ortools.sat.python.cp_model import BoundedLinearExpression
from itertools import combinations, product, chain
from collections.abc import Iterable, Sequence
from typing import Callable, TypeAlias
import numpy as np

from asignacion_aulica.gestor_de_datos.entidades import Clase
from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulaPreprocesada, AulasPreprocesadas, ClasesPreprocesadas
)

restricción_de_aulas_prohibidas: TypeAlias = Callable[
    [ClasesPreprocesadas, AulasPreprocesadas],
    Iterable[tuple[int, int]]
]
'''
Las restricciones de aulas prohibidas se representan con funciones que reciben:
- Los datos de las clases de el problema de asignación.
- Los datos de las aulas disponibles.

Y devuelven un iterable de tuplas `(índice de clase, índice de aula)` que
representan las combinaciones de clases y aulas que hay que evitar.
'''

restricción_con_variables: TypeAlias = Callable[
    [ClasesPreprocesadas, AulasPreprocesadas, np.ndarray],
    Iterable[BoundedLinearExpression]
]
'''
Las restricciones con variables se representan con funciones que reciben:
- Los datos de las clases de el problema de asignación.
- Los datos de las aulas disponibles.
- La matriz de variables de asignación, donde cada fila es una clase y cada
  columna es un aula.

Y devuelven un iterable de predicados que hay que agregar al modelo.
'''

def no_superponer_clases(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    asignaciones: np.ndarray
) -> Iterable[BoundedLinearExpression]:
    '''
    Las materias con horarios superpuestos no pueden estar en el mismo aula.
    '''
    for i_clase1, i_clase2 in _pares_de_clases_que_se_superponen(clases):
        asignaciones_de_ambas_clases = asignaciones[i_clase1, :] + asignaciones[i_clase2, :]
        for asignaciones_a_un_aula in asignaciones_de_ambas_clases:
            yield asignaciones_a_un_aula <= 1

def no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    asignaciones: np.ndarray
) -> Iterable[BoundedLinearExpression]:
    '''
    Si se asigna un aula doble, las aulas que la conforman no pueden asignarse
    a otras clases que en ese horario.
    '''
    for i_clase1, i_clase2 in _pares_de_clases_que_se_superponen(clases):
        for aula_doble, aulas_hijas in aulas.aulas_dobles.items():
            # Se asigna una clase al aula doble => No se asigna ninguna clase a las aulas hijas 
            # Se asigna alguna clase a una de las aulas hijas => No se asigna una clase al aula doble
            for aula_hija in aulas_hijas:
                yield asignaciones[i_clase1, aula_doble] + asignaciones[i_clase2, aula_hija] <= 1
                yield asignaciones[i_clase2, aula_doble] + asignaciones[i_clase1, aula_hija] <= 1

def no_asignar_aulas_ocupadas(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas
) -> Iterable[tuple[int, int]]:
    '''
    Una clase no puede ser asignada a un aula que está ocupada en ese horario.
    '''
    for clase_e_índice, aula_ocupada in product(enumerate(clases.clases), clases.aulas_ocupadas):
        i_clase, clase = clase_e_índice
        i_aula, horario_aula = aula_ocupada
        if clase.horario.se_superpone_con(horario_aula):
            yield (i_clase, i_aula)
            if i_aula in aulas.aulas_dobles:
                aula1, aula2 = aulas.aulas_dobles[i_aula]
                yield (i_clase, aula1)
                yield (i_clase, aula2)

def no_asignar_en_aula_cerrada(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas
) -> Iterable[tuple[int, int]]:
    '''
    Una clase no se puede asignar a un aula que no esté abierta en ese horario.
    '''
    for i_clase, clase, i_aula, aula in _combinaciones_de_clases_y_aulas(clases, aulas):
        horario_aula = aula.horarios[clase.día]
        aula_está_cerrada = horario_aula.inicio > clase.horario.inicio or horario_aula.fin < clase.horario.fin
        if aula_está_cerrada:
            yield (i_clase, i_aula)

def asignar_aulas_con_el_equipamiento_requerido(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas
) -> Iterable[tuple[int, int]]:
    '''
    Una clase no puede ser asignada a un aula que no tenga todo el equipamiento
    requerido.
    '''
    for i_clase, clase, i_aula, aula in _combinaciones_de_clases_y_aulas(clases, aulas):
        if not clase.equipamiento_necesario.issubset(aula.equipamiento):
            yield (i_clase, i_aula)

todas_las_restricciones_de_aulas_prohibidas: Sequence[restricción_de_aulas_prohibidas] = (
    no_asignar_aulas_ocupadas,
    no_asignar_en_aula_cerrada,
    asignar_aulas_con_el_equipamiento_requerido
)

todas_las_restricciones_con_variables: Sequence[restricción_con_variables] = (
    no_superponer_clases,
    no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo
)

def aulas_prohibidas(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas
) -> Iterable[tuple[int, int]]:
    '''
    Genera las combinaciones de clases y aulas que no pueden ser asignadas entre
    sí.

    :param clases: Los datos de las clases de el problema de asignación.
    :pram aulas: Los datos de las aulas disponibles.

    :return: Iterable de tuplas (clase, aula) que representan las combinaciones
    de índice de clase e índice de aula que hay que evitar.
    '''
    return chain.from_iterable(
        restricción(clases, aulas)
        for restricción in todas_las_restricciones_de_aulas_prohibidas
    )

def restricciones_con_variables(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    asignaciones: np.ndarray
) -> Iterable[BoundedLinearExpression]:
    '''
    :param clases: Los datos de las clases de el problema de asignación.
    :pram aulas: Los datos de las aulas disponibles.
    :param asignaciones: Matriz con las variables de asignaciones, donde las
    filas son clases y las columnas son aulas.

    :return: Iterable de predicados que deben ser agregados al modelo.
    '''
    return chain.from_iterable(
        restricción(clases, aulas, asignaciones)
        for restricción in todas_las_restricciones_con_variables
    )

def _combinaciones_de_clases_y_aulas(clases: ClasesPreprocesadas, aulas: AulasPreprocesadas) -> Iterable[tuple[int, Clase, int, AulaPreprocesada]]:
    '''
    Devuelve un iterable de todas las combinaciones de clases y aulas.

    El iterable produce tuplas (índice de la clase, clase, índice del aula, aula).
    '''
    for clase_con_índice, aula_con_ìndice in product(enumerate(clases.clases), enumerate(aulas.aulas)):
        i_clase, clase = clase_con_índice
        i_aula, aula = aula_con_ìndice
        yield i_clase, clase, i_aula, aula

def _pares_de_clases_que_se_superponen(clases: ClasesPreprocesadas) -> Iterable[tuple[int, int]]:
    '''
    Devuelve un iterable de todos los pares de clases que se superponen entre sí.

    El iterable produce tuplas (índice 1, índice 2).
    '''
    for clase1_e_índice, clase2_e_índice in combinations(enumerate(clases.clases), 2):
        i_clase1, clase1 = clase1_e_índice
        i_clase2, clase2 = clase2_e_índice
        se_superpopnen = clase1.día == clase2.día and clase1.horario.se_superpone_con(clase2.horario)
        if se_superpopnen:
            yield i_clase1, i_clase2
