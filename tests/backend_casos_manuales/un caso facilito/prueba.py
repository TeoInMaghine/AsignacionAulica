import pandas as pd
import json
from asignacion_aulica import lógica_de_asignación

días = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

def parsear_equipamiento(literal):
    componentes = (x.strip() for x in literal.split(','))
    return {componente for componente in componentes if componente != ''}

def construir_horarios(aulas):
    horarios = []
    for i in aulas.index:
        horarios_i = {}
        for día in días:
            columna = f'horarios_{día}'
            if columna in aulas and aulas.loc[i, columna]:
                horarios_i[día] = tuple(map(int, aulas.loc[i, columna].split(',')))
        horarios.append(horarios_i)
    
    return horarios
        

clases = pd.read_csv('clases.csv', keep_default_na=False)
clases['equipamiento_necesario'] = list(map(parsear_equipamiento, clases['equipamiento_necesario']))

aulas = pd.read_csv('aulas.csv', keep_default_na=False)
aulas['equipamiento'] = list(map(parsear_equipamiento, aulas['equipamiento']))
aulas['horarios'] = construir_horarios(aulas)

lógica_de_asignación.asignar(clases, aulas)

tabla_asignaciones = clases.copy()
tabla_asignaciones['edificio'] = clases['aula_asignada'].map(aulas['edificio'])
tabla_asignaciones['aula'] = clases['aula_asignada'].map(aulas['nombre'])
tabla_asignaciones.sort_values(['día', 'horario_inicio'], inplace=True)

print(tabla_asignaciones)
