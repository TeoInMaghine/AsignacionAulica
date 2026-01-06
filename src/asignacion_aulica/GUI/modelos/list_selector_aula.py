from enum import IntEnum, auto
import logging
from types import NoneType
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, QVariant, Qt, QModelIndex, QByteArray, pyqtSlot, pyqtProperty

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    nombre = Qt.ItemDataRole.UserRole + 1
    índice = auto()

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}

class ListSelectorDeAula(QAbstractListModel):
    '''
    Lista para el selector de aula.

    Es como ListAulas, pero agrega un item al principio de la lista para
    permitir seleccionar ningún aula.
    '''

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        
        # Seteado por QT
        self.texto_cuando_no_seleccionado: str = ''
        self.i_edificio: int|None = 0
    
    @pyqtProperty(str)
    def textoCuandoNoSeleccionado(self) -> str:
        return self.texto_cuando_no_seleccionado

    @textoCuandoNoSeleccionado.setter
    def textoCuandoNoSeleccionado(self, texto: str):
        self.texto_cuando_no_seleccionado = texto
    
    @pyqtProperty(QVariant) # int|None
    def indexEdificio(self) -> int|None:
        return self.i_edificio

    @indexEdificio.setter
    def indexEdificio(self, indexEdificio: int|None|Any):
        if not isinstance(indexEdificio, (int, NoneType)):
            logger.error('Invalid type for indexEdificio: %s %s', type(indexEdificio), indexEdificio)
        if indexEdificio is None or indexEdificio >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexEdificio: %s', indexEdificio)
            self.i_edificio = indexEdificio

    @pyqtSlot()
    def ordenar(self):
        if self.i_edificio is not None:
            self.layoutAboutToBeChanged.emit()
            self.gestor.ordenar_aulas(self.i_edificio)
            self.layoutChanged.emit()

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        if self.i_edificio is None:
            return 1
        else:
            return self.gestor.cantidad_de_aulas(self.i_edificio) + 1

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        
        i_aula: int|None = (
            None
            if self.i_edificio is None or index.row() == 0
            else index.row() - 1
        )
        
        match role:
            case Rol.nombre:
                return (
                    self.gestor.get_aula(self.i_edificio, i_aula).nombre
                    if i_aula is not None
                    else self.texto_cuando_no_seleccionado
                )
            case Rol.índice:
                return i_aula
            case _:
                logger.error('Rol desconocido: %s', role)
                return None
