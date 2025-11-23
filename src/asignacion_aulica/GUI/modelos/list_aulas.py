import logging
from datetime import time, datetime
from copy import copy
from typing import Any, Type, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import (
    Aula,
    RangoHorario
)

logger = logging.getLogger(__name__)

NOMBRES_DE_ROLES: list[str] = [
    'nombre',
    'capacidad',
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
ROL_CAPACIDAD:              int = ROL_BASE + NOMBRES_DE_ROLES.index('capacidad')
ROL_PRIMER_HORARIO:         int = ROL_BASE + NOMBRES_DE_ROLES.index('horario_inicio_lunes')
PARIDAD_ROL_HORARIO_INICIO: int = ROL_PRIMER_HORARIO % 2

def índice_semanal_de_rol_horario(rol: int) -> int:
    '''
    El índice semanal es 0 para el lunes y 6 para el domingo.
    Nota: devuelve valores raros para roles no horarios.
    '''
    return (rol - ROL_PRIMER_HORARIO) // 2

def es_rol_horario_inicio(rol: int) -> bool:
    return (rol % 2) == PARIDAD_ROL_HORARIO_INICIO

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    i + ROL_BASE: QByteArray(rolename.encode()) \
        for i, rolename in enumerate(NOMBRES_DE_ROLES)
}

EQUIVALENTE_24_HORAS: time = time.max
'''
'24:00' no puede parsearse como time, lo tratamos como si fuera `time.max`.
'''

def hay_type_mismatch(value: Any, tipo_esperado: Type) -> bool:
    if isinstance(value, tipo_esperado):
        return False

    logger.debug(f'Se esperaba asignar un valor de tipo {tipo_esperado}, pero'
                 f' en cambio se recibió uno de tipo {type(value)}')
    return True

class ListAulas(QAbstractListModel):
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.i_edificio: int = 0 # Seteado por QT

    # TODO: Mover ordenamiento al nivel de elemento de lista de edificios
    # (para que al ordenar también se actualizen los índices de las aulas dobles)
    @pyqtSlot()
    def ordenar(self):
        self.layoutAboutToBeChanged.emit()
        self.gestor.ordenar_aulas(self.i_edificio)
        self.layoutChanged.emit()

    @pyqtProperty(int)
    def indexEdificio(self) -> int:
        return self.i_edificio

    @indexEdificio.setter
    def indexEdificio(self, indexEdificio: int):
        if indexEdificio >= 0: # Ignorar cuando QT setea -1
            logger.info('Set indexEdificio: %s', indexEdificio)
            self.i_edificio = indexEdificio

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return self.gestor.cantidad_de_aulas(self.i_edificio)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None
        if role not in ROLES_A_NOMBRES_QT: return None

        aula: Aula = self.gestor.get_aula(self.i_edificio, index.row())

        if role == ROL_NOMBRE:
            return aula.nombre
        elif role == ROL_CAPACIDAD:
            return aula.capacidad
        else: # Es un rol horario
            índice_semanal: int = índice_semanal_de_rol_horario(role)
            rango_horario: RangoHorario = aula.horarios[índice_semanal]

            # Cuando el aula no especifica el horario, hacérselo saber a la UI
            if not rango_horario: return None

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

        aula: Aula = self.gestor.get_aula(self.i_edificio, index.row())
        roles_actualizados: list[int] = [role]

        if role == ROL_NOMBRE:
            if hay_type_mismatch(value, str):
                return False
            # Por un aparente bug de Qt, se edita 2 veces seguidas al apretar
            # Enter; lo ignoramos en vez de loguearlo
            if value.lower().strip() == aula.nombre.lower():
                return False

            if self.gestor.existe_aula(value):
                logger.debug(f'No se puede asignar el nombre "{value}", porque'
                              ' ya existe un aula con el mismo nombre')
                return False

            aula.nombre = value

        elif role == ROL_CAPACIDAD:
            if hay_type_mismatch(value, str):
                return False
            if not value.isdigit():
                return False

            aula.capacidad = int(value)

        else: # Es un rol horario
            if hay_type_mismatch(value, str):
                return False

            índice_semanal: int = índice_semanal_de_rol_horario(role)
            rango_horario: RangoHorario = aula.horarios[índice_semanal]

            # Si antes el aula no especificaba el horario, hacer que lo haga
            if not rango_horario:
                rango_horario = copy(aula.edificio.horarios[índice_semanal])
                aula.horarios[índice_semanal] = rango_horario
                # Actualizar el rol del otro extremo del rango horario
                roles_actualizados.append(
                    role+1 if es_rol_horario_inicio(role) else role-1
                )

            # Transformar string con formato HH:MM a time
            if value == '24:00':
                value = EQUIVALENTE_24_HORAS
            else:
                value = datetime.strptime(value, '%H:%M').time()

            if es_rol_horario_inicio(role):
                rango_horario.inicio = value
            else:
                rango_horario.fin = value

        self.dataChanged.emit(index, index, roles_actualizados)
        return True

    @override
    def removeRows(self, row: int, count: int, parent: QModelIndex|None = None) -> bool:
        '''Borra un solo elemento aún cuando count > 1.'''
        if parent is None: return False

        self.beginRemoveRows(parent, row, row)
        self.gestor.borrar_aula(self.i_edificio, row)
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

        actual_row = self.gestor.cantidad_de_aulas(self.i_edificio)
        self.beginInsertRows(parent, actual_row, actual_row)
        self.gestor.agregar_aula(self.i_edificio)
        self.endInsertRows()
        return True
