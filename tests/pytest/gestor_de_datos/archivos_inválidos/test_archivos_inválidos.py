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
    argnames='filename,expected_exception,expected_substring',
    argvalues=[
        ('empty.pickle',                   EOFError,     'Ran out of input'),
        ('not_tuple.pickle',               ValueError, 'tupla'),
        ('empty_tuple.pickle',             ValueError, 'al menos un'),
        ('no_version.pickle',              ValueError, 'versión como primer objeto'),
        ('not_current_version.pickle',     ValueError, 'no es igual a la versión actual'),
        ('invalid_current_version.pickle', ValueError, 'esperaba leer 4 objetos'),
    ]
)
def test_archivos_inválidos(
        invalid_file: Path, expected_exception: type, expected_substring: str
    ):
    '''
    Verificar que el gestor puede identificar archivos inválidos al cargar.
    '''
    gestor = GestorDeDatos(invalid_file)
    
    with pytest.raises(expected_exception, match=expected_substring) as exc_info:
        gestor.cargar()

    logging.info(str(exc_info))
