from dataclasses import dataclass

@dataclass
class Edificio:
    nombre: str
    aulas_dobles: dict[str, tuple[str, str]] # Mapea el nombre del aula grande a los nombres de las aulas que la componen
    preferir_no_usar: bool = False # Indica que este edificio no es cómodo, y hay que asignarle pocas clases si es posible.

    horario_lunes: Optional[tuple[time, time]] = None # Los horarios son tuplas (apretura, cierre). None si está cerrado ese día.
    horario_martes: Optional[tuple[time, time]] = None
    horario_miércoles: Optional[tuple[time, time]] = None
    horario_jueves: Optional[tuple[time, time]] = None
    horario_viernes: Optional[tuple[time, time]] = None
    horario_sábado: Optional[tuple[time, time]] = None
    horario_domingo: Optional[tuple[time, time]] = None
