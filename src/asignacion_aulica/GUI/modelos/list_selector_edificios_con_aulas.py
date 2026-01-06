from enum import IntEnum, auto
import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtSlot, pyqtProperty

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

class ListSelectorDeEdificiosConAulas(QAbstractListModel):
    '''
    Lista de edificios para el editor de aula asignada.

    Es como ListSelectorDeEdificios, pero solamente muestra los edificios que
    tienen aulas.
    '''

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.índices_de_edificios_con_aulas: list[int] = []
        
        # Seteado por QT
        self.texto_cuando_no_seleccionado: str = ''
    
    @pyqtProperty(str)
    def textoCuandoNoSeleccionado(self) -> str:
        return self.texto_cuando_no_seleccionado

    @textoCuandoNoSeleccionado.setter
    def textoCuandoNoSeleccionado(self, texto: str):
        self.texto_cuando_no_seleccionado = texto

    @pyqtSlot()
    def actualizar(self):
        self.layoutAboutToBeChanged.emit()

        self.gestor.ordenar_edificios()
        self.índices_de_edificios_con_aulas = [
            i_edificio
            for i_edificio in range(self.gestor.cantidad_de_edificios())
            if self.gestor.cantidad_de_aulas(i_edificio) > 0
        ]

        self.layoutChanged.emit()

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return len(self.índices_de_edificios_con_aulas) + 1

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        i_edificio: int|None = (
            None if index.row() == 0
            else self.índices_de_edificios_con_aulas[index.row()-1]
        )
        
        match role:
            case Rol.nombre:
                return (
                    self.gestor.get_edificio(i_edificio).nombre
                    if i_edificio is not None
                    else self.texto_cuando_no_seleccionado
                )
            case Rol.índice:
                return i_edificio
            case _:
                logger.error('Rol desconocido: %s', role)
                return None
