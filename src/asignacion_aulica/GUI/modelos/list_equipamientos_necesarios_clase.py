import logging
from typing import Any, override
from PyQt6.QtCore import QAbstractListModel, Qt, QModelIndex, QByteArray, pyqtProperty, pyqtSignal, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

logger = logging.getLogger(__name__)

ROL_NOMBRE: int = Qt.ItemDataRole.UserRole + 1
ROL_SELECCIONADO: int = Qt.ItemDataRole.UserRole + 2
ROLE_NAMES: dict[int, QByteArray] = {
    ROL_NOMBRE: QByteArray("nombre".encode()),
    ROL_SELECCIONADO: QByteArray("seleccionado".encode())
}

class ListEquipamientosNecesariosDeClases(QAbstractListModel):
    '''
    Esta clase conecta el selector de equipamientos de las clases en la GUI con
    el gestor datos.

    En la GUI los equipamientos existentes se muestran en orden alfabético, pero
    en el gestor de datos se guardan en una estructura que no tiene orden, así
    que para no estar ordenándolos todo el rato esta clase se encarga de
    mantener una copia ordenada y sincronizada de esos datos.
    '''
    seleccionadosTextChanged: pyqtSignal = pyqtSignal() #TODO: Esto no debería ser compartido entre instancias.

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor

        # Cosas seteadas desde QT:
        self.i_carrera: int = 0
        self.i_materia: int = 0
        self.i_clase: int = 0

        # Cache para no estar pidiéndole al gestor que ordene los datos todo el
        # tiempo. Acordarse de actualizarla cuando puede haber cambios.
        self.equipamientos_posibles: list[str]
        self.actualizarLista()

    @pyqtProperty(str, notify=seleccionadosTextChanged)
    def seleccionadosText(self) -> str:
        seleccionados = self._get_equipamientos_seleccionados()
        if len(seleccionados) == 0:
            return "Ninguno"
        else:
            seleccionados_en_orden_alfabético = list(seleccionados)
            seleccionados_en_orden_alfabético.sort()
            return ", ".join(seleccionados_en_orden_alfabético)

    @pyqtProperty(int)
    def indexCarrera(self) -> int:
        return self.i_carrera

    @indexCarrera.setter
    def indexCarrera(self, indexCarrera: int):
        if indexCarrera >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexCarrera=%d', indexCarrera)
            self.i_carrera = indexCarrera
            self.seleccionadosTextChanged.emit()

    @pyqtProperty(int)
    def indexMateria(self) -> int:
        return self.i_materia

    @indexMateria.setter
    def indexMateria(self, indexMateria: int):
        if indexMateria >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexMateria=%d', indexMateria)
            self.i_materia = indexMateria
            self.seleccionadosTextChanged.emit()

    @pyqtProperty(int)
    def indexClase(self) -> int:
        return self.i_clase

    @indexClase.setter
    def indexClase(self, indexClase: int):
        if indexClase >= 0: # Ignorar cuando QT setea -1
            logger.debug('Set indexClase=%d', indexClase)
            self.i_clase = indexClase
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
            return self.equipamientos_posibles[index.row()] in self._get_equipamientos_seleccionados()
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
                self.gestor.agregar_equipamiento_a_clase(
                    self.i_carrera, self.i_materia, self.i_clase, equipamiento
                )
            else:
                self.gestor.borrar_equipamiento_de_clase(
                    self.i_carrera, self.i_materia, self.i_clase, equipamiento
                )

            self.seleccionadosTextChanged.emit()
            return True
        else:
            return False

    @pyqtSlot(str, result=bool)
    def agregarEquipamiento(self, name: str) -> bool:
        '''
        Agregar un equipamiento nuevo a la lista.
        '''
        name = name.strip()
        if not name:
            return False

        self.gestor.agregar_equipamiento_a_clase(
            self.i_carrera, self.i_materia, self.i_clase, name
        )
        self.actualizarLista()
        self.seleccionadosTextChanged.emit()
        return True
    
    @pyqtSlot()
    def actualizarLista(self):
        logger.debug('Actualizando lista')
        self.beginResetModel()
        self.equipamientos_posibles = self.gestor.get_equipamientos_existentes()
        self.endResetModel()
    
    def _get_equipamientos_seleccionados(self) -> set[str]:
        los_índices_son_válidos = (
            self.gestor.cantidad_de_carreras() > self.i_carrera
            and self.gestor.cantidad_de_materias(self.i_carrera) > self.i_materia
            and self.gestor.cantidad_de_clases(self.i_carrera, self.i_materia) > self.i_clase
        )
        
        if los_índices_son_válidos:
            return self.gestor.get_clase(
                self.i_carrera, self.i_materia, self.i_clase
            ).equipamiento_necesario
        else:
            return set()
