import logging
from enum import IntEnum, auto
from datetime import time
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Edificio
from asignacion_aulica.gestor_de_datos.días_y_horarios import (
    Día, RangoHorario, parse_string_horario_to_time, time_to_string_horario
)

logger = logging.getLogger(__name__)

class RolHorario(IntEnum):
    inicio    = 0
    fin       = auto()
    cerrado   = auto()

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    horario_inicio_lunes        = Qt.ItemDataRole.UserRole + 1
    horario_fin_lunes           = auto()
    horario_cerrado_lunes       = auto()
    horario_inicio_martes       = auto()
    horario_fin_martes          = auto()
    horario_cerrado_martes      = auto()
    horario_inicio_miércoles    = auto()
    horario_fin_miércoles       = auto()
    horario_cerrado_miércoles   = auto()
    horario_inicio_jueves       = auto()
    horario_fin_jueves          = auto()
    horario_cerrado_jueves      = auto()
    horario_inicio_viernes      = auto()
    horario_fin_viernes         = auto()
    horario_cerrado_viernes     = auto()
    horario_inicio_sábado       = auto()
    horario_fin_sábado          = auto()
    horario_cerrado_sábado      = auto()
    horario_inicio_domingo      = auto()
    horario_fin_domingo         = auto()
    horario_cerrado_domingo     = auto()
    nombre                      = auto()
    preferir_no_usar            = auto()

    def desempacar_día_y_rol_horario(self) -> tuple[Día, RolHorario]:
        '''Sólo válido para roles de horarios.'''
        return (
            Día(       (self - Rol.horario_inicio_lunes) // len(RolHorario)),
            RolHorario((self - Rol.horario_inicio_lunes) %  len(RolHorario))
        )

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}


class ListEdificios(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor

    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit()
        self.gestor.ordenar_edificios()
        self.layoutChanged.emit()

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_edificios()

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        if role not in Rol: return None

        rol = Rol(role)
        # TODO: Sandboxear llamadas al gestor? Está bueno crashear cuando
        # debugeamos pero en release quizás querríamos impedir eso
        edificio: Edificio = self.gestor.get_edificio(index.row())

        if rol == Rol.nombre:
            return edificio.nombre
        elif rol == Rol.preferir_no_usar:
            return edificio.preferir_no_usar
        else: # Es un rol horario
            día, rol_horario = rol.desempacar_día_y_rol_horario()
            rango_horario: RangoHorario = edificio.horarios[día]

            if rol_horario == RolHorario.cerrado:
                return rango_horario.cerrado

            horario: time = (
                rango_horario.inicio if rol_horario == RolHorario.inicio else
                rango_horario.fin
            )

            return time_to_string_horario(horario)

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False
        if role not in Rol: return False

        rol = Rol(role)
        logger.debug('Editando %s con el valor %s', rol.name, value)

        was_set: bool = self.try_to_set(index, value, rol)
        if was_set: self.dataChanged.emit(index, index, [role])
        return was_set

    def try_to_set(self, index: QModelIndex, value: Any, rol: Rol) -> bool:
        edificio: Edificio = self.gestor.get_edificio(index.row())

        if rol == Rol.nombre:
            if not isinstance(value, str):
                logger.error(
                    'No se puede asignar el valor "%s" de tipo'
                    ' %s al nombre, de tipo %s.',
                    value, type(value), str
                )
                return False

            return self.try_to_set_nombre(edificio, value)

        if rol == Rol.preferir_no_usar:
            if not isinstance(value, bool):
                logger.error(
                    'No se puede asignar el valor "%s" de tipo'
                    ' %s a "preferir no usar", de tipo %s.',
                    value, type(value), bool
                )
                return False

            edificio.preferir_no_usar = value
            return True

        día, rol_horario = rol.desempacar_día_y_rol_horario()
        rango_horario: RangoHorario = edificio.horarios[día]

        if rol_horario == RolHorario.cerrado:
            if not isinstance(value, bool):
                logger.error(
                    'No se puede asignar el valor "%s" de tipo'
                    ' %s a "horario cerrado", de tipo %s.',
                    value, type(value), bool
                )
                return False

            rango_horario.cerrado = value
            return True

        if rol_horario == RolHorario.inicio or rol_horario == RolHorario.fin:
            if not isinstance(value, str):
                logger.error(
                    'No se puede parsear como horario un valor "%s"'
                    ' de tipo %s, se esperaba uno de tipo %s.',
                    value, type(value), str
                )
                return False

            return self.try_to_set_horario_inicio_o_fin(
                rol_horario, rango_horario, value
            )

        logger.error(
            'Esto nunca debería ocurrir, todos los roles deberían manejarse.'
        )
        return False

    def try_to_set_nombre(self, edificio: Edificio, value: str) -> bool:
        nuevo_nombre: str = value.strip()

        # Por un aparente bug de Qt, se edita 2 veces seguidas al apretar
        # Enter; lo ignoramos en vez de loguearlo
        if nuevo_nombre == edificio.nombre:
            return False

        # Aceptamos cambiar la capitalización del nombre
        cambio_de_capitalización: bool = nuevo_nombre.lower() == edificio.nombre.lower()
        if not cambio_de_capitalización and self.gestor.existe_edificio(nuevo_nombre):
            logger.debug(
                'No se puede asignar el nombre "%s", porque ya'
                ' existe un edificio con el mismo nombre.',
                nuevo_nombre
            )
            return False

        edificio.nombre = nuevo_nombre
        return True

    def try_to_set_horario_inicio_o_fin(
            self,
            rol_horario: RolHorario,
            rango_horario: RangoHorario,
            value: str
        ) -> bool:
        '''
        Asignar inicio o fin del rango horario si no resulta en un rango
        inválido (i.e.: con inicio >= fin).
        '''

        horario: time = parse_string_horario_to_time(value)

        if rol_horario == RolHorario.inicio:
            if horario >= rango_horario.fin:
                return False

            rango_horario.inicio = horario
        else:
            if rango_horario.inicio >= horario:
                return False

            rango_horario.fin = horario

        return True

    @override
    def removeRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''Borra un solo elemento aún cuando count > 1.'''
        if parent is None: return False

        self.beginRemoveRows(parent, row, row)
        self.gestor.borrar_edificio(row)
        self.endRemoveRows()
        return True

    @override
    def insertRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''
        Insertar edificio "sin rellenar".

        Inserta un solo elemento aún cuando count > 1, y lo inserta siempre al
        final independientemente del valor de row.
        '''
        if parent is None: return False

        actual_row = self.gestor.cantidad_de_edificios()
        self.beginInsertRows(parent, actual_row, actual_row)
        self.gestor.agregar_edificio()
        self.endInsertRows()
        return True
