from enum import IntEnum, auto
from typing import Any
from openpyxl.workbook.workbook import Workbook
from collections.abc import Sequence
from pathlib import Path

from openpyxl.worksheet.worksheet import Worksheet

from asignacion_aulica.excel import plantilla_clases
from asignacion_aulica.gestor_de_datos.entidades import Carrera, Clase, Materia

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

class RowCounter:
    def __init__(self, initial_value: int = 0):
        self._current: int = initial_value
    def current(self) -> int:
        return self._current
    def next(self) -> int:
        self._current += 1
        return self._current

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
        _escribir_datos_de_una_carrera(hoja, carrera)

    excel.save(path)

def _escribir_datos_de_una_carrera(hoja: Worksheet, carrera: Carrera):
    hoja[celda_nombre_carrera].value = carrera.nombre
    #TODO: ano y cuatrimestre

    # Copiamos la lista de materias para poder ordenarla sin afectar al gestor.
    # Ordenamos las materias primero por año y después alfabéticamente.
    materias = list(carrera.materias)
    materias.sort(key=lambda materia: (materia.año, materia.nombre))

    fila_actual = RowCounter(initial_value=plantilla_clases.fila_primer_clase)
    for materia in materias:
        if len(materia.clases) > 0:
            _escribir_datos_de_una_materia(hoja, materia, fila_actual)

def _escribir_datos_de_una_materia(hoja: Worksheet, materia: Materia, fila_actual: RowCounter):
    _merge_cells_and_set_value(hoja, materia.año, fila_actual.current(), Columna.año, n_rows=len(materia.clases))
    _merge_cells_and_set_value(hoja, materia.nombre, fila_actual.current(), Columna.materia, n_rows=len(materia.clases))
    _merge_cells_and_set_value(hoja, materia.cuatrimestral_o_anual, fila_actual.current(), Columna.cuatrimestral_o_anual, n_rows=len(materia.clases))

    # Copiamos la lista de clases para poder ordenarla sin afectar al gestor.
    # Ordenamos las clases primero por comisión, después por día, y después por horario de inicio
    clases = list(materia.clases)
    clases.sort(key=lambda clase: (clase.comisión, clase.día, clase.horario.inicio))

    for clase in clases:
        _escribir_datos_de_una_clase(hoja, clase, fila_actual.current())
        fila_actual.next()

def _escribir_datos_de_una_clase(hoja: Worksheet, clase: Clase, fila_actual: int):
    hoja.cell(fila_actual, Columna.comisión, value=clase.comisión)
    hoja.cell(fila_actual, Columna.teórica_o_práctica, value=clase.teórica_o_práctica)
    hoja.cell(fila_actual, Columna.día, value=clase.día.name)
    hoja.cell(fila_actual, Columna.horario_inicio, value=clase.horario.inicio)
    hoja.cell(fila_actual, Columna.horario_fin, value=clase.horario.fin)
    hoja.cell(fila_actual, Columna.cupo, value=clase.cantidad_de_alumnos)
    hoja.cell(fila_actual, Columna.docente, value=clase.docente)
    hoja.cell(fila_actual, Columna.auxiliar, value=clase.auxiliar)
    hoja.cell(fila_actual, Columna.promocionable, value=clase.promocionable)

    if clase.virtual:
        _merge_cells_and_set_value(hoja, 'virtual', fila_actual, Columna.edificio, n_cols=2)
    elif clase.aula_asignada is not None:
        hoja.cell(fila_actual, Columna.edificio, value=clase.aula_asignada.edificio.nombre)
        hoja.cell(fila_actual, Columna.aula, value=clase.aula_asignada.nombre)


def _merge_cells_and_set_value(
    sheet: Worksheet,
    value: Any,
    start_row: int,
    start_col: int,
    n_rows: int = 1,
    n_cols: int = 1
):
    sheet.merge_cells(
        start_row=start_row,
        end_row=start_row + n_rows - 1,
        start_column=start_col,
        end_column=start_col + n_cols - 1
    )
    sheet.cell(start_row, start_col, value=value)
