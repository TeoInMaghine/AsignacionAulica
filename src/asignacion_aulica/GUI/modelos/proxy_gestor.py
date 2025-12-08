import logging
from PyQt6.QtCore import QObject, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.lógica_de_asignación.postprocesamiento import InfoPostAsignación

logger = logging.getLogger(__name__)

class ProxyGestorDeDatos(QObject):
    '''
    Bindings para poder llamar a métodos del gestor de datos desde QML.
    '''
    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
    
    @pyqtSlot()
    def asignarAulas(self):
        result: InfoPostAsignación = self.gestor.asignar_aulas()
