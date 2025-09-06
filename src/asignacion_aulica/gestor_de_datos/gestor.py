from typing import Optional

from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificio, Carrera, Clase
from asignacion_aulica.lógica_de_asignación import AsignaciónImposibleException
from asignacion_aulica.gestor_de_datos.enums import Día, PeriodoDeClases

class GestorDeDatos:
    '''
    Objeto encargado de administrar todos los datos de edificios, clases, y
    aulas.

    Internamente usa una base de datos para almacenar los datos de manera
    persistente.
    '''

    def __init__(self, path_base_de_datos: str):
        '''
        :param path_base_de_datos: El path absoluto del archivo de la base de
        datos. Si el archivo no existe, es creado.
        '''
        pass

    def asignar_aulas(self):
        '''
        Asignar aulas a todas las clases que no tengan una asignación forzada.

        :raise AsignaciónImposibleException: Si no se pueden asignar aulas a
        todas las clases. Al manejar esta excepción, tener en cuenta que se
        pueden haber asignado aulas a algunas clases si y otras no (esta
        información estará contenida en la excepción).
        '''
        # Nota: Este método debería llamar a lógica_de_asignación.asignar,
        # y actualizar la base de datos con el resultado.
        pass

    def importar_clases_de_excel(self, path: str):
        '''
        Leer datos de clases de un archivo excel e incorporarlos a la base de
        datos.

        TODO: Decidir si esta acción debería sobreescribir clases que ya existen
        o tirar una excepción o qué hacer.

        :param path: El path absoluto del archivo.

        :raise FileNotFoundError: Si el archivo no existe.
        :raise ExcelInválidoException: Si el formato del archivo no es correcto.
        :raise DatoInválidoException: Si el archivo contiene un dato inválido.
        '''
        # Nota: Este método debería llamar a archivos_excel.clases.importar,
        # y actualizar la base de datos con el resultado.
        # (El módulo archivos_excel todavía no existe, ver Issue #52)
        pass

    def exportar_clases_a_excel(self, path: str, carrera: Optional[str] = None):
        '''
        Escribir los datos de las clases (incluyendo la asignación de aulas) en
        un archivo excel.

        Si se especifica el nombre de una carrera, se exportan solamente las
        clases de esa carrera. Si no se especifica el nombre de una carrera, se
        exportan los datos de todas las carreras, una en cada hoja del archivo.

        :param path: El path absoluto del archivo.
        :param carrera: El nombre de una carrera, o None.

        :raise ValueError: Si `carrera` no es `None` y no es el nombre de una
        carrera que existe.
        :raise TBD: Si no se puede escribir el archivo en el path dado.
        '''
        # Nota: Este método debería llamar a archivos_excel.clases.exportar.
        # (El módulo archivos_excel todavía no existe, ver Issue #74)
        pass

    def exportar_cronograma_de_edificios_a_excel(self, path: str, edificio: Optional[str] = None):
        '''
        Generar un archivo excel con el cronograma de cada aula en formato de
        línea de tiempo.

        Si se especifica el nombre de un edificio, se genera solamente el
        cronograma de ese edificio. Si no se especifica el nombre de un
        edificio, se generan los cronogramas de todos los edificios, uno en cada
        hoja del archivo.

        :param path: El path absoluto del archivo.
        :param edificio: El nombre de un edificio, o None.

        :raise ValueError: Si `edificio` no es `None` y no es el nombre de un
        edificio que existe.
        :raise TBD: Si no se puede escribir el archivo en el path dado.
        '''
        # Nota: Este método debería llamar a archivos_excel.cronograma.exportar.
        # (El módulo archivos_excel todavía no existe, ver Issue #75)
        pass
