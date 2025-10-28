from typing import Any
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSignal, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificio

class ListEquipamientos(QAbstractListModel):
    seleccionadosTextChanged: pyqtSignal = pyqtSignal()

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        # TODO: Esto es placeholder, falta usar el gestor de datos
        self.aula = Aula('B101', Edificio('Anasagasti'), 45)
        self.equipamientos = ["Proyector", "Computadoras", "No sé lol"]

    @pyqtProperty(str, notify=seleccionadosTextChanged)
    def seleccionadosText(self) -> str:
        if len(self.aula.equipamiento) == 0:
            return "Ninguno"

        return ",".join(self.aula.equipamiento)

    @pyqtProperty(int)
    def indexAula(self) -> int:
        return self._indexAula

    @indexAula.setter
    def indexAula(self, indexAula: int):
        self._indexAula = indexAula

    # Constante
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            Qt.ItemDataRole.UserRole + 1: "nombre".encode(),
            Qt.ItemDataRole.UserRole + 2: "seleccionado".encode()
        }

    def rowCount(self, _parent: QModelIndex) -> int:
        return len(self.equipamientos)

    def data(self, index: QModelIndex, role: int) -> Any:
        if not index.isValid(): return

        if role == Qt.ItemDataRole.UserRole + 1: # nombre
            return self.equipamientos[index.row()]
        elif role == Qt.ItemDataRole.UserRole + 2: # seleccionado
            # TODO: Esto tendría que ser basado en el índice del aula y usar el gestor, obvio
            return self.equipamientos[index.row()] in self.aula.equipamiento

    def setData(self, index: QModelIndex, value: Any, role: int) -> bool:
        if not index.isValid(): return False

        if role == Qt.ItemDataRole.UserRole + 1: # nombre
            # No hay capacidad de renombrar equipamientos existentes. Si
            # quisieramos, podríamos:
            # - Tener un dataclass Equipamiento que wrappee el string del
            #   nombre, así es mutable
            # - En Aula y Clase usar listas en vez de sets de equipamiento; porque si algo es
            #   mutable no es hasheable de forma segura
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

    # Función custom (en vez de insertRows) para poder poner un nombre
    # (es necesaria esta funcionalidad al no poder renombrar)
    @pyqtSlot(str, result=bool)
    def appendEquipamiento(self, name: str) -> bool:
        # TODO: validar (chequeos básicos y que no exista un equipamiento con
        # el mismo nombre)
        row_at_the_end = len(self.equipamientos)
        self.beginInsertRows(QModelIndex(), row_at_the_end, row_at_the_end)
        self.equipamientos.insert(row_at_the_end, name)
        self.endInsertRows()
        return True
