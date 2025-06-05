'''
En este módulo se definen las preferencias del sistema de asignación.

Las preferencias son valores numéricos que dependen de las variables del modelo,
y que se quieren minimizar o maximizar. En particular este módulo define
penalizaciones, que son preferencias que se quieren minimizar.

Cada penalización se define en una función que agrega al modelo las variables
necesarias y devuelve una expresión que representa el valor a minimizar.

Estas funciones toman los siguientes argumentos:
- modelo: el CpModel al que agregar variables
- clases: DataFrame, tabla con los datos de las clases
- aulas: DataFrame, tabla con los datos de las aulas

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

def obtener_cantidad_de_clases_fuera_del_edificio_preferido(modelo: cp_model.CpModel, clases: DataFrame, aulas: DataFrame):
    '''
    Devuelve una expresión que representa la cantidad de clases fuera de su edificio preferido.
    '''
    edificios = construir_edificios(aulas)
    cantidad_de_clases_fuera_del_edificio_preferido = 0

    for clase in clases.itertuples():
        if clase.edificio_preferido:
            aulas_del_edificio_preferido_en_un_formato_re_raro = [(aula,) for aula in edificios[clase.edificio_preferido]]

            # Definir flag de edificio preferido en el modelo
            fuera_del_edificio_preferido = modelo.new_bool_var(f"{clase.nombre}_fuera_del_edificio_preferido")
            modelo.add_allowed_assignments([clase.aula_asignada], aulas_del_edificio_preferido_en_un_formato_re_raro).only_enforce_if(~fuera_del_edificio_preferido)
            modelo.add_forbidden_assignments([clase.aula_asignada], aulas_del_edificio_preferido_en_un_formato_re_raro).only_enforce_if(fuera_del_edificio_preferido)

            cantidad_de_clases_fuera_del_edificio_preferido += fuera_del_edificio_preferido

    return cantidad_de_clases_fuera_del_edificio_preferido

def obtener_cantidad_de_alumnos_fuera_del_aula(modelo: cp_model.CpModel, clases: DataFrame, aulas: DataFrame):
    '''
    Devuelve una expresión que representa la cantidad de alumnos que exceden la 
    capacidad del aula asignada a su clase.
    '''
    cantidad_de_alumnos_fuera_del_aula = 0

    for clase in clases.itertuples():
        exceso_de_capacidad = modelo.new_int_var(0, clase.cantidad_de_alumnos, f"exceso_de_capacidad_de_{clase.nombre}")
        for aula in aulas.itertuples():
            # NOTE: Esto crea una tabla de n×m variable booleanas. Eso puede
            # llegar a ser poco eficiente. También esas variables contienen
            # exactamente la misma información que la columna "aula_asignada",
            # así que se puede llegar a des-duplicar eliminando una de las dos.
            # 
            # NOTE: Por las restricciones del otro módulo, hay varias
            # asignaciones prohibidas que se podrían saltear acá para no crear
            # tantas variables y restricciones.
            asignada_a_este_aula = modelo.new_bool_var(f'{clase.nombre} asignada al aula {aula.Index}')
            modelo.add(clase.aula_asignada == aula.Index).OnlyEnforceIf(asignada_a_este_aula)
            modelo.add(clase.aula_asignada != aula.Index).OnlyEnforceIf(~asignada_a_este_aula)

            if clase.cantidad_de_alumnos > aula.capacidad:
                modelo.add(exceso_de_capacidad == clase.cantidad_de_alumnos - aula.capacidad).OnlyEnforceIf(asignada_a_este_aula)
            else:
                modelo.add(exceso_de_capacidad == 0).OnlyEnforceIf(asignada_a_este_aula)
        
        cantidad_de_alumnos_fuera_del_aula += exceso_de_capacidad
    
    return cantidad_de_alumnos_fuera_del_aula

# Iterable de tuplas (peso, función)
todas_las_penalizaciones = (
    (10,  obtener_cantidad_de_clases_fuera_del_edificio_preferido),
    (100, obtener_cantidad_de_alumnos_fuera_del_aula),
)

def obtener_penalizaciones(modelo: cp_model.CpModel, clases: DataFrame, aulas: DataFrame):
    '''
    Calcula la suma de todas las penalizaciones con sus pesos.

    :param modelo: El CpModel al que agregar variables.
    :param clases: Tabla con los datos de las clases.
    :param aulas: Tabla con los datos de las aulas.
    :return: La expresión de penalización total.
    '''
    penalización_total = 0
    for peso, función in todas_las_penalizaciones:
        penalización_total += peso * función(modelo, clases, aulas)
    
    return penalización_total

