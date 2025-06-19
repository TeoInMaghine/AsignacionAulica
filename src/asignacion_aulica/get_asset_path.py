from os import environ, path

assets_path = environ['FLET_ASSETS_DIR']

def get_asset_path(path_relativo: str) -> str:
    '''
    Devuelve el path absoluto de una archivo dentro de la carpeta assets.

    Usar esta función para cargar archivos (por ejemplo, con pandas) de manera
    independiente del ambiente de ejecución (ambiente de desarrollo o
    ambiente empaquetado).

    Para cargar archivos con flet no es necesario usar esta función, flet sabe
    que los paths relativos son respecto a la carpeta assets.

    :param path_relativo: El nombre de un archivo dentro de la carpeta assets.
    :return: El path absoluto del archivo.
    '''
    return path.join(assets_path, path_relativo)
