from dataclasses import dataclass
from typing import Optional

@dataclass
class Carrera:
    nombre: str
    edificio_preferido: Optional[str]
