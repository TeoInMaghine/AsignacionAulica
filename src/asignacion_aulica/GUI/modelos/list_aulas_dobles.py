import logging
from enum import IntEnum, auto
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos, aula_no_seleccionada
from asignacion_aulica.gestor_de_datos.entidades import Aula, AulaDoble

logger = logging.getLogger(__name__)

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    index_aula_grande  = Qt.ItemDataRole.UserRole + 1
    index_aula_chica_1 = auto()
    index_aula_chica_2 = auto()

ÍNDICE_CUANDO_NO_SELECCIONADO: int = 0

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}


class ListAulasDobles(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.i_edificio: int = 0 # Seteado por QT

    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit([], self.LayoutChangeHint.VerticalSortHint)
        self.gestor.ordenar_aulas_dobles(self.i_edificio)
        self.layoutChanged.emit([], self.LayoutChangeHint.VerticalSortHint)

    @pyqtProperty(int)
    def indexEdificio(self) -> int:
        return self.i_edificio

    @indexEdificio.setter
    def indexEdificio(self, indexEdificio: int):
        if indexEdificio >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexEdificio: %s', indexEdificio)
            self.i_edificio = indexEdificio

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_aulas_dobles(self.i_edificio)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        if role not in Rol:
            logger.error('Rol desconocido: %s', role)
            return None

        rol = Rol(role)
        aula_doble: AulaDoble = self.gestor.get_aula_doble(
            self.i_edificio, index.row()
        )

        aula: Aula
        match rol:
            case Rol.index_aula_grande:
                aula = aula_doble.aula_grande
            case Rol.index_aula_chica_1:
                aula = aula_doble.aula_chica_1
            case Rol.index_aula_chica_2:
                aula = aula_doble.aula_chica_2

        return (
            aula.edificio.aulas.index(aula) + 1
            if aula is not aula_no_seleccionada else
            ÍNDICE_CUANDO_NO_SELECCIONADO
        )

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False
        if role not in Rol:
            logger.error('Rol desconocido: %s', role)
            return None

        rol = Rol(role)
        logger.debug('Editando %s con el valor %s', rol.name, value)
        aula_doble: AulaDoble = self.gestor.get_aula_doble(
            self.i_edificio, index.row()
        )

        if not isinstance(value, int):
            logger.error(
                '%s recibió el valor "%s" de tipo %s, pero se esperaba un int.',
                rol.name, value, type(value)
            )
            return False

        if value > self.gestor.cantidad_de_aulas(self.i_edificio):
            logger.error(
                '%s recibió un valor fuera de rango para el edificio actual: %d',
                rol.name, value
            )
            return False

        aula: Aula = (
            aula_no_seleccionada
            if value == ÍNDICE_CUANDO_NO_SELECCIONADO else
            self.gestor.get_aula(self.i_edificio, value-1)
        )

        match rol:
            case Rol.index_aula_grande:
                aula_doble.aula_grande = aula
            case Rol.index_aula_chica_1:
                aula_doble.aula_chica_1 = aula
            case Rol.index_aula_chica_2:
                aula_doble.aula_chica_2 = aula

        self.dataChanged.emit(index, index, [role])
        return True

    @override
    def removeRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''Borra un solo elemento aún cuando count > 1.'''
        if parent is None: return False

        self.beginRemoveRows(parent, row, row)
        self.gestor.borrar_aula_doble(self.i_edificio, row)
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

        actual_row = self.gestor.cantidad_de_aulas_dobles(self.i_edificio)
        self.beginInsertRows(parent, actual_row, actual_row)
        self.gestor.agregar_aula_doble(self.i_edificio)
        self.endInsertRows()
        return True
