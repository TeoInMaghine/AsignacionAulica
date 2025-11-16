import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import fieldnames_Aula

logger = logging.getLogger(__name__)

NOMBRES_DE_ROLES: dict[int, QByteArray] = {
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt
    i + Qt.ItemDataRole.UserRole + 1: QByteArray(campo.encode()) for i, campo in enumerate(fieldnames_Aula)
}

def rol_a_índice(rol: int) -> int:
    return rol - Qt.ItemDataRole.UserRole - 1

class ListAulas(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.i_edificio: int = 0 # Seteado por QT

    # TODO: Mover ordenamiento al nivel de elemento de lista de edificios
    # (para que al ordenar también se actualizen los índices de las aulas dobles)
    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit()
        self.gestor.ordenar_aulas(self.i_edificio)
        self.layoutChanged.emit()

    @pyqtProperty(int)
    def indexEdificio(self) -> int:
        return self.i_edificio

    @indexEdificio.setter
    def indexEdificio(self, indexEdificio: int):
        logger.info('Set indexEdificio: %s', indexEdificio)
        self.i_edificio = indexEdificio

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return NOMBRES_DE_ROLES

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_aulas(self.i_edificio)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        if role in NOMBRES_DE_ROLES:
            return self.gestor.get_from_aula(self.i_edificio, index.row(), rol_a_índice(role))
        else:
            return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False
        if role not in NOMBRES_DE_ROLES: return False

        # TODO: validar value
        if NOMBRES_DE_ROLES[role] == 'capacidad':
            if not value.isdigit(): return False
            value = int(value)

        self.gestor.set_in_aula(self.i_edificio, index.row(), rol_a_índice(role), value)
        self.dataChanged.emit(index, index, [role])
        return True

    @override
    def removeRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''Borra un solo elemento aún cuando count > 1.'''
        if parent is None: return False

        self.beginRemoveRows(parent, row, row)
        self.gestor.borrar_aula(self.i_edificio, row)
        self.endRemoveRows()
        return True

    @override
    def insertRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''
        Insertar aula "sin rellenar".

        Inserta un solo elemento aún cuando count > 1, y lo inserta siempre al
        final independientemente del valor de row.
        '''
        if parent is None: return False

        actual_row = self.gestor.cantidad_de_aulas(self.i_edificio)
        self.beginInsertRows(parent, actual_row, actual_row)
        # TODO: validar value (ej.: no dejar insertar si ya hay un aula "sin rellenar")
        self.gestor.agregar_aula(self.i_edificio)
        self.endInsertRows()
        return True
