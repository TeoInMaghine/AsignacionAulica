from os import environ, getcwd, path

# Si no existe la variable de ambiente FLET_ASSETS_DIR significa que estamos en
# el ejecutable, asignar assets_path usando getcwd(). Ver
# https://github.com/flet-dev/flet/discussions/4658 para más información.
assets_path = environ.get('FLET_ASSETS_DIR', path.join(getcwd(), "assets"))

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
