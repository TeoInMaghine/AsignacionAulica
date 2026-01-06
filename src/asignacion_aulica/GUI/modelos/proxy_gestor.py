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

    @pyqtSlot()
    def asignarAulas(self):
        '''
        Ejecuta la asignación en un hilo y emite la señal finAsignarAulas
        cuando termina.
        '''
        worker = _Asignador(self.gestor, self.finAsignarAulas)
        self.threadpool.start(worker)
    
    @pyqtSlot(int, int, int, int, int)
    def asignarAulaDeUnaClase(self, i_carrera: int, i_materia: int, i_clase: int, i_edificio: int, i_aula: int):
        '''
        Le asigna un aula a una clase.

        Falla silenciosamente si hay algún índice fuera de rango.
        '''
        if not 0 <= i_carrera < self.gestor.cantidad_de_carreras():
            logger.error('setearAulaDeUnaClase: carrera %d está fuera de rango.', i_carrera)
        elif not 0 <= i_materia < self.gestor.cantidad_de_materias(i_carrera):
            logger.error('setearAulaDeUnaClase: materia %d está fuera de rango.', i_materia)
        elif not 0 <= i_clase < self.gestor.cantidad_de_clases(i_carrera, i_materia):
            logger.error('setearAulaDeUnaClase: clase %d está fuera de rango.', i_clase)
        elif not 0 <= i_edificio < self.gestor.cantidad_de_edificios():
            logger.error('setearAulaDeUnaClase: edificio %d está fuera de rango.', i_edificio)
        elif not 0 <= i_aula < self.gestor.cantidad_de_aulas(i_edificio):
            logger.error('setearAulaDeUnaClase: aula %d está fuera de rango.', i_aula)
        else:
            logger.debug('Asignando aula %s a la clase %s.', (i_edificio, i_aula), (i_carrera, i_materia, i_clase))
            clase = self.gestor.get_clase(i_carrera, i_materia, i_clase)
            clase.aula_asignada = self.gestor.get_aula(i_edificio, i_aula)
    
    @pyqtSlot(int, int, int)
    def borrarAulaDeUnaClase(self, i_carrera: int, i_materia: int, i_clase: int):
        '''
        Le asigna `None` como aula a una clase.

        Falla silenciosamente si hay algún índice fuera de rango.
        '''
        if not 0 <= i_carrera < self.gestor.cantidad_de_carreras():
            logger.error('setearAulaDeUnaClase: carrera %d está fuera de rango.', i_carrera)
        elif not 0 <= i_materia < self.gestor.cantidad_de_materias(i_carrera):
            logger.error('setearAulaDeUnaClase: materia %d está fuera de rango.', i_materia)
        elif not 0 <= i_clase < self.gestor.cantidad_de_clases(i_carrera, i_materia):
            logger.error('setearAulaDeUnaClase: clase %d está fuera de rango.', i_clase)
        else:
            logger.debug('Borrando aula de la clase %s.', (i_carrera, i_materia, i_clase))
            clase = self.gestor.get_clase(i_carrera, i_materia, i_clase)
            clase.aula_asignada = None

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
        time.sleep(0.8) # Para que parezca como que tarda un poquito
        result: InfoPostAsignación = self.gestor.asignar_aulas()
        str_días_sin_asignar = ', '.join(map(lambda d: d.name, result.días_sin_asignar))
        self.señal_fin.emit(str_días_sin_asignar)
