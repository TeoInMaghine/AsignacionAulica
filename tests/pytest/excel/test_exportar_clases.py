from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.cell import MergedCell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from asignacion_aulica.excel.exportar_clases import Columna, exportar_datos_de_clases_a_excel
from asignacion_aulica.gestor_de_datos.entidades import Carreras
from mocks import MockCarrera, MockMateria, MockClase, MockEdificio, MockAula
import pytest

@pytest.fixture
def tmp_xlsx_filename(tmp_path: Path) -> Path:
    '''
    :return: A filename inside a temporary directory created for each  test.
    '''
    return tmp_path / "tmp_file.xlsx"

@pytest.fixture
def excel_exportado(carreras: Carreras, tmp_xlsx_filename: Path) -> Workbook:
    '''
    Exporta los datos del fixture de carreras a un archivo excel, para luego
    leer y devolver el contenido del archivo.
    '''
    exportar_datos_de_clases_a_excel(carreras, tmp_xlsx_filename)
    return openpyxl.load_workbook(tmp_xlsx_filename)

def get_cell_value(sheet: Worksheet, row: int, col: int) -> Any:
    '''
    :return: The value of a cell that may be merged or not
    
    https://stackoverflow.com/a/76617485
    '''
    cell = sheet.cell(row=row, column=col)
    if isinstance(cell, MergedCell):
        for merged_range in sheet.merged_cells.ranges:
            if cell.coordinate in merged_range:
                # return the left top cell
                cell = sheet.cell(row=merged_range.min_row, column=merged_range.min_col)
                break
    return cell.value

@pytest.mark.carreras(
    MockCarrera(nombre='A'),
    MockCarrera(nombre='B'),
    MockCarrera(nombre='C')
)
def test_encabezado(carreras: Carreras, excel_exportado: Workbook):
    '''
    Verificar que hay una hoja para cada carrera y que aparecen los datos
    correctos en el encabezado.
    '''
    assert len(excel_exportado.worksheets) == len(carreras)
    for hoja, carrera in zip(excel_exportado.worksheets, carreras):
        assert hoja.title == carrera.nombre
        assert hoja['F1'].value == carrera.nombre
        #TODO: año y cuatrimestre
    
@pytest.mark.edificios(
    MockEdificio(nombre='E1', aulas=(MockAula(nombre='A1.1'), MockAula(nombre='A1.2'))),
    MockEdificio(nombre='E2', aulas=(MockAula(nombre='A2.1'), MockAula(nombre='A2.2')))
)
@pytest.mark.carreras(
    MockCarrera(
        materias=(
            MockMateria(
                nombre='Ma 1',
                año = 8,
                clases=(
                    MockClase(aula_asignada=(0, 1)),
                    MockClase(aula_asignada=(1, 0)),
                    MockClase(aula_asignada=None),
                    MockClase(virtual=True),
                )
            ),
        )
    )
)
def test_datos_de_las_clases(carreras: Carreras, excel_exportado: Workbook):
    carrera = carreras[0]
    materia = carrera.materias[0]
    clases = materia.clases
    
    hoja = excel_exportado.worksheets[0]
    
    for i in range(len(clases)):
        assert get_cell_value(hoja, i+4, Columna.año) == materia.año
        assert get_cell_value(hoja, i+4, Columna.materia) == materia.nombre
    