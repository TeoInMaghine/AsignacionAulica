import logging
from datetime import time, datetime
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Edificio
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día, RangoHorario

logger = logging.getLogger(__name__)

NOMBRES_DE_ROLES: list[str] = [
    'nombre',
    'preferir_no_usar',
    'horario_inicio_lunes',
    'horario_fin_lunes',
    'horario_inicio_martes',
    'horario_fin_martes',
    'horario_inicio_miércoles',
    'horario_fin_miércoles',
    'horario_inicio_jueves',
    'horario_fin_jueves',
    'horario_inicio_viernes',
    'horario_fin_viernes',
    'horario_inicio_sábado',
    'horario_fin_sábado',
    'horario_inicio_domingo',
    'horario_fin_domingo'
]

# No se empieza desde 0 para no colisionar con los roles ya existentes de Qt
ROL_BASE:                   int = Qt.ItemDataRole.UserRole + 1
ROL_NOMBRE:                 int = ROL_BASE + NOMBRES_DE_ROLES.index('nombre')
ROL_PREFERIR_NO_USAR:       int = ROL_BASE + NOMBRES_DE_ROLES.index('preferir_no_usar')
ROL_PRIMER_HORARIO:         int = ROL_BASE + NOMBRES_DE_ROLES.index('horario_inicio_lunes')
PARIDAD_ROL_HORARIO_INICIO: int = ROL_PRIMER_HORARIO % 2

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    i + ROL_BASE: QByteArray(rolename.encode())
    for i, rolename in enumerate(NOMBRES_DE_ROLES)
}

EQUIVALENTE_24_HORAS: time = time.max
'''
'24:00' no puede parsearse como time, lo tratamos como si fuera `time.max`.
'''

def día_de_rol_horario(rol: int) -> Día:
    return Día((rol - ROL_PRIMER_HORARIO) // 2)

def es_rol_horario_inicio(rol: int) -> bool:
    return (rol % 2) == PARIDAD_ROL_HORARIO_INICIO

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
        if role not in ROLES_A_NOMBRES_QT: return None

        # TODO: Sandboxear llamadas al gestor? Está bueno crashear cuando
        # debugeamos pero en release quizás querríamos impedir eso
        edificio: Edificio = self.gestor.get_edificio(index.row())

        if role == ROL_NOMBRE:
            return edificio.nombre
        elif role == ROL_PREFERIR_NO_USAR:
            return edificio.preferir_no_usar
        else: # Es un rol horario
            día: Día = día_de_rol_horario(role)
            rango_horario: RangoHorario = edificio.horarios[día]
            horario: time = rango_horario.inicio \
                            if es_rol_horario_inicio(role) else \
                            rango_horario.fin

            # Transformar time a string con formato HH:MM
            if horario == EQUIVALENTE_24_HORAS:
                return '24:00'
            else:
                return horario.strftime('%H:%M')

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False
        if role not in ROLES_A_NOMBRES_QT: return False

        logger.debug(f'Editando {NOMBRES_DE_ROLES[role - ROL_BASE]}')
        edificio: Edificio = self.gestor.get_edificio(index.row())

        if role == ROL_NOMBRE:
            if not isinstance(value, str):
                logger.debug(
                    f'No se puede asignar el valor "{value}" de tipo'
                    f' {type(value)} al nombre, de tipo {str}.'
                )
                return False
            # Por un aparente bug de Qt, se edita 2 veces seguidas al apretar
            # Enter; lo ignoramos en vez de loguearlo
            if value.strip() == edificio.nombre:
                return False

            # Aceptamos cambiar la capitalización del nombre
            cambio_de_capitalización: bool = value.lower().strip() == edificio.nombre.lower()
            if not cambio_de_capitalización and self.gestor.existe_edificio(value):
                logger.debug(f'No se puede asignar el nombre "{value}", porque'
                              ' ya existe un edificio con el mismo nombre.')
                return False

            edificio.nombre = value.strip()

        elif role == ROL_PREFERIR_NO_USAR:
            if not isinstance(value, bool):
                logger.debug(
                    f'No se puede asignar el valor "{value}" de tipo'
                    f' {type(value)} a "preferir no usar", de tipo {bool}.'
                )
                return False

            edificio.preferir_no_usar = value

        else: # Es un rol horario
            if not isinstance(value, str):
                logger.debug(
                    f'No se puede parsear como horario un valor "{value}"'
                    f' de tipo {type(value)}, se esperaba uno de tipo {str}.'
                )
                return False

            día: Día = día_de_rol_horario(role)
            rango_horario: RangoHorario = edificio.horarios[día]

            # Transformar string con formato HH:MM a time
            if value == '24:00':
                value = EQUIVALENTE_24_HORAS
            else:
                value = datetime.strptime(value, '%H:%M').time()

            if es_rol_horario_inicio(role):
                rango_horario.inicio = value
            else:
                rango_horario.fin = value

        self.dataChanged.emit(index, index, [role])
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
