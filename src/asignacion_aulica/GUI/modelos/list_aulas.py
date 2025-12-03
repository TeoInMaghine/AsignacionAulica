import logging
from enum import IntEnum, auto
from datetime import time, datetime
from copy import copy
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.gestor_de_datos.entidades import Aula
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día, RangoHorario

logger = logging.getLogger(__name__)

class RolHorario(IntEnum):
    inicio    = 0
    fin       = auto()
    cerrado   = auto()
    es_propio = auto()

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    horario_inicio_lunes        = Qt.ItemDataRole.UserRole + 1
    horario_fin_lunes           = auto()
    horario_cerrado_lunes       = auto()
    horario_es_propio_lunes     = auto()
    horario_inicio_martes       = auto()
    horario_fin_martes          = auto()
    horario_cerrado_martes      = auto()
    horario_es_propio_martes    = auto()
    horario_inicio_miércoles    = auto()
    horario_fin_miércoles       = auto()
    horario_cerrado_miércoles   = auto()
    horario_es_propio_miércoles = auto()
    horario_inicio_jueves       = auto()
    horario_fin_jueves          = auto()
    horario_cerrado_jueves      = auto()
    horario_es_propio_jueves    = auto()
    horario_inicio_viernes      = auto()
    horario_fin_viernes         = auto()
    horario_cerrado_viernes     = auto()
    horario_es_propio_viernes   = auto()
    horario_inicio_sábado       = auto()
    horario_fin_sábado          = auto()
    horario_cerrado_sábado      = auto()
    horario_es_propio_sábado    = auto()
    horario_inicio_domingo      = auto()
    horario_fin_domingo         = auto()
    horario_cerrado_domingo     = auto()
    horario_es_propio_domingo   = auto()
    nombre                      = auto()
    capacidad                   = auto()

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

ROLES_DEL_DÍA: tuple[tuple[int, ...], ...] = tuple(
    tuple(Rol.horario_inicio_lunes + len(RolHorario) * día + i for i in RolHorario)
    for día in Día
)

EQUIVALENTE_24_HORAS: time = time.max
'''
'24:00' no puede parsearse como time, lo tratamos como si fuera `time.max`.
'''

def parse_string_horario_to_time(value: str) -> time:
    '''
    Transformar string con formato HH:MM a time.
    '''
    if value == '24:00':
        return EQUIVALENTE_24_HORAS

    return datetime.strptime(value, '%H:%M').time()


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

        rol = Rol(role)
        aula: Aula = self.gestor.get_aula(self.i_edificio, index.row())

        if rol == Rol.nombre:
            return aula.nombre
        elif rol == Rol.capacidad:
            return aula.capacidad
        else: # Es un rol horario
            día, rol_horario = rol.desempacar_día_y_rol_horario()
            rango_horario: RangoHorario|None = aula.horarios[día]

            if rol_horario == RolHorario.es_propio:
                return rango_horario is not None

            if not rango_horario:
                logger.warning(
                    'Esto nunca debería ocurrir, se debe verificar que el'
                    ' horario sea propio antes de acceder al mismo.'
                    f' Rol obtenido: {rol.name}.'
                )
                return None

            if rol_horario == RolHorario.cerrado:
                return rango_horario.cerrado

            horario: time = (
                rango_horario.inicio if rol_horario == RolHorario.inicio else
                rango_horario.fin
            )

            # Transformar time a string con formato HH:MM
            if horario == EQUIVALENTE_24_HORAS:
                return '24:00'
            else:
                return horario.strftime('%H:%M')

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
        aula: Aula = self.gestor.get_aula(self.i_edificio, index.row())
        value_no_es_string: bool = not isinstance(value, str)

        if rol == Rol.nombre:
            if value_no_es_string:
                logger.debug(
                    f'No se puede asignar el valor "{value}" de tipo'
                    f' {type(value)} al nombre, de tipo {str}.'
                )
                return False

            return self.try_to_set_nombre(aula, value)

        if rol == Rol.capacidad:
            if value_no_es_string:
                logger.debug(
                    f'No se puede parsear como capacidad un valor "{value}"'
                    f' de tipo {type(value)}, se esperaba uno de tipo {str}.'
                )
                return False

            return self.try_to_set_capacidad(aula, value)

        # Es un rol horario
        día, rol_horario = rol.desempacar_día_y_rol_horario()

        if rol_horario == RolHorario.es_propio:
            if value != True:
                logger.debug(
                    f'El valor "{value}" de tipo {type(value)} no es '
                    f'válido para "horario es propio", sólo admite {True}.'
                )
                return False

            aula.horarios[día] = None
            return True

        rango_horario: RangoHorario|None = aula.horarios[día]

        # Si el horario del aula no era propio, hacerlo propio antes de editar
        if not rango_horario:
            rango_horario = copy(aula.edificio.horarios[día])
            aula.horarios[día] = rango_horario
            self.dataChanged.emit(index, index, ROLES_DEL_DÍA[día])

        if rol_horario == RolHorario.cerrado:
            if not isinstance(value, bool):
                logger.debug(
                    f'No se puede asignar el valor "{value}" de tipo'
                    f' {type(value)} a "horario cerrado", de tipo {bool}.'
                )
                return False

            rango_horario.cerrado = value
            return True

        if rol_horario == RolHorario.inicio or rol_horario == RolHorario.fin:
            if value_no_es_string:
                logger.debug(
                    f'No se puede parsear como horario un valor "{value}"'
                    f' de tipo {type(value)}, se esperaba uno de tipo {str}.'
                )
                return False

            return self.try_to_set_horario_inicio_o_fin(
                rol_horario, rango_horario, value
            )

        logger.warning(
            'Esto nunca debería ocurrir, todos los roles deberían manejarse.'
        )
        return False

    def try_to_set_nombre(self, aula: Aula, value: str) -> bool:
        # Por un aparente bug de Qt, se edita 2 veces seguidas al apretar
        # Enter; lo ignoramos en vez de loguearlo
        if value.strip() == aula.nombre:
            return False

        # Aceptamos cambiar la capitalización del nombre
        cambio_de_capitalización: bool = value.lower().strip() == aula.nombre.lower()
        if not cambio_de_capitalización and self.gestor.existe_aula(self.i_edificio, value):
            logger.debug(
                f'No se puede asignar el nombre "{value}", porque ya'
                ' existe un aula en el mismo edificio con el mismo nombre.'
            )
            return False

        aula.nombre = value.strip()
        return True

    def try_to_set_capacidad(self, aula: Aula, value: str) -> bool:
        if value.isdigit():
            aula.capacidad = int(value)
            return True

        # Es intuitivo interpretar input vacío como 0
        if value == '':
            aula.capacidad = 0
            return True

        return False

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
            return True

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
