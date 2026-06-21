from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import load_workbook
import pytest

from mocks import (
    pytest_configure,
    edificios,
    carreras
)

@pytest.fixture
def primera_hoja_del_archivo(archivo) -> Worksheet:
    '''
    Recibe en el marker "archivo" el nombre de un archivo excel del directorio
    "archivos_de_prueba".

    :return: La primera hoja del archivo.
    '''
    libro = load_workbook(archivo)
    hoja = libro.active
    return hoja
