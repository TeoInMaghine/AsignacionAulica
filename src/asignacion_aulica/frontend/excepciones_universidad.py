class ElementoInvalidoException(Exception):
    """Excepcion lanzada cuando quiere cambiarse un rango horario de dia a un horario de cierre menor al de apertura"""
    def __init__(self, mensaje, elemento=None):
        super().__init__(mensaje)
        self.elemento = elemento

class ElementoDuplicadoException(Exception):
    """Excepcion lanzada cuando quiere agregarse a un dataframe un dato que ya existe."""
    def __init__(self, mensaje, elemento=None):
        super().__init__(mensaje)
        self.elemento = elemento

class HorarioInvalidoException(Exception):
    """Excepcion lanzada cuando quiere cambiarse un rango horario de dia a un horario de cierre menor al de apertura"""
    def __init__(self, mensaje, elemento=None):
        super().__init__(mensaje)
        self.elemento = elemento

class ElementoNoExisteException(Exception):
    """Excepcion lanzada cuando quiere cambiarse un rango horario de dia a un horario de cierre menor al de apertura"""
    def __init__(self, mensaje, elemento=None):
        super().__init__(mensaje)
        self.elemento = elemento

class ElementoTieneDependenciasException(Exception):
    """Excepcion lanzada cuando quiere cambiarse un rango horario de dia a un horario de cierre menor al de apertura"""
    def __init__(self, mensaje, elemento=None):
        super().__init__(mensaje)
        self.elemento = elemento
