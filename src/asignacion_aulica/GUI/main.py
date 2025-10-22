import sys, os
from pathlib import Path

from PyQt6.QtGui import QGuiApplication, QFontDatabase, QIcon
from PyQt6.QtQml import QQmlApplicationEngine, qmlRegisterType

from asignacion_aulica.GUI.list_model import ListAulas
from asignacion_aulica.GUI.equipamiento_model import ListEquipamientos
from asignacion_aulica.gestor_de_datos import GestorDeDatos
from asignacion_aulica import assets

def configurar_fuente_por_defecto():
    fonts_path = assets.get_path('fonts')
    for font_file in os.listdir(fonts_path):
        QFontDatabase.addApplicationFont(os.path.join(fonts_path, font_file))

    default_font = QFontDatabase.font('Karla', 'regular', 12)
    QGuiApplication.setFont(default_font)

def main() -> int:
    app = QGuiApplication(sys.argv + ['-style', 'Basic'])
    icono = QIcon(assets.get_path('iconos', 'unrn.ico'))
    app.setWindowIcon(icono)

    # Creamos clases wrapper de los list models para que usen esta instancia
    # del gestor de datos, ya que pasarlo desde Qml sería más complicado
    gestor_de_datos_de_la_aplicación = GestorDeDatos(assets.get_path('base_de_datos'))

    # Si python tuviera clases anónimas se usarían acá, en cambio prefijo con
    # '_' para dar a entender lo mismo (que no me importa el nombre)
    class _ListAulas(ListAulas):
        def __init__(self, parent):
            super().__init__(parent, gestor_de_datos_de_la_aplicación)
    class _ListEquipamientos(ListEquipamientos):
        def __init__(self, parent):
            super().__init__(parent, gestor_de_datos_de_la_aplicación)

    qmlRegisterType(_ListAulas, 'Custom', 1, 0, 'ListAulas')
    qmlRegisterType(_ListEquipamientos, 'Custom', 1, 0, 'ListEquipamientos')

    configurar_fuente_por_defecto()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('assets_path', Path(assets.assets_path).as_uri())
    engine.addImportPath(assets.QML_import_path)
    engine.loadFromModule('QML', "Main")
    
    if not engine.rootObjects():
        return -1

    return app.exec()
