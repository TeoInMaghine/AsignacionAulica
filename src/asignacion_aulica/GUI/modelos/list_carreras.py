import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSignal, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

ROL_NOMBRE: int = Qt.ItemDataRole.UserRole + 1
ROLE_NAMES: dict[int, QByteArray] = {
    ROL_NOMBRE: QByteArray("nombre".encode())
}

class ListCarreras(QAbstractListModel):
    '''
    Esta clase conecta el selector de carreras de la GUI con el gestor datos.
    '''
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor

        # Nombres de las carreras existentes.
        # Acordarse de actualizarla cuando puede haber cambios.
        self.carreras_existentes: list[str]
        self.actualizarLista()
        
    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLE_NAMES

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return len(self.carreras_existentes)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        if role == ROL_NOMBRE:
            return self.carreras_existentes[index.row()]
        else:
            return None

    @pyqtSlot(str, result=int)
    def agregarCarrera(self, nombre: str) -> int:
        '''
        Agregar una nueva carrera a la lista.

        :return: Si se pudo agregar la carrera, su índice. Si no, un número
        negativo.
        '''
        nombre = nombre.strip()
        if not nombre:
            return -1
        if self.gestor.existe_carrera(nombre):
            return -2

        índice = self.gestor.agregar_carrera(nombre)
        self.actualizarLista()
        return índice
    
    @pyqtSlot()
    def actualizarLista(self):
        logger.debug('Actualizando lista de carreras')
        self.beginResetModel()
        self.carreras_existentes = self.gestor.get_carreras()
        self.endResetModel()
