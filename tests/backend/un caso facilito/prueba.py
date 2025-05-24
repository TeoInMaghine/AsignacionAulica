import pandas as pd
from asignacion_aulica import backend

clases = pd.read_csv('clases.csv')
aulas = pd.read_csv('aulas.csv')

asignaciones = backend.asignar(aulas, clases)

tabla_asignaciones = clases[['nombre', 'día', 'horario inicio', 'horario fin']].copy()
tabla_asignaciones['edificio'] = [aulas.loc[x, 'edificio'] for x in asignaciones]
tabla_asignaciones['aula'] = [aulas.loc[x, 'nombre'] for x in asignaciones]

print(tabla_asignaciones)