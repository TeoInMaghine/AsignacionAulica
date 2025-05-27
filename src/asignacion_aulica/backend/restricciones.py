'''
En este módulo se definen las restricciones del sistema de asignación.

Las restricciones son predicados que se pueden agregar al modelo. La función
`todas_las_restricciones` devuelve un iterable con todos los predicados que hay
que agregar al modelo.

Internamente, cada restricción se define con una función que devuelve un
iterable de predicados.
Estas funciones toman los siguientes argumentos:
- clases: DataFrame, tabla con los datos de las clases
- aulas: DataFrame, tabla con los datos de las aulas
- aulas_asignadas: lista con las variables del modelo, donde cada índice
  representa una clase, y el valor de cada variable es el número de aula que
  tiene asignada esa clase.

Esto se omite de los docstrings para no tener que repetirlo en todos lados.
'''
from ortools.sat.python import cp_model
from itertools import combinations
from itertools import product
from pandas import DataFrame
from typing import Iterable

def no_superponer_clases(clases: DataFrame, aulas: DataFrame):
    '''
    Las materias con horarios superpuestos no pueden estar en el mismo aula.
    '''
    for clase1, clase2 in combinations(clases.itertuples(), 2):
        if clase1.día == clase2.día and \
           clase1.horario_inicio < clase2.horario_fin and \
           clase2.horario_inicio < clase1.horario_fin:
            yield clase1.aula_asignada != clase2.aula_asignada

def en_aula_abierta(clases: DataFrame, aulas: DataFrame):
    '''
    La clase no puede estar en un aula que no esté abierta en ese horario.
    '''
    for clase, aula in product(clases.itertuples(), aulas.itertuples()):
        if aula.horario_inicio > clase.horario_inicio or \
           clase.horario_fin > aula.horario_fin:
               yield clase.aula_asignada != aula.Index

todas_las_funciones_de_restricciones = (
    no_superponer_clases,
    en_aula_abierta,
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
        for predicado in restricción(clases, aulas, aulas_asignadas):
            yield predicado
