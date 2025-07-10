'''
Funciones para analizar la asignación de aulas a posteriori.
'''
from pandas import DataFrame

def clases_con_aula_chica(clases: DataFrame, aulas: DataFrame, asignaciones: list[int]) -> dict[int, int]:
    '''
    Devuelve un diccionario que mapea índices de clases a la cantidad de alumnos
    que no entran en el aula asignada a esa clase.

    Las clases que entran bien en sus aulas no son incluídas en el diccionario.
    '''
    clases_con_aula_chica = {}
    for i in clases.index:
        exceso = clases.loc[i, 'cantidad_de_alumnos'] - aulas.loc[asignaciones[i], 'capacidad']
        if exceso > 0:
            clases_con_aula_chica[i] = exceso
    
    return clases_con_aula_chica

def clases_fuera_del_edificio_preferido(clases: DataFrame, aulas: DataFrame, asignaciones: list[int]) -> set[int]:
    '''
    Devuelve un set con los índices de las clases que están fuera de su edificio
    preferido.
    '''
    clases_fuera_del_edificio_preferido = set()
    for i in clases.index:
        if clases.loc[i, 'edificio_preferido'] and \
            clases.loc[i, 'edificio_preferido'] != aulas.loc[asignaciones[i], 'edificio']:
            clases_fuera_del_edificio_preferido.add(i)
    
    return clases_fuera_del_edificio_preferido