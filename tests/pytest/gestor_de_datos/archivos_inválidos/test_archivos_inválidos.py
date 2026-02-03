'''
Los archivos que se usan en estos tests fueron generados con pickle.dump, y
tienen los siguientes contenidos:

- empty.pickle                  : Nada, es un archivo vacío
- not_tuple.pickle              : [1, [], [], []]
- empty_tuple.pickle            : ()
- no_version.pickle             : ([], [], [])
- not_current_version.pickle    : (-1, [], [], [])
- invalid_current_version.pickle: (1, [], [])
'''
from os import path
from pathlib import Path
import pytest, logging
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

@pytest.fixture
def invalid_file(filename: str) -> Path:
    '''
    :return: A file inside this directory with the given name.
    '''
    return Path(__file__).parent / filename

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
    
    with pytest.raises(ValueError, match=expected_substring) as exc_info:
        gestor.cargar()

    logging.info(str(exc_info))

@pytest.mark.parametrize(
    argnames='filename',
    argvalues=[
        ('invalid_current_version.pickle'),
    ]
)
def test_archivo_inválido_con_versión_actual(invalid_file: Path):
    '''
    Verificar que el gestor puede identificar archivos inválidos marcados con
    la versión actual.
    '''
    gestor = GestorDeDatos(invalid_file)
    
    with pytest.raises(ValueError) as exc_info:
        gestor.cargar()

    substrings_not_included = (
        'nada',
        'tupla',
        'al menos un',
        'versión como primer objeto',
        'no es igual a la versión actual'
    )
    assert all(substring not in str(exc_info) for substring in substrings_not_included)
    logging.info(str(exc_info))
