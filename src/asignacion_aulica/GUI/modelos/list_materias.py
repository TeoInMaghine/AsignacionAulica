import logging
from enum import IntEnum, auto
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Materia

logger = logging.getLogger(__name__)

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    nombre = Qt.ItemDataRole.UserRole + 1
    año    = auto()

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}


class ListMaterias(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.i_carrera: int = 0 # Seteado por QT

        # TODO: Placeholder, borrar eventualmente
        if not gestor.existe_carrera('Sin nombre'):
            gestor.agregar_carrera('Sin nombre')

    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit()
        self.gestor.ordenar_materias(self.i_carrera)
        self.layoutChanged.emit()

    @pyqtProperty(int)
    def indexCarrera(self) -> int:
        return self.i_carrera

    @indexCarrera.setter
    def indexCarrera(self, indexCarrera: int):
        if indexCarrera >= 0: # Ignorar cuando QT setea -1
            logger.info('Set indexCarrera: %s', indexCarrera)
            self.i_carrera = indexCarrera

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_materias(self.i_carrera)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        if role not in ROLES_A_NOMBRES_QT: return None

        rol = Rol(role)
        materia: Materia = self.gestor.get_materia(self.i_carrera, index.row())

        if rol == Rol.nombre:
            return materia.nombre

        if rol == Rol.año:
            return materia.año

        logger.error(
            'Esto nunca debería ocurrir, todos los roles deberían manejarse.'
        )
        return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False
        if role not in ROLES_A_NOMBRES_QT: return False

        rol = Rol(role)
        logger.debug(f'Editando {rol.name} con el valor {value}')

        was_set: bool = self.try_to_set(index, value, rol)
        if was_set: self.dataChanged.emit(index, index, [role])
        return was_set

    def try_to_set(self, index: QModelIndex, value: Any, rol: Rol) -> bool:
        materia: Materia = self.gestor.get_materia(self.i_carrera, index.row())

        if rol == Rol.nombre:
            if not isinstance(value, str):
                logger.error(
                    f'No se puede asignar el valor "{value}" de tipo'
                    f' {type(value)} al nombre, de tipo {str}.'
                )
                return False

            return self.try_to_set_nombre(materia, value)

        if rol == Rol.año:
            if not isinstance(value, str):
                logger.error(
                    f'No se puede parsear como año un valor "{value}"'
                    f' de tipo {type(value)}, se esperaba uno de tipo {str}.'
                )
                return False

            return self.try_to_set_año(materia, value)

        logger.error(
            'Esto nunca debería ocurrir, todos los roles deberían manejarse.'
        )
        return False

    def try_to_set_año(self, materia: Materia, value: str) -> bool:
        if value.isdigit():
            materia.año = int(value)
            return True

        # Es intuitivo interpretar input vacío como 0
        if value == '':
            materia.año = 0
            return True

        return False

    def try_to_set_nombre(self, materia: Materia, value: str) -> bool:
        nuevo_nombre: str = value.strip()

        # Por un aparente bug de Qt, se edita 2 veces seguidas al apretar
        # Enter; lo ignoramos en vez de loguearlo
        if nuevo_nombre == materia.nombre:
            return False

        # Aceptamos cambiar la capitalización del nombre
        cambio_de_capitalización: bool = nuevo_nombre.lower() == materia.nombre.lower()
        if not cambio_de_capitalización and self.gestor.existe_materia(self.i_carrera, nuevo_nombre):
            logger.debug(
                f'No se puede asignar el nombre "{nuevo_nombre}", porque ya'
                ' existe una materia en la misma carrera con el mismo nombre.'
            )
            return False

        materia.nombre = nuevo_nombre
        return True

    @override
    def removeRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''Borra un solo elemento aún cuando count > 1.'''
        if parent is None: return False

        self.beginRemoveRows(parent, row, row)
        self.gestor.borrar_materia(self.i_carrera, row)
        self.endRemoveRows()
        return True

    @override
    def insertRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''
        Insertar materia "sin rellenar".

        Inserta un solo elemento aún cuando count > 1, y lo inserta siempre al
        final independientemente del valor de row.
        '''
        if parent is None: return False

        actual_row = self.gestor.cantidad_de_materias(self.i_carrera)
        self.beginInsertRows(parent, actual_row, actual_row)
        self.gestor.agregar_materia(self.i_carrera)
        self.endInsertRows()
        return True
