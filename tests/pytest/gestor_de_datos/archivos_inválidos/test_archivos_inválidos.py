from os import path
from pathlib import Path
import pytest, logging
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

@pytest.fixture
def invalid_file(filename: str) -> Path:
    '''
    :return: A file inside this directory with the given name.
    '''
    return Path(path.dirname(__file__) + '\\' + filename)

@pytest.mark.parametrize(
    argnames='filename,expected_substring',
    argvalues=[
        ('empty.pickle', 'nada'),
        ('not_tuple.pickle', 'tupla'),
        ('empty_tuple.pickle', 'al menos un'),
        ('no_version.pickle', 'versión como primer objeto'),
        ('not_current_version.pickle', 'no es igual a la versión actual'),
    ]
)
def test_archivos_inválidos(invalid_file: Path, expected_substring: str):
    '''
    Verificar que el gestor puede identificar archivos inválidos al cargar.
    '''
    gestor = GestorDeDatos(invalid_file)
    
    with pytest.raises(RuntimeError, match=expected_substring) as exc_info:
        gestor.cargar()

    logging.info(str(exc_info))

def test_archivo_inválido_con_versión_actual():
    '''
    Verificar que el gestor puede identificar archivos inválidos marcados con
    la versión actual.
    '''
    # TODO
    assert False
