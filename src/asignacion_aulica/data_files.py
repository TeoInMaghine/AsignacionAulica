from importlib.resources import files

def get_file(nombre: str):
    return files('asignacion_aulica.data').joinpath(nombre)

open('fonts/times_new_roman.tiff')
open(get_file('fonts/times_new_roman.tiff'))