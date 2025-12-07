from enum import IntEnum, auto
import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    nombre             = Qt.ItemDataRole.UserRole + 1
    edificio_preferido = auto()

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}

class ListCarreras(QAbstractListModel):
    '''
    Esta clase conecta el selector de carreras de la GUI con el gestor datos.
    '''
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        
    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_carreras()

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        la_carrera = self.gestor.get_carrera(index.row())

        match role:
            case Rol.nombre:
                return la_carrera.nombre
            case Rol.edificio_preferido if la_carrera.edificio_preferido is not None:
                return la_carrera.edificio_preferido.nombre
            case _:
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

        self.beginResetModel()
        índice = self.gestor.agregar_carrera(nombre)
        self.endResetModel()
        return índice
    
    @pyqtSlot(int, str, result=int)
    def cambiarNombre(self, índice: int, nuevo_nombre: str) -> int:
        '''
        Cambiar el nombre de una carrera existente.

        :return: El nuevo índice de la carrera.
        '''
        n_carreras = self.rowCount()
        if 0 <= índice < n_carreras:
            self.beginResetModel()
            try:
                nuevo_índice = self.gestor.set_carrera_nombre(índice, nuevo_nombre)
            except ValueError:
                # Ignorar el error si el nuevo nombre no era válido
                return índice
            else:
                return nuevo_índice
            finally:
                self.endResetModel()
        else:
            # Índices inválidos: dejar seleccionada la última carrera
            # o -1 si no hay carreras.
            return n_carreras - 1
            
    @pyqtSlot(int, result=int)
    def borrarCarrera(self, índice: int) -> int:
        '''
        Borrar una carrera del gestor de datos.

        :return: El índice de la carrera que debería quedar seleccionada, 0 -1
        si no quedan carreras.
        '''
        n_carreras = self.rowCount()
        if 0 <= índice < n_carreras:
            self.beginResetModel()
            self.gestor.borrar_carrera(índice)
            self.endResetModel()
            # Mantener el mismo índice, excepto que quede fuera de rango y ahí
            # dejamos seleccionada la última carrera de la lista o -1 si no
            # quedó ninguna carrera.
            return min(índice, self.rowCount() - 1)
        else:
            # Índices inválidos: dejar seleccionada la última carrera
            # o -1 si no hay carreras.
            return n_carreras - 1
    
    @pyqtSlot(int, int)
    def setEdificioPreferido(self, i_carrera: int, i_edificio: int):
        '''
        Setear el edificio preferido de una carrera.

        :param i_carrera: El índice de la carrera.
        :param i_edificio: El índice del nuevo edificio preferido, o -1 para
        borrar el edificio preferido.
        '''
        if not 0 <= i_carrera < self.rowCount():
            logger.error('Set edificio preferido con carrera fuera de rango.')
        elif i_edificio >= self.gestor.cantidad_de_edificios():
            logger.error('Set edificio preferido con edificio fuera de rango.')
        else:
            edificio = (
                self.gestor.get_edificio(i_edificio)
                if i_edificio >= 0
                else None
            )
            self.gestor.get_carrera(i_carrera).edificio_preferido = edificio
