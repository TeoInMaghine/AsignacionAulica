from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

class AsignaciónImposibleException(Exception):
    def __init__(self, *días_sin_asignar: Día):
        if len(días_sin_asignar) == 0:
            mensaje = 'No se pudieron asignar las aulas.'
        elif len(días_sin_asignar) == 1:
            mensaje = f'No se pudieron asignar aulas para las clases del día {días_sin_asignar[0].name}.'
        else:
            días_str = ', '.join(día.name for día in días_sin_asignar[:-1]) + ' y ' + días_sin_asignar[-1].name
            mensaje = f'No se pudieron asignar aulas para las clases de los días {días_str}.'

        super().__init__(mensaje)
        self.días_sin_asignar: tuple[Día, ...] = tuple(días_sin_asignar)
