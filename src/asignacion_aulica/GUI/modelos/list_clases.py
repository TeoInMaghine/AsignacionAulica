import logging
from enum import IntEnum, auto
from datetime import time
from copy import copy
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Clase
from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    Día, RangoHorario, parse_string_horario_to_time, time_to_string_horario
)

logger = logging.getLogger(__name__)

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    día                   = Qt.ItemDataRole.UserRole + 1
    horario_inicio        = auto()
    horario_fin           = auto()
    virtual               = auto()
    cantidad_de_alumnos   = auto()
    aula_asignada         = auto()
    no_cambiar_asignación = auto()

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}


class ListClases(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.i_carrera: int = 0 # Seteado por QT
        self.i_materia: int = 0 # Seteado por QT

        # TODO: Placeholder, borrar eventualmente
        if not gestor.existe_carrera('Sin nombre'):
            gestor.agregar_carrera('Sin nombre')
            gestor.agregar_materia(self.i_carrera)

    @pyqtProperty(int)
    def indexCarrera(self) -> int:
        return self.i_carrera

    @indexCarrera.setter
    def indexCarrera(self, indexCarrera: int):
        if indexCarrera >= 0: # Ignorar cuando QT setea -1
            logger.info('Set indexCarrera: %s', indexCarrera)
            self.i_carrera = indexCarrera

    @pyqtProperty(int)
    def indexMateria(self) -> int:
        return self.i_materia

    @indexMateria.setter
    def indexMateria(self, indexMateria: int):
        if indexMateria >= 0: # Ignorar cuando QT setea -1
            logger.info('Set indexMateria: %s', indexMateria)
            self.i_materia = indexMateria

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_clases(self.i_carrera, self.i_materia)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        if role not in ROLES_A_NOMBRES_QT: return None

        rol = Rol(role)
        clase: Clase = self.gestor.get_clase(
            self.i_carrera, self.i_materia, index.row()
        )

        if rol == Rol.cantidad_de_alumnos:
            return clase.cantidad_de_alumnos

        elif rol == Rol.horario_inicio:
            return time_to_string_horario(clase.horario.inicio)

        elif rol == Rol.horario_fin:
            return time_to_string_horario(clase.horario.fin)

        else:
            logger.warn('F**k off mate')
            return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False
        if role not in ROLES_A_NOMBRES_QT: return False

        rol = Rol(role)
        logger.debug(f'Editando {rol.name}')

        was_set: bool = self.try_to_set(index, value, rol)
        if was_set: self.dataChanged.emit(index, index, [role])
        return was_set

    def try_to_set(self, index: QModelIndex, value: Any, rol: Rol) -> bool:
        clase: Clase = self.gestor.get_clase(
            self.i_carrera, self.i_materia, index.row()
        )
        value_no_es_string: bool = not isinstance(value, str)

        if rol == Rol.cantidad_de_alumnos:
            if value_no_es_string:
                logger.debug(
                    f'No se puede parsear como capacidad un valor "{value}"'
                    f' de tipo {type(value)}, se esperaba uno de tipo {str}.'
                )
                return False

            return self.try_to_set_cantidad_de_alumnos(clase, value)

        logger.error(
            'Esto nunca debería ocurrir, todos los roles deberían manejarse.'
        )
        return False

    def try_to_set_cantidad_de_alumnos(self, clase: Clase, value: str) -> bool:
        if value.isdigit():
            clase.cantidad_de_alumnos = int(value)
            return True

        # Es intuitivo interpretar input vacío como 0
        if value == '':
            clase.cantidad_de_alumnos = 0
            return True

        return False

    @override
    def removeRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''Borra un solo elemento aún cuando count > 1.'''
        if parent is None: return False

        self.beginRemoveRows(parent, row, row)
        self.gestor.borrar_clase(self.i_carrera, self.i_materia, row)
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

        actual_row = self.gestor.cantidad_de_clases(
            self.i_carrera, self.i_materia
        )
        self.beginInsertRows(parent, actual_row, actual_row)
        self.gestor.agregar_clase(self.i_carrera, self.i_materia)
        self.endInsertRows()
        return True
