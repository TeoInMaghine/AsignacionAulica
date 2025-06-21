'''
En este módulo se definen las preferencias del sistema de asignación.

Las preferencias son valores numéricos que dependen de las variables del modelo,
y que se quieren minimizar o maximizar. En particular este módulo define
penalizaciones, que son preferencias que se quieren minimizar.

Cada penalización se define en una función que agrega al modelo las variables
necesarias y devuelve una tupla con: una expresión que representa el valor a
minimizar, y el valor máximo que puede llegar a tener esa expresión una vez
resuelto el modelo (excepto si el valor máximo es 0, en cuyo caso devuelve 1).

Este valor máximo o cota superior se utiliza para normalizar los valores de las
penalizaciones. Esto hace que las escalas de penalizaciones sean más
comparables, facilitando la selección de pesos.

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
from ortools.sat.python.cp_model_helper import LinearExpr
from ortools.sat.python import cp_model
from pandas import DataFrame
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

def obtener_cantidad_de_clases_fuera_del_edificio_preferido(
        clases: DataFrame,
        aulas: DataFrame,
        modelo: cp_model.CpModel,
        asignaciones: np.ndarray
    ) -> tuple[LinearExpr, int]:
    '''
    Devuelve una expresión que representa la cantidad de clases fuera de su
    edificio preferido, y su cota superior.
    '''
    edificios = construir_edificios(aulas)

    # La cantidad comienza con el total de clases, y por cada clase que se
    # encuentra dentro de su edificio preferido se resta 1 a la cantidad de
    # clases fuera del edificio preferido
    cantidad_de_clases_fuera_del_edificio_preferido = len(clases)
    cota_superior = len(clases)

    for clase in clases.itertuples():
        if clase.edificio_preferido:
            # Esta expresión da 1 o 0
            en_edificio_preferido = sum(asignaciones[clase.Index, aula] for aula in edificios[clase.edificio_preferido])
            cantidad_de_clases_fuera_del_edificio_preferido -= en_edificio_preferido
        else:
            # Si no tiene edificio preferido, no puede estar fuera de su edificio preferido
            cantidad_de_clases_fuera_del_edificio_preferido -= 1
            cota_superior -= 1

    return cantidad_de_clases_fuera_del_edificio_preferido, cota_superior

def obtener_cantidad_de_alumnos_fuera_del_aula(
        clases: DataFrame,
        aulas: DataFrame,
        modelo: cp_model.CpModel,
        asignaciones: np.ndarray
    ) -> tuple[LinearExpr, int]:
    '''
    Devuelve una expresión que representa la cantidad de alumnos que exceden la
    capacidad del aula asignada a su clase, y su cota superior.
    '''
    mínima_capacidad = min(aulas["capacidad"])

    cantidad_de_alumnos_fuera_del_aula = 0
    cota_superior_total = 0

    for clase in clases.itertuples():
        # Un modelo es inválido si una variable tiene un upper bound menor a su
        # lower bound, así que tenemos que limitarlo
        máximo_exceso_de_capacidad = max(0, clase.cantidad_de_alumnos - mínima_capacidad)
        exceso_de_capacidad = modelo.new_int_var(0, máximo_exceso_de_capacidad, f"exceso_de_capacidad_de_{clase.nombre}")
        cota_superior = 0

        for aula in aulas.itertuples():
            asignada_a_este_aula = asignaciones[clase.Index, aula.Index]

            # Esta lógica asume que no va a haber asignaciones en 1 nunca;
            # que van a ser 0 (asignaciones prohibidas) o variables del modelo
            if isinstance(asignada_a_este_aula, cp_model.IntVar):
                posible_exceso = max(0, clase.cantidad_de_alumnos - aula.capacidad)
                modelo.add(exceso_de_capacidad == posible_exceso).only_enforce_if(asignada_a_este_aula)

                # Si no se sabe la asignación de antemano, la cota superior puede necesitar actualización
                cota_superior = max(cota_superior, posible_exceso)

        cantidad_de_alumnos_fuera_del_aula += exceso_de_capacidad
        cota_superior_total += cota_superior

    # Evitamos que la cota superior sea 0 porque luego se usa para dividir
    if cota_superior_total == 0:
        cota_superior_total = 1

    return cantidad_de_alumnos_fuera_del_aula, cota_superior_total

def obtener_capacidad_sobrante(
        clases: DataFrame,
        aulas: DataFrame,
        modelo: cp_model.CpModel,
        asignaciones: np.ndarray
    ) -> tuple[LinearExpr, int]:
    '''
    Devuelve una expresión que representa la cantidad de asientos que sobran en
    el aula asignada a cada clase, y su cota superior.
    '''
    máxima_capacidad = max(aulas["capacidad"])

    capacidad_sobrante_total = 0
    cota_superior_total = 0

    for clase in clases.itertuples():
        # Un modelo es inválido si una variable tiene un upper bound menor a su
        # lower bound, así que tenemos que limitarlo
        máxima_capacidad_sobrante = max(0, máxima_capacidad - clase.cantidad_de_alumnos)
        capacidad_sobrante = modelo.new_int_var(0, máxima_capacidad_sobrante, f"capacidad_sobrante_{clase.nombre}")
        cota_superior = 0

        for aula in aulas.itertuples():
            asignada_a_este_aula = asignaciones[clase.Index, aula.Index]

            # Esta lógica asume que no va a haber asignaciones en 1 nunca;
            # que van a ser 0 (asignaciones prohibidas) o variables del modelo
            if isinstance(asignada_a_este_aula, cp_model.IntVar):
                posible_sobra = max(0, aula.capacidad - clase.cantidad_de_alumnos)
                modelo.add(capacidad_sobrante == posible_sobra).only_enforce_if(asignada_a_este_aula)

                # Si no se sabe la asignación de antemano, la cota superior puede necesitar actualización
                cota_superior = max(cota_superior, posible_sobra)

        capacidad_sobrante_total += capacidad_sobrante
        cota_superior_total += cota_superior

    # Evitamos que la cota superior sea 0 porque luego se usa para dividir
    if cota_superior_total == 0:
        cota_superior_total = 1

    return capacidad_sobrante_total, cota_superior_total

# Iterable de tuplas (peso, función)
todas_las_penalizaciones = (
    (100,  obtener_cantidad_de_clases_fuera_del_edificio_preferido),
    (1000, obtener_cantidad_de_alumnos_fuera_del_aula),
    (1, obtener_capacidad_sobrante),
)

def obtener_penalización(
        clases: DataFrame,
        aulas: DataFrame,
        modelo: cp_model.CpModel,
        asignaciones: np.ndarray
    ):
    '''
    Calcula la suma de todas las penalizaciones con sus pesos,
    y normalizadas usando sus cotas máximas.

    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :param modelo: El CpModel al que agregar variables.
    :return: La expresión de penalización total.
    '''
    penalización_total = 0
    for peso, función in todas_las_penalizaciones:
        penalización, cota_superior = función(clases, aulas, modelo, asignaciones)
        penalización_total += (peso / cota_superior) * penalización
    
    return penalización_total

