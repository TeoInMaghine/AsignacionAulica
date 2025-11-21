import logging
from datetime import time, datetime
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import (
    rolenames_Edificio,
    es_campo_horario_Edificio as es_campo_horario
)

logger = logging.getLogger(__name__)

NOMBRES_DE_ROLES: dict[int, QByteArray] = {
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt
    campo + Qt.ItemDataRole.UserRole + 1: QByteArray(rolename.encode()) \
        for campo, rolename in enumerate(rolenames_Edificio)
}

EQUIVALENTE_24_HORAS = time(23, 59, 59)

def rol_a_campo(rol: int) -> int:
    return rol - Qt.ItemDataRole.UserRole - 1

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
        return NOMBRES_DE_ROLES

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_edificios()

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None


        if role in NOMBRES_DE_ROLES:
            logger.debug(f"Obteniendo {NOMBRES_DE_ROLES[role]}")
            campo: int = rol_a_campo(role)
            valor_obtenido = self.gestor.get_from_edificio(index.row(), campo)

            # Transformar time a string con formato HH:MM
            if es_campo_horario[campo]:
                horario: time = valor_obtenido
                if horario == EQUIVALENTE_24_HORAS:
                    valor_obtenido = '24:00'
                else:
                    valor_obtenido = horario.strftime('%H:%M')

            return valor_obtenido
        else:
            return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False

        if role in NOMBRES_DE_ROLES:
            logger.debug(f"Editando {NOMBRES_DE_ROLES[role]}")
            campo: int = rol_a_campo(role)

            # Transformar string con formato HH:MM a time
            if es_campo_horario[campo]:
                if value == '24:00':
                    value = EQUIVALENTE_24_HORAS
                else:
                    value = datetime.strptime(value, "%H:%M").time()

            self.gestor.set_in_edificio(index.row(), campo, value)
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

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
        # TODO: validar value (ej.: no dejar insertar si ya hay un aula "sin rellenar")
        self.gestor.agregar_edificio()
        self.endInsertRows()
        return True
