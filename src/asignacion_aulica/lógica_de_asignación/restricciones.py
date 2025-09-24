'''
En este módulo se definen las restricciones del sistema de asignación.

Las restricciones son condiciones rígidas que tiene que cumplir la asignación.
Para simplificar la representación de los datos, se procesan primero las
restricciones que determinan un valor fijo para una variable de asignación, y
luego las restricciones que requieren comparar variables entre sí.

Las restricciones del primer tipo se definen como funciones que toman los datos
de clases y aulas, e indican qué valores se deben fijar.

Las del segundo tipo se definen como funciones que toman los datos de clases y
aulas, y la matriz de asignaciones, y devuelven predicados que se deben agregar
al modelo.

Estas funciones toman los siguientes argumentos:
- clases: Los datos de las clases en el problema de asignación.
- aulas: Los datos de todas las aulas disponibles.
- aulas_dobles: Diccionario con los índices de las aulas dobles.
- asignaciones: Matriz con los datos de asignaciones, donde las filas son
  clases y las columnas son aulas.

Esto se omite de los docstrings para no tener que repetirlo en todos lados.
'''
from datetime import time
from itertools import combinations, product
from pandas import DataFrame
from collections.abc import Iterable, Sequence
import numpy as np

from asignacion_aulica.gestor_de_datos.día import Día
from asignacion_aulica.gestor_de_datos.entidades import Clase
from asignacion_aulica.lógica_de_asignación.preprocesamiento import AulaPreprocesada

def no_superponer_clases(
    clases: Sequence[Clase],
    aulas: Sequence[AulaPreprocesada],
    aulas_dobles: dict[ int, tuple[int, int] ],
    asignaciones: np.ndarray
):
    '''
    Las materias con horarios superpuestos no pueden estar en el mismo aula.
    '''
    for i_clase1, clase1, i_clase2, clase2 in _pares_de_clases_que_se_superponen(clases):
        for i_aula in range(len(aulas)):
            yield asignaciones[i_clase1, i_aula] + asignaciones[i_clase2, i_aula] <= 1

def no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo(
    clases: Sequence[Clase],
    aulas: Sequence[AulaPreprocesada],
    aulas_dobles: dict[ int, tuple[int, int] ],
    asignaciones: np.ndarray
):
    '''
    Si se asigna un aula doble en cierto horario, no pueden asignarse las aulas
    individuales que la conforman a clases que se superpongan en ese horario.
    '''
    for i_clase1, clase1, i_clase2, clase2 in _pares_de_clases_que_se_superponen(clases):
        for aula_doble, aulas_hijas in aulas_dobles.items():
            # Se asigna una clase al aula doble => No se asigna ninguna clase a las aulas hijas 
            # Se asigna alguna clase a una de las aulas hijas => No se asigna una clase al aula doble
            for aula_hija in aulas_hijas:
                yield asignaciones[i_clase1, aula_doble] + asignaciones[i_clase2, aula_hija] <= 1
                yield asignaciones[i_clase2, aula_doble] + asignaciones[i_clase1, aula_hija] <= 1

def no_asignar_en_aula_cerrada(clases: Sequence[Clase], aulas: Sequence[AulaPreprocesada]) -> Iterable[ tuple[int, int] ]:
    '''
    La clase no puede estar en un aula que no esté abierta en ese horario.
    '''
    for i_clase, clase, i_aula, aula in _combinaciones_de_clases_y_aulas(clases, aulas):
        aula_abre, aula_cierra = aula.horarios[clase.día]
        aula_cerrada = aula_abre > clase.horario_inicio or aula_cierra < clase.horario_fin
        if aula_cerrada:
            yield (i_clase, i_aula)

def asignar_aulas_con_el_equipamiento_requerido(clases: Sequence[Clase], aulas: Sequence[AulaPreprocesada]) -> Iterable[ tuple[int, int] ]:
    '''
    Una clase no puede ser asignada a un aula que no tenga todo el equipamiento
    requerido.
    '''
    for i_clase, clase, i_aula, aula in _combinaciones_de_clases_y_aulas(clases, aulas):
        if not clase.equipamiento_necesario.issubset(aula.equipamiento):
            yield (i_clase, i_aula)

