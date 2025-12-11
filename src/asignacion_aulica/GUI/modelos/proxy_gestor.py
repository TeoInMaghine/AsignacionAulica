import logging
import time
from PyQt6.QtCore import QObject, QThreadPool, pyqtBoundSignal, pyqtSignal, pyqtSlot, QRunnable

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.lógica_de_asignación.postprocesamiento import InfoPostAsignación

logger = logging.getLogger(__name__)

class ProxyGestorDeDatos(QObject):
    '''
    Bindings para poder llamar a métodos del gestor de datos desde QML.
    '''

    # Se emite con un string que dice los días sin asignar.
    finAsignarAulas: pyqtSignal = pyqtSignal(str)

    def __init__(self, gestor: GestorDeDatos):
        super().__init__()
        self.gestor: GestorDeDatos = gestor

        self.threadpool = QThreadPool()

    @pyqtSlot()
    def asignarAulas(self):
        '''
        Ejecuta la asignación en un hilo y emite la señal finAsignarAulas
        cuando termina.
        '''
        worker = _Asignador(self.gestor, self.finAsignarAulas)
        self.threadpool.start(worker)

class _Asignador(QRunnable):
    '''
    Objeto QT encargado de ejecutar la asignación de aulas en un hilo.
    '''

    def __init__(self, gestor: GestorDeDatos, señal_fin: pyqtBoundSignal):
        super().__init__()
        self.gestor: GestorDeDatos = gestor
        self.señal_fin: pyqtBoundSignal = señal_fin

    @pyqtSlot()
    def run(self):
        time.sleep(1.5)
        result: InfoPostAsignación = self.gestor.asignar_aulas()
        str_días_sin_asignar = ', '.join(map(lambda d: d.name, result.días_sin_asignar))
        self.señal_fin.emit(str_días_sin_asignar)
