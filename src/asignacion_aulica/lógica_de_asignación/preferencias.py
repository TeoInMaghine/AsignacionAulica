'''
En este módulo se definen las preferencias del sistema de asignación.

Las preferencias son valores numéricos que dependen de las variables del modelo,
y que se quieren minimizar o maximizar. En particular este módulo define
penalizaciones, que son preferencias que se quieren minimizar.

Cada penalización se define en una función que agrega al modelo las variables
necesarias y devuelve una tupla con: una expresión que representa el valor a
minimizar, y el valor máximo que puede llegar a tener esa expresión una vez
resuelto el modelo (excepto si el valor máximo es 0, en cuyo caso devuelve 1).

Las penalizaciones individuales se suman para formar una penalización total.
Cada penalización tiene un peso distinto en esa suma, para permitir darle más
importancia a unas que a otras.

El valor máximo o cota superior se utiliza para normalizar los valores de las
penalizaciones. Esto hace que las escalas de penalizaciones sean más
comparables, facilitando la selección de pesos.

La función `obtener_penalizaciones` es la que hay que llamar desde fuera de este
módulo.
'''
from ortools.sat.python.cp_model_helper import LinearExpr
from ortools.sat.python.cp_model import CpModel, IntVar
from typing import Callable, TypeAlias
from collections.abc import Sequence
import numpy as np

from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulasPreprocesadas, ClasesPreprocesadas
)

función_de_penalización: TypeAlias = Callable[
    [ClasesPreprocesadas, AulasPreprocesadas, CpModel, np.ndarray],
    tuple[LinearExpr|int, int]
]
'''
Las funciones de penalización toman los siguientes argumentos:
- clases: Los datos de las clases en el problema de asignación.
- aulas: Los datos de todas las aulas disponibles.
- modelo: el CpModel al que agregar variables.
- asignaciones: Matriz con los datos de asignaciones, donde las filas son
  clases y las columnas son aulas.

Y devuelven una expresión que representa el valor de la penalización, y su cota
superior. La cota superior siempre es mayor a 0.

Esto se omite de los docstrings para no tener que repetirlo en todos lados.
'''

#TODO: Preferir que clases del mismo año de la misma carrera el mismo día se
#      asignen en el mismo edificio.
#TODO: ¿Tal vez preferir que las clases de la misma materia se asignen al mismo
#      edificio?

def cantidad_de_clases_fuera_del_edificio_preferido(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    modelo: CpModel,
    asignaciones: np.ndarray
) -> tuple[LinearExpr|int, int]:
    '''Cantidad de clases que no están en el edificio preferido de su carrera.'''
    #TODO: calcular cantidad de alumnos en vez de cantidad de clases.
    cantidad_de_clases_fuera_del_edificio_preferido: LinearExpr|int = 0
    cota_superior: int = 0

    for rango_clases, rango_aulas_preferidas in clases.rangos_de_aulas_preferidas:
        n_clases = rango_clases.stop - rango_clases.start
        asignaciones_a_aulas_preferidas = asignaciones[rango_clases, rango_aulas_preferidas]
        cantidad_de_clases_fuera_del_edificio_preferido += n_clases - asignaciones_a_aulas_preferidas.sum()
        cota_superior += n_clases

    # Evitamos que la cota superior sea 0 porque luego se usa para dividir
    if cota_superior == 0:
        cota_superior = 1

    return cantidad_de_clases_fuera_del_edificio_preferido, cota_superior

def cantidad_de_alumnos_fuera_del_aula(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    modelo: CpModel,
    asignaciones: np.ndarray
) -> tuple[LinearExpr|int, int]:
    '''
    La cantidad de alumnos que exceden la capacidad del aula asignada a su clase.

    TODO: cambiar nombre a cantidad_de_alumnos_que_no_entran_en_el_aula
    '''
    mínima_capacidad = min(aula.capacidad for aula in aulas.aulas)

    cantidad_de_alumnos_que_no_entran_en_el_aula: LinearExpr|int = 0
    cota_superior_total = 0

    for i_clase, clase in enumerate(clases.clases):
        máximo_exceso_de_capacidad: LinearExpr|int = max(0, clase.cantidad_de_alumnos - mínima_capacidad)
        exceso_de_capacidad_en_esta_clase = modelo.new_int_var(0, máximo_exceso_de_capacidad, f"exceso_de_capacidad_de_clase{i_clase}")
        cota_superior_en_esta_clase = 0

        for i_aula, aula in enumerate(aulas.aulas):
            asignada_a_este_aula = asignaciones[i_clase, i_aula]

            # Esta lógica asume que no va a haber asignaciones en 1 nunca;
            # que van a ser 0 (asignaciones prohibidas) o variables del modelo
            if isinstance(asignada_a_este_aula, IntVar):
                exceso_si_se_asigna_a_este_aula = max(0, clase.cantidad_de_alumnos - aula.capacidad)
                modelo.add(exceso_de_capacidad_en_esta_clase == exceso_si_se_asigna_a_este_aula).only_enforce_if(asignada_a_este_aula)

                cota_superior_en_esta_clase = max(cota_superior_en_esta_clase, exceso_si_se_asigna_a_este_aula)

        cantidad_de_alumnos_que_no_entran_en_el_aula += exceso_de_capacidad_en_esta_clase
        cota_superior_total += cota_superior_en_esta_clase

    # Evitamos que la cota superior sea 0 porque luego se usa para dividir
    if cota_superior_total == 0:
        cota_superior_total = 1

    return cantidad_de_alumnos_que_no_entran_en_el_aula, cota_superior_total

