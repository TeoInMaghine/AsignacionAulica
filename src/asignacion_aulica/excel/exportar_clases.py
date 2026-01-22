from collections.abc import Sequence
from pathlib import Path

from asignacion_aulica.gestor_de_datos.entidades import Carrera


def exportar_datos_de_clases_a_excel(carreras: Sequence[Carrera], path: Path):
    '''
    Escribir los datos de las clases (incluyendo las aulas asignadas) en un
    archivo excel.

    Cada carrera se exporta en una en una hoja del archivo.

    :param carreras: Las carreras cuyos datos se quiere exportar.
    :param path: El path absoluto del archivo.

    :raise TBD: Si no se puede escribir el archivo en el path dado.
    '''
