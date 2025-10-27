import sys, os
from pathlib import Path

from PyQt6.QtGui import QGuiApplication, QFontDatabase, QIcon
from PyQt6.QtQml import QQmlApplicationEngine

from asignacion_aulica.GUI.modelos import registrar_modelos_qml
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

    gestor_de_datos_de_la_aplicación = GestorDeDatos(assets.get_path('base_de_datos'))
    registrar_modelos_qml(gestor_de_datos_de_la_aplicación)

    configurar_fuente_por_defecto()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('assets_path', Path(assets.assets_path).as_uri())
    engine.addImportPath(assets.QML_import_path)
    engine.loadFromModule('QML', "Main")
    
    if not engine.rootObjects():
        return -1

    return app.exec()
