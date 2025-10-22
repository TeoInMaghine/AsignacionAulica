from typing import Any
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSignal

from asignacion_aulica.gestor_de_datos import GestorDeDatos, Aula, Edificio

class ListEquipamientos(QAbstractListModel):
    seleccionadosTextChanged = pyqtSignal()

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        # TODO: Esto es placeholder, falta usar el gestor de datos
        self.aula = Aula('B101', Edificio('Anasagasti'), 45)
        self.equipamientos = ["Proyector", "Computadoras", "No sé lol"]

    @pyqtProperty(str, notify=seleccionadosTextChanged)
    def seleccionadosText(self):
        if len(self.aula.equipamiento) == 0:
            return "Ninguno"

        return ",".join(self.aula.equipamiento)

    @pyqtProperty(int)
    def indexAula(self):
        return self._indexAula

    @indexAula.setter
    def indexAula(self, indexAula):
        self._indexAula = indexAula

    # Constante
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            Qt.ItemDataRole.UserRole + 1: "nombre".encode(),
            Qt.ItemDataRole.UserRole + 2: "seleccionado".encode()
        }

    def rowCount(self, _parent: QModelIndex):
        return len(self.equipamientos)

    def data(self, index: QModelIndex, role: int):
        if not index.isValid(): return

        if role == Qt.ItemDataRole.UserRole + 1: # nombre
            return self.equipamientos[index.row()]
        elif role == Qt.ItemDataRole.UserRole + 2: # seleccionado
            # TODO: Esto tendría que ser basado en el índice del aula y usar el gestor, obvio
            return self.equipamientos[index.row()] in self.aula.equipamiento

    def setData(self, index: QModelIndex, value: Any, role: int):
        if not index.isValid(): return False

        if role == Qt.ItemDataRole.UserRole + 1: # nombre
            return False
        elif role == Qt.ItemDataRole.UserRole + 2: # seleccionado
            if value:
                self.aula.equipamiento.add(self.equipamientos[index.row()])
            else:
                # TODO: el gestor de datos borraría el equipamiento de la lista
                # general si no se usa en ningún aula (probablemente conviene
                # tener contadores de uso de equipamiento)
                self.aula.equipamiento.discard(self.equipamientos[index.row()])

            self.seleccionadosTextChanged.emit()

            return True

        return False

    def insertRows(self, row: int, count: int, _parent: QModelIndex):
        # TODO: Dejar nombre de equipamiento por defecto razonable y único
        # Inserta un solo elemento aún cuando count > 1
        self.beginInsertRows(_parent, row, row)
        self.equipamientos.insert(row, "Nuevo equipamiento")
        self.endInsertRows()
        return True

