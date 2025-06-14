import pandas as pd
import json
from asignacion_aulica import backend

def parsear_equipamiento(literal):
    componentes = (x.strip() for x in literal.split(','))
    return {componente for componente in componentes if componente != ''}

clases = pd.read_csv('clases.csv', keep_default_na=False)
aulas = pd.read_csv('aulas.csv', keep_default_na=False)

with open('aulas_dobles.json') as f:
    aulas_dobles = { int(aula_doble): tuple(aulas_hijas) for aula_doble, aulas_hijas in json.load(f).items() }

clases['equipamiento_necesario'] = list(map(parsear_equipamiento, clases['equipamiento_necesario']))
aulas['equipamiento'] = list(map(parsear_equipamiento, aulas['equipamiento']))

asignaciones = backend.asignar(clases, aulas, aulas_dobles)

tabla_asignaciones = clases.copy()
tabla_asignaciones['edificio'] = [aulas.loc[x, 'edificio'] for x in asignaciones]
tabla_asignaciones['aula'] = [aulas.loc[x, 'nombre'] for x in asignaciones]
tabla_asignaciones.sort_values(['día', 'horario_inicio'], inplace=True)

print(tabla_asignaciones)
