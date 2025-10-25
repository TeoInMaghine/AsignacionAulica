from asignacion_aulica.gestor_de_datos.entidades import Carreras, Clase, Edificios, todas_las_clases
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

class InfoPostAsignación:
    '''
    Datos para informarle al usuario cómo salió la asignación.
    '''
    def __init__(
        self,
        edificios: Edificios,
        carreras: Carreras,
        días_sin_asignar: list[Día]|None = None
    ) -> None:
        '''
        :param días_sin_asignar: Días en los que no se pudo hacer la asignación.
        :param edificios: Los edificios disponibles.
        :param carreras: Las carreras, con las aulas ya asignadas.
        '''
        carreras_con_edificio_preferido = (carrera for carrera in carreras if carrera.edificio_preferido)
        
        # Días en los que no se pudo hacer la asignación.
        self.días_sin_asignar: list[Día] = días_sin_asignar or []

        # Clases que tienen más alumnos de los que entran en el aula que tienen
        # asignada.
        self.clases_con_aula_chica: list[Clase] = [
            clase
            for clase in todas_las_clases(carreras)
            if clase.aula_asignada and clase.cantidad_de_alumnos > clase.aula_asignada.capacidad
        ]

        # Clases que están fuera de su edificio preferido.
        self.clases_fuera_de_su_edificio_preferido: list[Clase] = [
            clase
            for clase in todas_las_clases(carreras_con_edificio_preferido)
            if clase.aula_asignada and clase.aula_asignada.edificio != clase.materia.carrera.edificio_preferido
        ]
    
    def todo_ok(self) -> bool:
        '''
        :return: `True` si está todo bien y no hay nada que avisarle al usuario.
        '''
        return (
            len(self.días_sin_asignar) == 0
            and len(self.clases_con_aula_chica) == 0
            and len(self.clases_fuera_de_su_edificio_preferido) == 0
        )