def no_asignar_aulas_ocupadas(
    clases: Sequence[Clase],
    aulas: Sequence[AulaPreprocesada],
    aulas_dobles: dict[ int, tuple[int, int] ],
    aulas_ocupadas: set[tuple[int, Día, time, time]]
) -> Iterable[ tuple[int, int] ]:
    '''
    Una clase no puede ser asignada a un aula que está ocupada en ese horario.

    Esta función recibe argumentos distintos que las otras, así que no está en
    funciones_de_restricciones_de_aulas_prohibidas.
    '''
    for clase_e_índice, aula_ocupada in product(enumerate(clases), aulas_ocupadas):
        i_clase, clase = clase_e_índice
        aula, día, inicio, fin = aula_ocupada
        se_superponen = clase.día == día and \
                        clase.horario_inicio < fin and \
                        clase.horario_fin > inicio
        if se_superponen:
            yield (i_clase, aula)
            if aula in aulas_dobles:
                yield (i_clase, aulas_dobles[aula][0])
                yield (i_clase, aulas_dobles[aula][1])

funciones_de_restricciones_de_aulas_prohibidas = (
    no_asignar_en_aula_cerrada,
    asignar_aulas_con_el_equipamiento_requerido
)

funciones_de_restricciones_con_variables = (
    no_superponer_clases,
    no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo
)

def aulas_prohibidas(
    clases: Sequence[Clase],
    aulas: Sequence[AulaPreprocesada],
    aulas_dobles: dict[ int, tuple[int, int] ],
    aulas_ocupadas: set[tuple[int, Día, time, time]]
    ) -> Iterable[ tuple[int, int] ]:
    '''
    Genera las combinaciones de clases y aulas que no pueden ser asignadas entre sí.

    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param aulas_dobles: Diccionario donde las keys son los índices de las
        aulas dobles y los valores son tuplas con las aulas individuales que
        conforman el aula doble.
    :param aulas_ocupadas: Tuplas (aula, día, inicio, fin) de momentos en los
        que no se pueden usar algunas aulas.
    :return: Iterable de tuplas (clase, aula), representando índices de la
    matriz de asignaciones.
    '''
    for restricción in funciones_de_restricciones_de_aulas_prohibidas:
        yield from restricción(clases, aulas)

    yield from no_asignar_aulas_ocupadas(clases, aulas, aulas_dobles, aulas_ocupadas)

def restricciones_con_variables(
    clases: Sequence[Clase],
    aulas: Sequence[AulaPreprocesada],
    aulas_dobles: dict[ int, tuple[int, int] ],
    asignaciones: np.ndarray) -> Iterable:
    '''
    :param clases: Los datos de las clases en el problema de asignación.
    :param aulas: Los datos de todas las aulas disponibles.
    :param aulas_dobles: Diccionario con los índices de las aulas dobles.
    asignaciones: Matriz con los datos de asignaciones, donde las filas son
    clases y las columnas son aulas.

    :return: Iterable de predicados que deben ser agregados al modelo.
    '''
    for restricción in funciones_de_restricciones_con_variables:
        yield from restricción(clases, aulas, aulas_dobles, asignaciones)

def _combinaciones_de_clases_y_aulas(clases: Sequence[Clase], aulas: Sequence[AulaPreprocesada]) -> Iterable[tuple[int, Clase, int, AulaPreprocesada]]:
    '''
    Devuelve un iterable de todas las combinaciones de clases y aulas.

    El iterable produce tuplas (índice de la clase, clase, índice del aula, aula).
    '''
    for clase_con_índice, aula_con_ìndice in product(enumerate(clases), enumerate(aulas)):
        i_clase, clase = clase_con_índice
        i_aula, aula = aula_con_ìndice
        yield i_clase, clase, i_aula, aula

def _pares_de_clases_que_se_superponen(clases: Sequence[Clase]) -> Iterable[tuple[int, Clase, int, Clase]]:
    '''
    Devuelve un iterable de todos los pares de clases que se superponen entre sí.

    El iterable produce tuplas (índice 1, clase 1, índice 2, clase 2).
    '''
    for clase1_e_índice, clase2_e_índice in combinations(enumerate(clases), 2):
        i_clase1, clase1 = clase1_e_índice
        i_clase2, clase2 = clase2_e_índice
        se_superpopnen = clase1.día == clase2.día and \
           clase1.horario_inicio < clase2.horario_fin and \
           clase2.horario_inicio < clase1.horario_fin
        if se_superpopnen:
            yield i_clase1, clase1, i_clase2, clase2
