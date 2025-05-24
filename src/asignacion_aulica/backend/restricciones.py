'''
En este módulo se definen las restricciones del sistema de asignación.

Las restricciones son predicados que se pueden agregar al modelo. La función
`todas_las_restricciones` devuelve un iterable con todos los predicados que hay
que agregar al modelo.

Internamente, cada restricción se define con una función que devuelve un
iterable de predicados.
Estas funciones toman los siguientes kwargs:
- clases: DataFrame, tabla con los datos de las clases
- aulas: DataFrame, tabla con los datos de las aulas
- asignaciones: lista con las variable de asignaciones de aulas

Esto se omite de los docstrings para no tener que repetirlo en todos lados.
'''
from ortools.sat.python import cp_model
from itertools import combinations
from pandas import DataFrame
from typing import Iterable

def no_superponer_clases(clases, aulas, asignaciones):
    '''
    Las materias con horarios superpuestos no pueden estar en el mismo aula.
    '''
    for clase1, clase2 in combinations(clases.index, 2):
        if clases.loc[clase1, 'día'] == clases.loc[clase2, 'día']:
            inicio_1 = clases.loc[clase1, 'horario inicio']
            fin_1 = clases.loc[clase1, 'horario fin']
            inicio_2 = clases.loc[clase2, 'horario inicio']
            fin_2 = clases.loc[clase2, 'horario fin']

            if inicio_1 < fin_2 and inicio_2 < fin_1:
                    yield asignaciones[clase1] != asignaciones[clase2]

todas_las_funciones_de_restricciones = (
    no_superponer_clases,
)

def todas_las_restricciones(clases: DataFrame, aulas: DataFrame, asignaciones: list) -> Iterable:
    '''
    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param asignaciones: Lista con las variables de asignación.
        asignaciones[i] es el número de aula asignada a la clase i.
    :return: Iterable de predicados que deben ser agregados al modelo.
    '''
    for restricción in todas_las_funciones_de_restricciones:
        for predicado in restricción(clases=clases, aulas=aulas, asignaciones=asignaciones):
            yield predicado