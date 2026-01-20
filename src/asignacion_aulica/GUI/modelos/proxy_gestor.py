import logging, time
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

    @pyqtSlot(int)
    def ordenarAulas(self, i_edificio: int|None):
        '''
        Ordena las aulas del edificio en el índice dado (sólo si es válido).
        '''
        if i_edificio is not None and i_edificio >= 0 and i_edificio < self.gestor.cantidad_de_edificios():
            self.gestor.ordenar_aulas(i_edificio)

    @pyqtSlot()
    def asignarAulas(self):
        '''
        Ejecuta la asignación en un hilo y emite la señal finAsignarAulas
        cuando termina.
        '''
        worker = _Asignador(self.gestor, self.finAsignarAulas)
        self.threadpool.start(worker)

    @pyqtSlot(result=str)
    def guardar(self) -> str:
        '''
        Llamar al método `guardar` del gestor de datos.

        :return: Un mensaje de error, vacío en caso de éxito.
        '''
        try:
            self.gestor.guardar()
            return ''
        except Exception as e:
            logger.error('Error guardando datos: %s', e)
            return 'No se pudieron guardar los datos.'


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
        mensaje_final = ''

        posible_error = self.gestor.validar_datos()
        if posible_error:
            mensaje_final = posible_error
        else:
            time.sleep(0.8) # Para que parezca como que tarda un poquito
            result: InfoPostAsignación = self.gestor.asignar_aulas()
            if result.días_sin_asignar:
                str_días_sin_asignar = ', '.join(map(lambda d: d.name, result.días_sin_asignar))
                mensaje_final = 'No se puedieron asignar aulas para las clases de los días ' + str_días_sin_asignar
        
        self.señal_fin.emit(mensaje_final)
