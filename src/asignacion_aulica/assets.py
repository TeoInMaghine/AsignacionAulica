'''
Este módulo se encarga de calcular los paths absolutos de archivos, detectando
si se está ejecutando el programa en el entorno de desarrollo o en el entorno
empaquetado.
'''
from os import path, getenv
import sys

estamos_en_ambiente_empaquetado = getattr(sys, 'frozen', False)

if estamos_en_ambiente_empaquetado:
    assets_path = path.join(sys.prefix, 'assets')
    app_data_path = path.join(getenv('LOCALAPPDATA'), 'AsignaciónÁulica')
    QML_import_path = sys.prefix
else:
    este_directorio = path.dirname(__file__)
    assets_path = path.abspath(path.join(este_directorio, path.pardir, path.pardir, 'assets'))
    app_data_path = assets_path
    QML_import_path = path.join(este_directorio, 'GUI')

def get_path(*nombres: str, read_only: bool = True) -> str:
    '''
    Devuelve el path absoluto de un archivo dentro de la carpeta assets.

    Usar esta función para cargar archivos de manera independiente del ambiente
    de ejecución (ambiente de desarrollo o ambiente empaquetado).

    :param nombres: Una secuencia de nombres de directorios dentro de la carpeta
    assets. El último elemento de la lista puede ser el nombre de un archivo.

    :param read_only: Si el archivo no es modificable. Si estamos en el
    ambiente empaquetado, los archivos modificables se situarán en
    "AppData\Local" del usuario.

    :return: El path absoluto obtenido al unir el path de la carpeta assets con
    la lista de nombres.
    '''
    return path.join(assets_path if read_only else app_data_path, *nombres)
