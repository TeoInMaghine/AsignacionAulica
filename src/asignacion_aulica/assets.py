'''
Este módulo se encarga de calcular los paths absolutos de archivos, detectando
si se está ejecutando el programa en el entorno de desarrollo o en el entorno
empaquetado.
'''
from os import path, getenv
import sys

estamos_en_ambiente_empaquetado = getattr(sys, 'frozen', False)
ASSETS_PATH: str
APP_DATA_PATH: str
QML_IMPORT_PATH: str

if estamos_en_ambiente_empaquetado:
    ASSETS_PATH = path.join(sys.prefix, 'assets')
    APP_DATA_PATH = path.join(getenv('LOCALAPPDATA'), 'AsignaciónÁulica')
    QML_IMPORT_PATH = sys.prefix
else:
    este_directorio = path.dirname(__file__)
    ASSETS_PATH = path.abspath(path.join(este_directorio, path.pardir, path.pardir, 'assets'))
    APP_DATA_PATH = path.abspath(path.join(este_directorio, path.pardir, path.pardir, 'data'))
    QML_IMPORT_PATH = path.join(este_directorio, 'GUI')

def get_path(*nombres: str) -> str:
    '''
    Devuelve el path absoluto de un archivo dentro de la carpeta assets.

    Usar esta función para cargar archivos de manera independiente del ambiente
    de ejecución (ambiente de desarrollo o ambiente empaquetado).

    :param nombres: Una secuencia de nombres de directorios dentro de la carpeta
    assets. El último elemento de la lista puede ser el nombre de un archivo.

    :return: El path absoluto obtenido al unir el path de la carpeta assets con
    la lista de nombres.
    '''
    return path.join(ASSETS_PATH, *nombres)
