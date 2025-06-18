import pandas as pd
import json
from asignacion_aulica import backend

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

with open('aulas_dobles.json') as f:
    aulas_dobles = { int(aula_doble): tuple(aulas_hijas) for aula_doble, aulas_hijas in json.load(f).items() }

asignaciones = backend.asignar(clases, aulas, aulas_dobles)

tabla_asignaciones = clases.copy()
tabla_asignaciones['edificio'] = [aulas.loc[x, 'edificio'] for x in asignaciones]
tabla_asignaciones['aula'] = [aulas.loc[x, 'nombre'] for x in asignaciones]
tabla_asignaciones.sort_values(['día', 'horario_inicio'], inplace=True)

print(tabla_asignaciones)
