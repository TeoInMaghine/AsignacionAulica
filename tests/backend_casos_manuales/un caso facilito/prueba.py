import pandas as pd
from asignacion_aulica import backend

def parsear_equipamiento(literal):
    componentes = (x.strip() for x in literal.split(','))
    return {componente for componente in componentes if componente != ''}

clases = pd.read_csv('clases.csv', keep_default_na=False)
aulas = pd.read_csv('aulas.csv', keep_default_na=False)

clases['equipamiento_necesario'] = list(map(parsear_equipamiento, clases['equipamiento_necesario']))
aulas['equipamiento'] = list(map(parsear_equipamiento, aulas['equipamiento']))

asignaciones = backend.asignar(clases, aulas)

tabla_asignaciones = clases[['nombre', 'día', 'horario_inicio', 'horario_fin']].copy()
tabla_asignaciones['edificio'] = [aulas.loc[x, 'edificio'] for x in asignaciones]
tabla_asignaciones['aula'] = [aulas.loc[x, 'nombre'] for x in asignaciones]

print(tabla_asignaciones)