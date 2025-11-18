from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSignal, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

CAMPO_AULA_EQUIPAMIENTO: int = 3

ROL_NOMBRE: int = Qt.ItemDataRole.UserRole + 1
ROL_SELECCIONADO: int = Qt.ItemDataRole.UserRole + 2
ROLE_NAMES: dict[int, QByteArray] = {
    ROL_NOMBRE: QByteArray("nombre".encode()),
    ROL_SELECCIONADO: QByteArray("seleccionado".encode())
}

class ListEquipamientosDeAula(QAbstractListModel):
    seleccionadosTextChanged: pyqtSignal = pyqtSignal()

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor

        # Cosas seteadas desde QT:
        self.i_edificio: int = 0
        self.i_aula: int = 0
        self.equipamientos_seleccionados: set[str] = set()

        self.equipamientos_posibles: list[str]
        self._actualizar_equipamientos_posibles()

    @pyqtProperty(str, notify=seleccionadosTextChanged)
    def seleccionadosText(self) -> str:
        if len(self.equipamientos_seleccionados) == 0:
            return "Ninguno"
        else:
            return ", ".join(self.equipamientos_seleccionados)

    @pyqtProperty(int)
    def indexEdificio(self) -> int:
        return self.i_edificio

    @indexEdificio.setter
    def indexEdificio(self, indexEdificio: int):
        self.i_edificio = indexEdificio
    
    @pyqtProperty(int)
    def indexAula(self) -> int:
        return self.i_aula

    @indexAula.setter
    def indexAula(self, indexAula: int):
        self.i_aula = indexAula
        self.equipamientos_seleccionados = self.gestor.get_from_aula(self.i_edificio, self.i_aula, CAMPO_AULA_EQUIPAMIENTO)

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLE_NAMES

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return len(self.equipamientos_posibles)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        if role == ROL_NOMBRE:
            return self.equipamientos_posibles[index.row()]
        elif role == ROL_SELECCIONADO:
            return self.equipamientos_posibles[index.row()] in self.equipamientos_seleccionados
        else:
            return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False

        if role == ROL_NOMBRE:
            # No tiene sentido renombrar equipamientos existentes
            return False
        elif role == ROL_SELECCIONADO:
            equipamiento = self.equipamientos_posibles[index.row()]
            if value:
                self.gestor.agregar_equipamiento_a_aula(self.i_edificio, self.i_aula, equipamiento)
            else:
                self.gestor.borrar_equipamiento_de_aula(self.i_edificio, self.i_aula, equipamiento)

            self.seleccionadosTextChanged.emit()
            return True
        else:
            return False

    # Función custom (en vez de insertRows) para poder poner un nombre
    # (es necesaria esta funcionalidad al no poder renombrar)
    @pyqtSlot(str, result=bool)
    def appendEquipamiento(self, name: str) -> bool:
        # TODO: más validaciones (en el gestor de datos directamente, creo)
        if not name:
            return False

        row_at_the_end = len(self.equipamientos)
        self.beginInsertRows(QModelIndex(), row_at_the_end, row_at_the_end)
        self.equipamientos.insert(row_at_the_end, name)
        self.endInsertRows()
        return True

    def _actualizar_equipamientos_posibles(self):
        self.equipamientos_posibles = self.gestor.get_equipamientos_existentes()
