import logging
from enum import IntEnum, auto
from datetime import time
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.GUI.modelos.list_selector_edificios_con_aulas import ListSelectorDeEdificiosConAulas
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Clase
from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    Día, RangoHorario, parse_string_horario_to_time, time_to_string_horario
)

logger = logging.getLogger(__name__)

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    día                     = Qt.ItemDataRole.UserRole + 1
    horario_inicio          = auto()
    horario_fin             = auto()
    virtual                 = auto()
    cantidad_de_alumnos     = auto()
    index_edificio_asignado = auto() # Este es el índice en la lista de edificios con aulas, no en la lista de todos los edificios
    index_aula_asignada     = auto() # i==0 representa ningún aula, i>0 representa el aula i-1
    no_cambiar_asignación   = auto()

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}

class ListClases(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.edificios_disponibles: ListSelectorDeEdificiosConAulas = ListSelectorDeEdificiosConAulas(None, self.gestor)
        self.i_carrera: int = 0 # Seteado por QT
        self.i_materia: int = 0 # Seteado por QT

    @pyqtProperty(int)
    def indexCarrera(self) -> int:
        return self.i_carrera

    @indexCarrera.setter
    def indexCarrera(self, indexCarrera: int):
        if indexCarrera >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexCarrera: %s', indexCarrera)
            self.i_carrera = indexCarrera

    @pyqtProperty(int)
    def indexMateria(self) -> int:
        return self.i_materia

    @indexMateria.setter
    def indexMateria(self, indexMateria: int):
        if indexMateria >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexMateria: %s', indexMateria)
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

        clase: Clase = self.gestor.get_clase(
            self.i_carrera, self.i_materia, index.row()
        )

        match role:
            case Rol.cantidad_de_alumnos:
                return clase.cantidad_de_alumnos

            case Rol.virtual:
                return clase.virtual

            case Rol.no_cambiar_asignación:
                return clase.no_cambiar_asignación

            case Rol.index_edificio_asignado: return(
                    self.edificios_disponibles.index_of(clase.aula_asignada.edificio)
                    if clase.aula_asignada else 0
                )

            case Rol.index_aula_asignada: return (
                clase.aula_asignada.edificio.aulas.index(clase.aula_asignada) + 1
                if clase.aula_asignada else 0
            )

            case Rol.día:
                return clase.día.value

            case Rol.horario_inicio:
                return time_to_string_horario(clase.horario.inicio)

            case Rol.horario_fin:
                return time_to_string_horario(clase.horario.fin)

            case _:
                logger.error('Rol desconocido: %s', role)
                return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False
        if role not in Rol:
            logger.error('Rol desconocido: %s', role)
            return False

        rol = Rol(role)
        logger.debug('Editando %s con el valor %s', rol.name, value)

        was_set: bool = self.try_to_set(index, value, rol)
        if was_set: self.dataChanged.emit(index, index, [role])
        return was_set

    def try_to_set(self, index: QModelIndex, value: Any, rol: Rol) -> bool:
        clase: Clase = self.gestor.get_clase(
            self.i_carrera, self.i_materia, index.row()
        )

        match rol:
            case Rol.cantidad_de_alumnos:
                return self.try_to_set_cantidad_de_alumnos(clase, value)

            case Rol.virtual:
                if not isinstance(value, bool):
                    logger.error(
                        'No se puede asignar el valor "%s" de tipo'
                        ' %s a "virtual", de tipo %s.',
                        value, type(value), bool
                    )
                    return False

                clase.virtual = value
                return True

            case Rol.no_cambiar_asignación:
                if not isinstance(value, bool):
                    logger.error(
                        'No se puede asignar el valor "%s" de tipo'
                        ' %s a "no cambiar asignación", de tipo %s.',
                        value, type(value), bool
                    )
                    return False

                clase.no_cambiar_asignación = value
                return True

            case Rol.index_edificio_asignado:
                if not isinstance(value, int):
                    logger.error(
                        'index_edificio_asignado recibió el valor "%s"'
                        ' de tipo %s, pero se esperaba un int.',
                        value, type(value)
                    )
                    return False
                
                self.edificios_disponibles.actualizar()
                if value >= self.edificios_disponibles.rowCount():
                    logger.error('index_edificio_asignado recibió un valor fuera de rango: %d', value)
                    return False
                
                i_edificio: int | None = self.edificios_disponibles[value]
                if i_edificio is None:
                    clase.aula_asignada = None
                else:
                    # Seleccionar la primer aula del edificio
                    clase.aula_asignada = self.gestor.get_aula(i_edificio, 0)
                return True

            case Rol.index_aula_asignada:
                if not isinstance(value, int):
                    logger.error(
                        'index_aula_asignada recibió el valor "%s" de tipo '
                        '%s, pero se esperaba un int.',
                        value, type(value)
                    )
                    return False
                elif value == 0:
                    clase.aula_asignada = None
                    return True
                elif clase.aula_asignada is None:
                    logger.error('No se puede seleccionar el aula sin seleccionar primero el edificio.')
                    return False
                elif value > len(clase.aula_asignada.edificio.aulas):
                    logger.error('index_aula_asignada recibió un valor fuera de rango para el edificio actual: %d', value)
                    return False
                else:
                    # Seleccionar otro aula del mismo edificio
                    edificio_actual = clase.aula_asignada.edificio
                    clase.aula_asignada = edificio_actual.aulas[value-1]
                    return True

            case Rol.día:
                if not isinstance(value, int):
                    logger.error(
                        'No se puede parsear como día un valor "%s"'
                        ' de tipo %s, se esperaba uno de tipo %s.',
                        value, type(value), int
                    )
                    return False
                if value not in Día:
                    logger.error(
                        'No se puede parsear como día un valor "%s",'
                        ' tiene que estar dentro del intervalo [0, 7).',
                        value
                    )
                    return False

                clase.día = Día(value)
                return True

            case Rol.horario_inicio | Rol.horario_fin:
                return self.try_to_set_horario_inicio_o_fin(
                    rol, clase.horario, value
                )

            case _:
                logger.error(
                    'Esto nunca debería ocurrir, '
                    'todos los roles deberían manejarse.'
                )
                return False

    def try_to_set_cantidad_de_alumnos(self, clase: Clase, value: str|Any) -> bool:

        if not isinstance(value, str):
            logger.error(
                'No se puede parsear como capacidad un valor "%s"'
                ' de tipo %s, se esperaba uno de tipo %s.',
                value, type(value), str
            )
            return False

        if value.isdigit():
            clase.cantidad_de_alumnos = int(value)
            return True

        # Es intuitivo interpretar input vacío como 0
        if value == '':
            clase.cantidad_de_alumnos = 0
            return True

        return False

    def try_to_set_horario_inicio_o_fin(
            self,
            rol: Rol,
            rango_horario: RangoHorario,
            value: str|Any
        ) -> bool:
        '''
        Asignar inicio o fin del rango horario si no resulta en un rango
        inválido (i.e.: con inicio >= fin).
        '''

        if not isinstance(value, str):
            logger.error(
                'No se puede parsear como horario un valor "%s"'
                ' de tipo %s, se esperaba uno de tipo %s.',
                value, type(value), str
            )
            return False

        horario: time = parse_string_horario_to_time(value)

        if rol == Rol.horario_inicio:
            if horario >= rango_horario.fin:
                return False

            rango_horario.inicio = horario
        else:
            if horario <= rango_horario.inicio:
                return False

            rango_horario.fin = horario

        return True

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
        Insertar clase "sin rellenar".

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
    
    @pyqtSlot()
    def resetModel(self):
        self.beginResetModel()
        self.endResetModel()
