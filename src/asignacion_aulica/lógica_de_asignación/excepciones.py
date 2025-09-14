from asignacion_aulica.gestor_de_datos.día import Día

class AsignaciónImposibleException(Exception):
    def __init__(self, *días_sin_asignar: Día):
        super().__init__()
        self.días_sin_asignar: tuple[Día, ...] = tuple(días_sin_asignar)
