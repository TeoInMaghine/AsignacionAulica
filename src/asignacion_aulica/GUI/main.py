from PySide6.QtGui import QGuiApplication, QFontDatabase, QIcon
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtQml import QQmlApplicationEngine
from pathlib import Path
import sys, os

from asignacion_aulica import assets

def configurar_fuente_por_defecto():
    fonts_path = assets.get_path('fonts')
    for font_file in os.listdir(fonts_path):
        QFontDatabase.addApplicationFont(os.path.join(fonts_path, font_file))

    default_font = QFontDatabase.font('Karla', 'regular', 12)
    QGuiApplication.setFont(default_font)

def main() -> int:
    app = QGuiApplication(sys.argv)
    icono = QIcon(assets.get_path('iconos', 'unrn.ico'))
    app.setWindowIcon(icono)
    QQuickStyle.setStyle('Basic')

    configurar_fuente_por_defecto()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty('assets_path', Path(assets.assets_path).as_uri())
    engine.addImportPath(assets.QML_import_path)
    engine.loadFromModule('QML', "Main")
    
    if not engine.rootObjects():
        return -1

    return app.exec()
