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
- clases: DataFrame, tabla con los datos de las clases.
- aulas: DataFrame, tabla con los datos de las aulas.
- aulas_dobles: Diccionario con los datos de aulas dobles.
- asignaciones: Matriz con los datos de asignaciones, donde las filas son
  clases y las columnas son aulas.

Esto se omite de los docstrings para no tener que repetirlo en todos lados.
'''
from itertools import combinations, product
from pandas import DataFrame
from typing import Iterable
import numpy as np

from asignacion_aulica.gestor_de_datos.día import Día

def clases_se_superponen(clase1, clase2) -> bool:
    '''
    Evalúa si las clases están en el mismo día y tienen horarios que se superponen.
    :return: Booleano, verdadero si se superponen, falso si no.
    '''
    return clase1.día == clase2.día and \
           clase1.horario_inicio < clase2.horario_fin and \
           clase2.horario_inicio < clase1.horario_fin

def no_superponer_clases(clases: DataFrame, aulas: DataFrame, aulas_dobles: dict[ int, tuple[int, int] ], asignaciones: np.ndarray):
    '''
    Las materias con horarios superpuestos no pueden estar en el mismo aula.
    '''
    for clase1, clase2 in combinations(clases.itertuples(), 2):
        if clases_se_superponen(clase1, clase2):
            for aula in aulas.index:
                yield asignaciones[clase1.Index, aula] + asignaciones[clase2.Index, aula] <= 1

def no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo(clases: DataFrame, aulas: DataFrame, aulas_dobles: dict[ int, tuple[int, int] ], asignaciones: np.ndarray):
    '''
    Si se asigna un aula doble en cierto horario, no pueden asignarse las aulas
    individuales que lo conforman a clases que se superpongan en ese horario.
    '''
    for clase1, clase2 in combinations(clases.itertuples(), 2):
        if clases_se_superponen(clase1, clase2):
            for aula_doble, aulas_hijas in aulas_dobles.items():
                # Se asigna una clase al aula doble => No se asigna ninguna clase a las aulas hijas 
                # Se asigna alguna clase a una de las aulas hijas => No se asigna una clase al aula doble
                for aula_hija in aulas_hijas:
                    yield asignaciones[clase1.Index, aula_doble] + asignaciones[clase2.Index, aula_hija] <= 1
                    yield asignaciones[clase2.Index, aula_doble] + asignaciones[clase1.Index, aula_hija] <= 1

def no_asignar_en_aula_cerrada(clases: DataFrame, aulas: DataFrame):
    '''
    La clase no puede estar en un aula que no esté abierta en ese horario.
    '''
    for aula, clase in product(aulas.itertuples(), clases.itertuples()):
        aula_cerrada = clase.día not in aula.horarios or \
                       aula.horarios[clase.día][0] > clase.horario_inicio or \
                       aula.horarios[clase.día][1] < clase.horario_fin
        if aula_cerrada:
            yield (clase.Index, aula.Index)

def asignar_aulas_con_capacidad_suficiente(clases: DataFrame, aulas: DataFrame):
    '''
    Una clase no puede ser asignada a un aula que tenga una capacidad menor a la cantidad de alumnos.
    '''
    for clase, aula in product(clases.itertuples(), aulas.itertuples()):
        if clase.cantidad_de_alumnos > aula.capacidad:
            yield (clase.Index, aula.Index)

def asignar_aulas_con_el_equipamiento_requerido(clases: DataFrame, aulas: DataFrame):
    '''
    Una clase no puede ser asignada a un aula que no tenga todo el equipamiento requerido.
    '''
    for clase, aula in product(clases.itertuples(), aulas.itertuples()):
        if not clase.equipamiento_necesario.issubset(aula.equipamiento):
            yield (clase.Index, aula.Index)

def no_asignar_aulas_ocupadas(
    clases: DataFrame,
    aulas: DataFrame,
    aulas_dobles: dict[ int, tuple[int, int] ],
    aulas_ocupadas: set[tuple[int, Día, int, int]]
    ) -> Iterable[ tuple[int, int] ]:
    '''
    Una clase no puede ser asignada a un aula que está ocupada en ese horario.

    Esta función recibe argumentos distintos que las otras, así que no está en
    funciones_de_restricciones_de_aulas_prohibidas.
    '''
    for clase, aula_ocupada in product(clases.itertuples(), aulas_ocupadas):
        aula, día, inicio, fin = aula_ocupada
        se_superponen = clase.día == día and \
                        clase.horario_inicio < fin and \
                        clase.horario_fin > inicio
        if se_superponen:
            yield (clase.Index, aula)
            if aula in aulas_dobles:
                yield (clase.Index, aulas_dobles[aula][0])
                yield (clase.Index, aulas_dobles[aula][1])

funciones_de_restricciones_de_aulas_prohibidas = (
    no_asignar_en_aula_cerrada,
    # asignar_aulas_con_capacidad_suficiente,
    asignar_aulas_con_el_equipamiento_requerido
)

funciones_de_restricciones_con_variables = (
    no_superponer_clases,
    no_asignar_aula_doble_y_sus_hijas_al_mismo_tiempo
)

def aulas_prohibidas(
    clases: DataFrame,
    aulas: DataFrame,
    aulas_dobles: dict[ int, tuple[int, int] ],
    aulas_ocupadas: set[tuple[int, Día, int, int]]
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
        for índices in restricción(clases, aulas):
            yield índices
    
    for índices in no_asignar_aulas_ocupadas(clases, aulas, aulas_dobles, aulas_ocupadas):
        yield índices

def restricciones_con_variables(clases: DataFrame, aulas: DataFrame, aulas_dobles: dict[ int, tuple[int, int] ], asignaciones: np.ndarray) -> Iterable:
    '''
    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param aulas_dobles: Diccionario con los datos de aulas dobles.
    :param asignaciones: Matriz con los datos de asignaciones.
    :return: Iterable de predicados que deben ser agregados al modelo.
    '''
    for restricción in funciones_de_restricciones_con_variables:
        for predicado in restricción(clases, aulas, aulas_dobles, asignaciones):
            yield predicado

