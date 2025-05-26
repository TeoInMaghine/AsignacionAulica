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
- aulas_asignadas: lista con las variables del modelo, donde cada índice
  representa una clase, y el valor de cada variable es el número de aula que
  tiene asignada esa clase.

Esto se omite de los docstrings para no tener que repetirlo en todos lados.
'''
from ortools.sat.python import cp_model
from itertools import combinations
from pandas import DataFrame
from typing import Iterable

def no_superponer_clases(clases, aulas, aulas_asignadas):
    '''
    Las materias con horarios superpuestos no pueden estar en el mismo aula.
    '''
    for index_clase1, index_clase2 in combinations(clases.index, 2):
        if clases.loc[index_clase1, 'día'] == clases.loc[index_clase2, 'día']:
            inicio_1 = clases.loc[index_clase1, 'horario inicio']
            fin_1 = clases.loc[index_clase1, 'horario fin']
            inicio_2 = clases.loc[index_clase2, 'horario inicio']
            fin_2 = clases.loc[index_clase2, 'horario fin']

            if inicio_1 < fin_2 and inicio_2 < fin_1:
                    yield aulas_asignadas[index_clase1] != aulas_asignadas[index_clase2]

todas_las_funciones_de_restricciones = (
    no_superponer_clases,
)

def todas_las_restricciones(clases: DataFrame, aulas: DataFrame, aulas_asignadas: list) -> Iterable:
    '''
    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param aulas_asignadas: Lista con las variables de asignación.
        aulas_asignadas[i] es el número de aula asignada a la clase i.
    :return: Iterable de predicados que deben ser agregados al modelo.
    '''
    for restricción in todas_las_funciones_de_restricciones:
        for predicado in restricción(clases=clases, aulas=aulas, aulas_asignadas=aulas_asignadas):
            yield predicado