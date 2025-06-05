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

Esto se omite de los docstrings para no tener que repetirlo en todos lados.
'''
from itertools import combinations, product
from ortools.sat.python import cp_model
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

def no_asignar_en_aula_cerrada(clases: DataFrame, aulas: DataFrame):
    '''
    La clase no puede estar en un aula que no esté abierta en ese horario.
    '''
    for aula, clase in product(aulas.itertuples(), clases.itertuples()):
        if aula.horario_apertura > clase.horario_inicio or \
           aula.horario_cierre < clase.horario_fin:
               yield clase.aula_asignada != aula.Index

def asignar_aulas_con_capacidad_suficiente(clases: DataFrame, aulas: DataFrame):
    '''
    Una clase no puede ser asignada a un aula que tenga una capacidad menor a la cantidad de alumnos.
    '''
    for clase, aula in product(clases.itertuples(), aulas.itertuples()):
        if clase.cantidad_de_alumnos > aula.capacidad:
            yield clase.aula_asignada != aula.Index

def asignar_aulas_con_el_equipamiento_requerido(clases: DataFrame, aulas: DataFrame):
    '''
    Una clase no puede ser asignada a un aula que no tenga todo el equipamiento requerido.
    '''
    for clase, aula in product(clases.itertuples(), aulas.itertuples()):
        if not clase.equipamiento_necesario.issubset(aula.equipamiento):
            yield clase.aula_asignada != aula.Index

todas_las_funciones_de_restricciones = (
    no_superponer_clases,
    no_asignar_en_aula_cerrada,
    # asignar_aulas_con_capacidad_suficiente,
    asignar_aulas_con_el_equipamiento_requerido
)

def todas_las_restricciones(clases: DataFrame, aulas: DataFrame) -> Iterable:
    '''
    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :return: Iterable de predicados que deben ser agregados al modelo.
    '''
    for restricción in todas_las_funciones_de_restricciones:
        for predicado in restricción(clases, aulas):
            yield predicado
