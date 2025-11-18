import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSignal, pyqtSlot

from asignacion_aulica.gestor_de_datos.entidades import fieldnames_Aula
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

CAMPO_AULA_EQUIPAMIENTO: int = fieldnames_Aula.index('equipamiento')

ROL_NOMBRE: int = Qt.ItemDataRole.UserRole + 1
ROL_SELECCIONADO: int = Qt.ItemDataRole.UserRole + 2
ROLE_NAMES: dict[int, QByteArray] = {
    ROL_NOMBRE: QByteArray("nombre".encode()),
    ROL_SELECCIONADO: QByteArray("seleccionado".encode())
}

class ListEquipamientosDeAula(QAbstractListModel):
    seleccionadosTextChanged: pyqtSignal = pyqtSignal() #TODO: Esto no debería ser compartido entre instancias.

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor

        # Cosas seteadas desde QT:
        self.i_edificio: int = 0
        self.i_aula: int = 0
        self.equipamientos_seleccionados: set[str]
        self._set_equipamientos_seleccionados()

        self.equipamientos_posibles: list[str]
        self._actualizar_equipamientos_posibles()

    @pyqtProperty(str, notify=seleccionadosTextChanged)
    def seleccionadosText(self) -> str:
        if len(self.equipamientos_seleccionados) == 0:
            return "Ninguno"
        else:
            seleccionados_en_orden_alfabético = list(self.equipamientos_seleccionados)
            seleccionados_en_orden_alfabético.sort()
            return ", ".join(seleccionados_en_orden_alfabético)

    @pyqtProperty(int)
    def indexEdificio(self) -> int:
        return self.i_edificio

    @indexEdificio.setter
    def indexEdificio(self, indexEdificio: int):
        self.i_edificio = indexEdificio
        self._set_equipamientos_seleccionados()
        self.seleccionadosTextChanged.emit()
    
    @pyqtProperty(int)
    def indexAula(self) -> int:
        return self.i_aula

    @indexAula.setter
    def indexAula(self, indexAula: int):
        self.i_aula = indexAula
        self._set_equipamientos_seleccionados()
        self.seleccionadosTextChanged.emit()
        
    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return ROLE_NAMES

    @override
    def rowCount(self, parent: QModelIndex|None = None) -> int:
        return len(self.equipamientos_posibles)

    @override
    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if not index.isValid(): return None

        if role == ROL_NOMBRE:
            return self.equipamientos_posibles[index.row()]
        elif role == ROL_SELECCIONADO:
            return self.equipamientos_posibles[index.row()] in self.equipamientos_seleccionados
        else:
            return None

    @override
    def setData(self, index: QModelIndex, value: Any, role: int = 0) -> bool:
        if not index.isValid(): return False

        if role == ROL_NOMBRE:
            # No tiene sentido renombrar equipamientos existentes
            return False
        elif role == ROL_SELECCIONADO:
            equipamiento = self.equipamientos_posibles[index.row()]
            if value:
                self.gestor.agregar_equipamiento_a_aula(self.i_edificio, self.i_aula, equipamiento)
            else:
                self.gestor.borrar_equipamiento_de_aula(self.i_edificio, self.i_aula, equipamiento)

            self.seleccionadosTextChanged.emit()
            return True
        else:
            return False

    @pyqtSlot(str, result=bool)
    def agregarEquipamiento(self, name: str) -> bool:
        '''
        Agregar un equipamiento que no está en la lista.
        '''
        name = name.strip()
        if not name:
            return False

        self.beginResetModel()
        self.gestor.agregar_equipamiento_a_aula(self.i_edificio, self.i_aula, name)
        self._actualizar_equipamientos_posibles()
        self.endResetModel()
        self.seleccionadosTextChanged.emit()
        return True

    def _actualizar_equipamientos_posibles(self):
        self.equipamientos_posibles = self.gestor.get_equipamientos_existentes()
    
    def _set_equipamientos_seleccionados(self):
        self.equipamientos_seleccionados = self.gestor.get_from_aula(self.i_edificio, self.i_aula, CAMPO_AULA_EQUIPAMIENTO)
