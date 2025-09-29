from dataclasses import fields, asdict
from PyQt6.QtCore import QAbstractListModel, Qt

from asignacion_aulica.gestor_de_datos import Aula

class ListAulas(QAbstractListModel):
    def __init__(self, parent):
        super().__init__(parent)
        atributos_aulas = [field.name for field in fields(Aula)]
        self.nombres_de_roles = {
            # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt
            i + Qt.ItemDataRole.UserRole + 1: atributo for i, atributo in enumerate(atributos_aulas)
        }
        # TODO: Esto es placeholder, falta usar el gestor de datos (que va a ser un quilombo btw)
        self.aulas = [
            Aula('B101', 'Anasagasti 1', 45),
            Aula('B102', 'Anasagasti 1', 45),
            Aula('B201', 'Anasagasti 1', 45)
        ]

    # Constante
    def roleNames(self):
        return {i: nombre.encode() for i, nombre in self.nombres_de_roles.items()}

    def rowCount(self, parent):
        return len(self.aulas)

    def data(self, index, role):
        if index.isValid() and role in self.nombres_de_roles:
            aula = self.aulas[index.row()]
            return asdict(aula)[self.nombres_de_roles[role]]

    def setData(self, index, value, role):
        if index.isValid() and role in self.nombres_de_roles:
            # TODO: validar value
            setattr(self.aulas[index.row()], self.nombres_de_roles[role], value)
            self.dataChanged.emit(index, index)
            return True

        return False
