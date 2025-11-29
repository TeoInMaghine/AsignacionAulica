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
    carrera_seleccionada_changed: pyqtSignal = pyqtSignal() #TODO: Esto no debería ser compartido entre instancias.

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor

        self.i_carrera: int = 0

        # Nombres de las carreras existentes.
        # Acordarse de actualizarla cuando puede haber cambios.
        self.carreras_existentes: list[str]
        self.actualizarLista()

    @pyqtProperty(str, notify=carrera_seleccionada_changed)
    def carreraSeleccionada(self) -> str:
        if 0 <= self.i_carrera < len(self.carreras_existentes):
            return self.carreras_existentes[self.i_carrera]
        else:
            return 'Ninguna'
    
    @pyqtProperty(int, notify=carrera_seleccionada_changed)
    def indexCarreraSeleccoinada(self) -> int:
        return self.i_carrera
        
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

    @pyqtSlot(str, result=bool)
    def agregarCarrera(self, nombre: str) -> bool:
        '''
        Agregar una carrera a la lista.
        '''
        nombre = nombre.strip()
        if not nombre:
            return False
        if self.gestor.existe_carrera(nombre):
            return False #TODO: Reaccionar a esto de alguna manera visible?

        self.i_carrera = self.gestor.agregar_carrera(nombre)
        self.actualizarLista()
        self.carrera_seleccionada_changed.emit()
        return True
    
    @pyqtSlot()
    def actualizarLista(self):
        logger.debug('Actualizando lista de carreras')
        self.beginResetModel()
        self.carreras_existentes = self.gestor.get_carreras()
        self.endResetModel()
