import pandas as pd

from asignacion_aulica import backend

materias = pd.read_csv('materias.csv')
aulas = pd.read_csv('aulas.csv')
aulas.index += 1 # Hacer que los números de aula empiecen en 1 (así el 0 es no tener aula)

asignaciones = backend.asignar(aulas, materias)

resultados_lindos = asignaciones.map(lambda x: '-' if x == 0 else f"{aulas.loc[x, 'edificio']} - {aulas.loc[x, 'nombre']}")
resultados_lindos.insert(0, 'Materia', materias['nombre'])