'''
En este módulo se definen las preferencias del sistema de asignación.

Las preferencias son valores numéricos que dependen de las variables del modelo,
y que se quieren minimizar o maximizar. En particular este módulo define
penalizaciones, que son preferencias que se quieren minimizar.

Cada penalización se define en una función que agrega al modelo las variables
necesarias y devuelve una expresión que representa el valor a minimizar.

Estas funciones toman los siguientes argumentos:
- clases: DataFrame, tabla con los datos de las clases
- aulas: DataFrame, tabla con los datos de las aulas
- modelo: el CpModel al que agregar variables
- asignaciones: Matriz con los datos de asignaciones, donde las filas son
  clases y las columnas son aulas.

Esto se omite de los docstrings para no tener que repetirlo en todos lados.

Las penalizaciones individuales se suman para formar una penalización total.
Cada penalización tiene un peso distinto en esa suma, para permitir darle más
importancia a unas que a otras.

La función `obtener_penalizaciones` es la que hay que llamar desde fuera de este
módulo. Devuelve un diccionario con todas las penalizaciones, incluyendo una
llamada "total" que es la que hay que minimizar.
'''
from ortools.sat.python import cp_model
from pandas import DataFrame
from typing import Iterable
import numpy as np

def construir_edificios(aulas: DataFrame) -> dict[str, set[int]]:
    '''
    Devuelve el diccionario de nombres de edificio a set de aulas que tiene cada edificio.
    '''
    edificios = {}
    for aula in aulas.itertuples():
        if not aula.edificio in edificios:
            edificios[aula.edificio] = set((aula.Index,))
        else:
            edificios[aula.edificio].add(aula.Index)

    return edificios

def obtener_cantidad_de_clases_fuera_del_edificio_preferido(clases: DataFrame, aulas: DataFrame, modelo: cp_model.CpModel, asignaciones: np.ndarray):
    '''
    Devuelve una expresión que representa la cantidad de clases fuera de su edificio preferido.
    '''
    edificios = construir_edificios(aulas)

    # La cantidad comienza con el total de clases, y por cada clase que se
    # encuentra dentro de su edificio preferido se resta 1 a la cantidad de
    # clases fuera del edificio preferido
    cantidad_de_clases_fuera_del_edificio_preferido = len(clases)
    for clase in clases.itertuples():
        if clase.edificio_preferido:
            # Esta expresión da 1 o 0
            en_edificio_preferido = sum(asignaciones[clase.Index, aula] for aula in edificios[clase.edificio_preferido])
            cantidad_de_clases_fuera_del_edificio_preferido -= en_edificio_preferido

    return cantidad_de_clases_fuera_del_edificio_preferido

def obtener_cantidad_de_alumnos_fuera_del_aula(clases: DataFrame, aulas: DataFrame, modelo: cp_model.CpModel, asignaciones: np.ndarray):
    '''
    Devuelve una expresión que representa la cantidad de alumnos que exceden la 
    capacidad del aula asignada a su clase.
    '''
    cantidad_de_alumnos_fuera_del_aula = 0

    for clase in clases.itertuples():
        exceso_de_capacidad = modelo.new_int_var(0, clase.cantidad_de_alumnos, f"exceso_de_capacidad_de_{clase.nombre}")
        for aula in aulas.itertuples():
            asignada_a_este_aula = asignaciones[clase.Index, aula.Index]

            if clase.cantidad_de_alumnos > aula.capacidad:
                modelo.add(exceso_de_capacidad == clase.cantidad_de_alumnos - aula.capacidad).only_enforce_if(asignada_a_este_aula)
            else:
                modelo.add(exceso_de_capacidad == 0).only_enforce_if(asignada_a_este_aula)
        
        cantidad_de_alumnos_fuera_del_aula += exceso_de_capacidad
    
    return cantidad_de_alumnos_fuera_del_aula

def obtener_capacidad_sobrante(clases: DataFrame, aulas: DataFrame, modelo: cp_model.CpModel, asignaciones: np.ndarray):
    '''
    Devuelve una expresión que representa la cantidad de asientos que sobran en
    el aula asignada a cada clase.
    '''
    capacidad_sobrante_total = 0

    for clase in clases.itertuples():
        capacidad_sobrante = modelo.new_int_var(0, clase.cantidad_de_alumnos, f"capacidad_sobrante_{clase.nombre}")
        for aula in aulas.itertuples():
            asignada_a_este_aula = asignaciones[clase.Index, aula.Index]

            if clase.cantidad_de_alumnos < aula.capacidad:
                modelo.add(capacidad_sobrante == aula.capacidad - clase.cantidad_de_alumnos).only_enforce_if(asignada_a_este_aula)
            else:
                modelo.add(capacidad_sobrante == 0).only_enforce_if(asignada_a_este_aula)
        
        capacidad_sobrante_total += capacidad_sobrante

    return capacidad_sobrante_total

# Iterable de tuplas (peso, función)
todas_las_penalizaciones = (
    (100,  obtener_cantidad_de_clases_fuera_del_edificio_preferido),
    (1000, obtener_cantidad_de_alumnos_fuera_del_aula),
    (1, obtener_capacidad_sobrante),
)

def obtener_penalización(clases: DataFrame, aulas: DataFrame, modelo: cp_model.CpModel, asignaciones: np.ndarray):
    '''
    Calcula la suma de todas las penalizaciones con sus pesos.

    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param modelo: El CpModel al que agregar variables.
    :return: La expresión de penalización total.
    '''
    penalización_total = 0
    for peso, función in todas_las_penalizaciones:
        penalización_total += peso * función(clases, aulas, modelo, asignaciones)
    
    return penalización_total
