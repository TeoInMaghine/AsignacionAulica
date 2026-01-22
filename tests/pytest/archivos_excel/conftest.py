'''
Los fixtures que se definen acá están disponibles en todos los casos de prueba
de este directorio.

Para usar un fixture, hay que ponerlo como argumento en la función del caso de
prueba que lo necesita.

Ver https://docs.pytest.org/en/stable/how-to/fixtures.html
'''
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import load_workbook
from pathlib import Path
import pytest

archivos_de_prueba = Path(__file__).parent.resolve() / 'archivos_de_prueba'

def pytest_configure(config):
    # Registrar los markers usados por las fixtures
    config.addinivalue_line("markers", "archivo: marca para pasar parametros al fixture archivo")

@pytest.fixture
def archivo(request) -> Path:
    '''
    Recibe en el marker "archivo" un nombre de archivo del directorio
    "archivos_de_prueba".

    :return: El path absoluto del archivo.
    '''
    nombre = request.node.get_closest_marker('archivo').args[0]
    return archivos_de_prueba / nombre

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
