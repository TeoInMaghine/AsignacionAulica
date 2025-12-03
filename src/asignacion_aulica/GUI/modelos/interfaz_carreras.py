from PyQt6.QtCore import QObject, pyqtSlot

from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

class InterfazDeCarreras(QObject):
    '''
    Interfaz para ver y editar los datos de una carrera desde QML.
    '''

    def __init__(self, parent, gestor: GestorDeDatos):
        super().__init__(parent)
        self.gestor: GestorDeDatos = gestor
