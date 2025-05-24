'''
En este módulo se definen las restricciones del sistema de asignación.

Cada restricción es una función que devuelve un iterable de predicados que se
pueden agregar al modelo.
Estas funciones toman los siguientes kwargs:
- materias: DataFrame, la tabla de materias
- aulas: DataFrame, la tabla de aulas
- asignaciones: DataFrame, la tabla de asignaciones de aulas

La constante `todas_las_restricciones` tiene un iterable con todas las
restricciones.
'''
from ortools.sat.python import cp_model
from itertools import combinations
from pandas import DataFrame

from .constantes import DÍAS_DE_LA_SEMANA

def solo_asignar_aula_a_las_materias_presenciales(materias, aulas, asignaciones):
    '''
    Las materias presenciales tienen asignada algún aula (!= 0).
    Las materias virtuales y las que no tienen clase no tienen aula (==0).
    '''
    for i in materias.index:
        for día in DÍAS_DE_LA_SEMANA:
            if materias.loc[i, f'modalidad {día}'] == 'presencial':
                yield asignaciones.loc[i, día] > 0
            else:
                yield asignaciones.loc[i, día] == 0

def no_superponer_materias(materias, aulas, asignaciones):
    '''
    Las materias con horarios superpuestos no pueden estar en el mismo aula.
    '''
    for día in DÍAS_DE_LA_SEMANA:
        modalidad = f'modalidad {día}'
        inicio = f'horario inicio {día}'
        fin = f'horario fin {día}'

        for materia_1, materia_2 in combinations(materias.index, 2):
            modalidad1 = materias.loc[materia_1, modalidad]
            modalidad2 = materias.loc[materia_2, modalidad]

            if modalidad1 == 'presencial' and modalidad2 == 'presencial':
                inicio_1 = materias.loc[materia_1, inicio]
                fin_1 = materias.loc[materia_1, fin]
                inicio_2 = materias.loc[materia_2, inicio]
                fin_2 = materias.loc[materia_2, fin]

                if inicio_1 < fin_2 and inicio_2 < fin_1:
                        yield asignaciones.loc[materia_1, día] != asignaciones.loc[materia_2, día]

todas_las_restricciones = (
    solo_asignar_aula_a_las_materias_presenciales,
    no_superponer_materias
)