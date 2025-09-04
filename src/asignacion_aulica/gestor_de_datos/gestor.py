from asignacion_aulica.lógica_de_asignación import AsignaciónImposibleException

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
