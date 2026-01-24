from enum import IntEnum, auto
from openpyxl.workbook.workbook import Workbook
from collections.abc import Sequence
from pathlib import Path

from asignacion_aulica.excel import plantilla_clases
from asignacion_aulica.gestor_de_datos.entidades import Carrera

# Coordenadas de las celdas relevantes
celda_nombre_carrera = 'F1'
celda_año = 'F2'
celda_cuatrimestre = 'J2'

class Columna(IntEnum):
    '''
    Los índices de las columnas de la tabla.
    '''
    año = 1
    materia = auto()
    cuatrimestral_o_anual = auto()
    comisión = auto()
    teórica_o_práctica = auto()
    día = auto()
    horario_inicio = auto()
    horario_fin = auto()
    cupo = auto()
    docente = auto()
    auxiliar = auto()
    promocionable = auto()
    edificio = auto()
    aula = auto()


def exportar_datos_de_clases_a_excel(carreras: Sequence[Carrera], path: Path):
    '''
    Escribir los datos de las clases (incluyendo las aulas asignadas) en un
    archivo excel.

    Cada carrera se exporta en una en una hoja del archivo.

    :param carreras: Las carreras cuyos datos se quiere exportar.
    :param path: El path absoluto del archivo.

    :raise TBD: Si no se puede escribir el archivo en el path dado.
    '''
    excel = Workbook()
    excel.remove(excel.active) # Por defecto hay una hoja vacía que no queremos

    for carrera in carreras:
        hoja = excel.create_sheet(title=carrera.nombre)
        plantilla_clases.generar_plantilla(hoja)
        hoja[celda_nombre_carrera].value = carrera.nombre
        #TODO: ano y cuatrimestre

        fila_actual = 4 # la primera fila después del header de la tabla
        for materia in carrera.materias:
            if len(materia.clases) == 0:
                continue

            hoja.merge_cells(
                start_row=fila_actual,
                end_row=fila_actual+len(materia.clases)-1,
                start_column=Columna.año,
                end_column=Columna.año
            )
            hoja.cell(fila_actual, Columna.año, value=materia.año)

    excel.save(path)
