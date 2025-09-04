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
        Asigna aulas a todas las clases que no tengan una asignación forzada.

        :raise AsignaciónImposibleException: Si no se pueden asignar aulas a
        todas las clases. Al manejar esta excepción, tener en cuenta que se
        pueden haber asignado aulas a algunas clases si y otras no (esta
        información estará contenida en la excepción).
        '''
        # Nota: Este método debería llamar a lógica_de_asignación.asignar,
        # y actualizar la base de datos con el resultado.
        pass
