from asignacion_aulica.gestor_de_datos.entidades import Carreras, Edificios
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

class InfoPostAsignación:
    '''
    Datos para informarle al usuario cómo salió la asignación.
    '''
    def __init__(
        self,
        edificios: Edificios,
        carreras: Carreras,
        días_sin_asignar: list[Día]
    ) -> None:
        '''
        :param días_sin_asignar: Días en los que no se pudo hacer la asignación.
        :param edificios: Los edificios disponibles.
        :param carreras: Las carreras, con las aulas ya asignadas.
        '''
        self.días_sin_asignar: list[Día] = días_sin_asignar
    
    def todo_ok(self) -> bool:
        '''
        :return: `True` si está todo bien y no hay nada que avisarle al usuario.
        '''
        return len(self.días_sin_asignar) == 0