def capacidad_sobrante(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    modelo: CpModel,
    asignaciones: np.ndarray
) -> tuple[LinearExpr|int, int]:
    '''
    Suma de la cantidad de asientos que sobran en el aula asignada a cada clase.
    '''
    máxima_capacidad = max(aula.capacidad for aula in aulas.aulas)

    capacidad_sobrante_total: LinearExpr|int = 0
    cota_superior_total: int = 0

    for i_clase, clase in enumerate(clases.clases):
        máxima_capacidad_sobrante = max(0, máxima_capacidad - clase.cantidad_de_alumnos)
        capacidad_sobrante_en_esta_clase = modelo.new_int_var(0, máxima_capacidad_sobrante, f"capacidad_sobrante_clase_{i_clase}")
        cota_superior_en_esta_clase = 0

        for i_aula, aula in enumerate(aulas.aulas):
            asignada_a_este_aula = asignaciones[i_clase, i_aula]

            # Esta lógica asume que no va a haber asignaciones en 1 nunca;
            # que van a ser 0 (asignaciones prohibidas) o variables del modelo
            if isinstance(asignada_a_este_aula, IntVar):
                sobrante_si_se_asigna_a_este_aula = max(0, aula.capacidad - clase.cantidad_de_alumnos)
                modelo.add(capacidad_sobrante_en_esta_clase == sobrante_si_se_asigna_a_este_aula).only_enforce_if(asignada_a_este_aula)

                cota_superior_en_esta_clase = max(cota_superior_en_esta_clase, sobrante_si_se_asigna_a_este_aula)

        capacidad_sobrante_total += capacidad_sobrante_en_esta_clase
        cota_superior_total += cota_superior_en_esta_clase

    # Evitamos que la cota superior sea 0 porque luego se usa para dividir
    if cota_superior_total == 0:
        cota_superior_total = 1

    return capacidad_sobrante_total, cota_superior_total

def cantidad_de_alumnos_en_edificios_no_deseables(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    modelo: CpModel,
    asignaciones: np.ndarray
) -> tuple[LinearExpr|int, int]:
    '''Cantidad de alumnos que cursan en edificios que se prefiere no usar.'''
    cantidad_de_alumnos_en_edificios_no_deseables = 0
    cota_superior = 0

    for i_clase, clase in enumerate(clases.clases):
        # Esta lógica asume que no va a haber asignaciones en 1 nunca;
        # que van a ser 0 (asignaciones prohibidas) o variables del modelo.
        asignaciones_a_edificios_no_deseables = asignaciones[i_clase, aulas.preferir_no_usar]
        puede_estar_en_edificio_no_deseable = any(map(lambda x: isinstance(x, IntVar), asignaciones_a_edificios_no_deseables))

        if puede_estar_en_edificio_no_deseable:
            está_en_edificio_no_deseable = sum(asignaciones_a_edificios_no_deseables)
            cantidad_de_alumnos_en_edificios_no_deseables += clase.cantidad_de_alumnos * está_en_edificio_no_deseable
            cota_superior += clase.cantidad_de_alumnos

    # Evitamos que la cota superior sea 0 porque luego se usa para dividir
    if cota_superior == 0:
        cota_superior = 1

    return cantidad_de_alumnos_en_edificios_no_deseables, cota_superior

todas_las_penalizaciones: Sequence[tuple[int, función_de_penalización]] = (
    (1000, cantidad_de_alumnos_fuera_del_aula),
    (100,  cantidad_de_clases_fuera_del_edificio_preferido),
    (10,   cantidad_de_alumnos_en_edificios_no_deseables),
    (1,    capacidad_sobrante)
)

def obtener_penalización(
    clases: ClasesPreprocesadas,
    aulas: AulasPreprocesadas,
    modelo: CpModel,
    asignaciones: np.ndarray
) -> LinearExpr|float:
    '''
    Calcula la suma de todas las penalizaciones, ponderada con sus pesos y sus
    cotas máximas.

    :param clases: Los datos de las clases en el problema de asignación.
    :param aulas: Los datos de todas las aulas disponibles.
    :param modelo: el CpModel al que agregar variables.
    :param asignaciones: Matriz con los datos de asignaciones, donde las filas
    son clases y las columnas son aulas.

    :return: La expresión de penalización total.
    '''
    penalización_total = 0.0
    for peso, función in todas_las_penalizaciones:
        penalización, cota_superior = función(clases, aulas, modelo, asignaciones)
        penalización_total += (peso / cota_superior) * penalización
    
    return penalización_total

