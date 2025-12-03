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
        self._actualizarLista()
        
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
        self._actualizarLista()
        return índice
    
    @pyqtSlot(int, str, result=int)
    def cambiarNombre(self, índice: int, nuevo_nombre: str) -> int:
        '''
        Cambiar el nombre de una carrera existente.

        :return: El nuevo índice de la carrera.
        '''
        # Índices inválidos: dejar seleccionada la última carrera
        # o -1 si no hay carreras.
        if índice < 0 or índice >= len(self.carreras_existentes):
            return len(self.carreras_existentes) - 1
        else:
            try:
                nuevo_índice = self.gestor.set_carrera_nombre(índice, nuevo_nombre)
            except ValueError:
                # Ignorar el error si el nuevo nombre no era válido
                return índice
            else:
                self._actualizarLista()
                return nuevo_índice
    
    @pyqtSlot(int, result=int)
    def borrarCarrera(self, índice: int) -> int:
        '''
        Borrar una carrera del gestor de datos.

        :return: El índice de la carrera que debería quedar seleccionada, 0 -1
        si no quedan carreras.
        '''
        # Índices inválidos: dejar seleccionada la última carrera
        # o -1 si no hay carreras.
        if índice < 0 or índice >= len(self.carreras_existentes):
            return len(self.carreras_existentes) - 1
        else:
            self.gestor.borrar_carrera(índice)
            self._actualizarLista()
            # Mantener el mismo índice, excepto que quede fuera de rango y ahí
            # dejamos seleccionada la última carrera de la lista o -1 si no
            # quedó ninguna carrera.
            return min(índice, len(self.carreras_existentes) - 1)

    def _actualizarLista(self):
        logger.debug('Actualizando lista de carreras')
        self.beginResetModel()
        self.carreras_existentes = self.gestor.get_carreras()
        self.endResetModel()
