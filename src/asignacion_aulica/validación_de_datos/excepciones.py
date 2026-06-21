class DatoInválidoException(Exception):
    '''
    Esta excepción indica que un dato ingresado por el usuario (o leído de un
    archivo) no es válido.
    '''

    def __init__(self, mensaje: str):
        '''
        :param mensaje: Explicación de cuál fue el problema. Debe ser un mensaje
        listo para mostrar al usuario.
        '''
        super().__init__(mensaje)

class ExcelInválidoException(Exception):
    '''
    Esta excepción indica que un archivo excel proveído por el usuario no es
    válido.
    '''

    def __init__(self, mensaje: str):
        '''
        :param mensaje: Explicación de cuál fue el problema. Debe ser un mensaje
        listo para mostrar al usuario.
        '''
        super().__init__(mensaje)
