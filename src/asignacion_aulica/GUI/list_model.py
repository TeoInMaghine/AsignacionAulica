from dataclasses import fields, asdict
from typing import Any
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray

from asignacion_aulica.gestor_de_datos import Aula

class ListAulas(QAbstractListModel):
    def __init__(self, parent):
        super().__init__(parent)
        atributos_aulas = [field.name for field in fields(Aula)]
        self.nombres_de_roles = {
            # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt
            i + Qt.ItemDataRole.UserRole + 1: atributo for i, atributo in enumerate(atributos_aulas)
        }
        # TODO: Esto es placeholder, falta usar el gestor de datos
        self.edificio = 'Anasagasti 1'
        self.aulas = [
            Aula('B101', self.edificio, 45),
            Aula('B102', self.edificio, 45),
            Aula('B201', self.edificio, 45)
        ]

    # Constante
    def roleNames(self) -> dict[int, QByteArray]:
        return {i: nombre.encode() for i, nombre in self.nombres_de_roles.items()}

    def rowCount(self, _parent: QModelIndex):
        return len(self.aulas)

    def data(self, index: QModelIndex, role: int):
        if index.isValid() and role in self.nombres_de_roles:
            aula = self.aulas[index.row()]
            return asdict(aula)[self.nombres_de_roles[role]]

    def setData(self, index: QModelIndex, value: Any, role: int):
        if index.isValid() and role in self.nombres_de_roles:
            # TODO: validar value
            setattr(self.aulas[index.row()], self.nombres_de_roles[role], value)
            self.dataChanged.emit(index, index)
            return True

        return False

    def removeRows(self, row: int, count: int, _parent: QModelIndex):
        # Borra un solo elemento aún cuando count > 1
        self.beginRemoveRows(_parent, row, row)
        self.aulas.pop(row)
        self.endRemoveRows()
        return True

    def insertRows(self, row: int, count: int, _parent: QModelIndex):
        # Inserta un solo elemento aún cuando count > 1
        self.beginInsertRows(_parent, row, row)
        # TODO: validar value (ej.: no dejar insertar si ya hay un aula "sin rellenar")
        # Insertar aula "sin rellenar"
        self.aulas.insert(row, Aula('', self.edificio, 0))
        self.endInsertRows()
        return True
