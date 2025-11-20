import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import fieldnames_Edificio

logger = logging.getLogger(__name__)

NOMBRES_DE_ROLES: dict[int, QByteArray] = {
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt
    i + Qt.ItemDataRole.UserRole + 1: QByteArray(campo.encode()) for i, campo in enumerate(fieldnames_Edificio)
}

def rol_a_índice(rol: int) -> int:
    return rol - Qt.ItemDataRole.UserRole - 1

class ListEdificios(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor

    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit()
        self.gestor.ordenar_edificios()
        self.layoutChanged.emit()

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return NOMBRES_DE_ROLES

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_edificios()

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        if role in NOMBRES_DE_ROLES:
            logger.debug(f"Obteniendo {NOMBRES_DE_ROLES[role]}")
            return self.gestor.get_from_edificio(index.row(), rol_a_índice(role))
        else:
            return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False

        if role in NOMBRES_DE_ROLES:
            logger.debug(f"Editando {NOMBRES_DE_ROLES[role]}")
            # TODO: validar value
            self.gestor.set_in_edificio(index.row(), rol_a_índice(role), value)
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    @override
    def removeRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''Borra un solo elemento aún cuando count > 1.'''
        if parent is None: return False

        self.beginRemoveRows(parent, row, row)
        self.gestor.borrar_edificio(row)
        self.endRemoveRows()
        return True

    @override
    def insertRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''
        Insertar edificio "sin rellenar".

        Inserta un solo elemento aún cuando count > 1, y lo inserta siempre al
        final independientemente del valor de row.
        '''
        if parent is None: return False

        actual_row = self.gestor.cantidad_de_edificios()
        self.beginInsertRows(parent, actual_row, actual_row)
        # TODO: validar value (ej.: no dejar insertar si ya hay un aula "sin rellenar")
        self.gestor.agregar_edificio()
        self.endInsertRows()
        return True
