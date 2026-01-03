import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtSlot, pyqtProperty

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

ROL_NOMBRE: int = Qt.ItemDataRole.UserRole + 1
ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    ROL_NOMBRE: QByteArray('nombre'.encode())
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
        self.i_edificio: int = 0
    
    @pyqtProperty(str)
    def textoCuandoNoSeleccionado(self) -> str:
        return self.texto_cuando_no_seleccionado

    @textoCuandoNoSeleccionado.setter
    def textoCuandoNoSeleccionado(self, texto: str):
        self.texto_cuando_no_seleccionado = texto
    
    @pyqtProperty(int)
    def indexEdificio(self) -> int:
        return self.i_edificio

    @indexEdificio.setter
    def indexEdificio(self, indexEdificio: int):
        if indexEdificio >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexEdificio: %s', indexEdificio)
            self.i_edificio = indexEdificio

    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit()
        self.gestor.ordenar_aulas(self.i_edificio)
        self.layoutChanged.emit()

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_aulas(self.i_edificio) + 1

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        if role not in ROLES_A_NOMBRES_QT: return None

        índice = index.row() - 1
        if índice < 0:
            return self.texto_cuando_no_seleccionado
        else:
            return self.gestor.get_aula(self.i_edificio, índice).nombre
