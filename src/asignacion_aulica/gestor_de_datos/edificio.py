from dataclasses import dataclass

@dataclass
class Edificio:
    nombre: str
    aulas_dobles: dict[str, tuple[str, str]] # Mapea el nombre del aula grande a los nombres de las aulas que la componen
    preferir_no_usar: bool = False # Indica que este edificio no es cómodo, y hay que asignarle pocas clases si es posible.
