import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtSlot, pyqtProperty

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

ROL_NOMBRE: int = Qt.ItemDataRole.UserRole + 1
ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    ROL_NOMBRE: QByteArray('nombre'.encode())
}

class ListSelectorDeEdificios(QAbstractListModel):
    '''
    Lista para el selector de edificios.

    Es como ListEdificios, pero agrega un item al principio de la lista para
    permitir seleccionar ningún edificio.
    '''

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        
        # Seteado por QT
        self.texto_cuando_no_seleccionado: str = ''
    
    @pyqtProperty(str)
    def textoCuandoNoSeleccionado(self) -> str:
        return self.texto_cuando_no_seleccionado

    @textoCuandoNoSeleccionado.setter
    def textoCuandoNoSeleccionado(self, texto: str):
        self.texto_cuando_no_seleccionado = texto

    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit([], self.LayoutChangeHint.VerticalSortHint)
        self.gestor.ordenar_edificios()
        self.layoutChanged.emit([], self.LayoutChangeHint.VerticalSortHint)

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_edificios() + 1

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        if role not in ROLES_A_NOMBRES_QT: return None

        índice = index.row() - 1
        if índice < 0:
            return self.texto_cuando_no_seleccionado
        else:
            return self.gestor.get_edificio(índice).nombre
