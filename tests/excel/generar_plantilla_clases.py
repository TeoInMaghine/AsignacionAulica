'''
Este script crea la plantilla del archivo excel de clases.

El path en donde guardar el archivo se recibe como argumento.
'''

import sys, os
from asignacion_aulica.excel.plantilla_clases import crear_plantilla

filename = os.path.abspath(sys.argv[1])
dirname = os.path.dirname(filename)
os.makedirs(dirname, exist_ok=True)

plantilla = crear_plantilla()
plantilla.save(filename)
