from enum import IntEnum, auto
import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtSlot, pyqtProperty

from asignacion_aulica.gestor_de_datos.entidades import Edificio
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

class Rol(IntEnum):
    # No se empieza desde 0 para no colisionar con los roles ya existentes de Qt.
    nombre = Qt.ItemDataRole.UserRole + 1
    índice = auto()

ROLES_A_NOMBRES_QT: dict[int, QByteArray] = {
    rol.value: QByteArray(rol.name.encode())
    for rol in Rol
}

class ListSelectorDeEdificiosConAulas(QAbstractListModel):
    '''
    Lista de edificios para el editor de aula asignada.

    Es como ListSelectorDeEdificios, pero solamente muestra los edificios que
    tienen aulas.
    '''

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
        self.índices_de_edificios_con_aulas: list[int] = []
        
        # Seteado por QT
        self.texto_cuando_no_seleccionado: str = ''
    
    @pyqtProperty(str)
    def textoCuandoNoSeleccionado(self) -> str:
        return self.texto_cuando_no_seleccionado

    @textoCuandoNoSeleccionado.setter
    def textoCuandoNoSeleccionado(self, texto: str):
        self.texto_cuando_no_seleccionado = texto

    @pyqtSlot()
    def actualizar(self):
        self.layoutAboutToBeChanged.emit()

        self.gestor.ordenar_edificios()
        self.índices_de_edificios_con_aulas = [
            i_edificio
            for i_edificio in range(self.gestor.cantidad_de_edificios())
            if self.gestor.cantidad_de_aulas(i_edificio) > 0
        ]

        self.layoutChanged.emit()

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLES_A_NOMBRES_QT

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        '''
        Nota: hay que actualizar la lista antes de usar esto.
        '''
        return len(self.índices_de_edificios_con_aulas) + 1

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        i_edificio: int|None = self[index.row()]
        
        match role:
            case Rol.nombre:
                return (
                    self.gestor.get_edificio(i_edificio).nombre
                    if i_edificio is not None
                    else self.texto_cuando_no_seleccionado
                )
            case Rol.índice:
                return i_edificio
            case _:
                logger.error('Rol desconocido: %s', role)
                return None
    
    def index_of(self, edificio: Edificio) -> int|None:
        '''
        :return: El índice del edificio dado en esta lista, o 0 (que equivale a
        no tener edificio seleccionado) si el edificio no está en la lista.
        '''
        logger.debug('index_of %s', edificio.nombre)
        self.actualizar()
        índice_en_el_gestor = self.gestor.índice_del_edificio(edificio)
        logger.debug('índice_en_el_gestor: %s', índice_en_el_gestor)
        try:
            índice_en_esta_lista = self.índices_de_edificios_con_aulas.index(índice_en_el_gestor) + 1
            logger.debug('índice_en_esta_lista: %s', índice_en_esta_lista)
            return índice_en_esta_lista
        except ValueError:
            return 0
    
    def __getitem__(self, index: int) -> int|None:
        '''
        :return: El índice que tiene en el gestor de datos el elemento que en
        esta lista tiene el índice `index`, o `None` si `index==0`.

        Nota: hay que actualizar la lista antes de usar esto.
        '''
        if index == 0: return None
        else: return self.índices_de_edificios_con_aulas[index-1]
