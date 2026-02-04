import sys, os, logging
from pathlib import Path

from PyQt6.QtGui import QGuiApplication, QFontDatabase, QIcon
from PyQt6.QtQml import QQmlApplicationEngine

from asignacion_aulica.GUI.modelos.registrador_de_modelos import registrar_modelos_qml
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica import assets

logger = logging.getLogger(__name__)

PATH_GESTOR_DE_DATOS = Path(os.path.join(assets.APP_DATA_PATH, 'gestor.pickle'))

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

    mensaje_de_error_al_cargar = ''
    gestor_de_datos_de_la_aplicación = GestorDeDatos(PATH_GESTOR_DE_DATOS)
    try:
        gestor_de_datos_de_la_aplicación.cargar()
    except ValueError as e:
        mensaje_de_error_al_cargar = str(e)
    except OSError as e:
        mensaje_de_error_al_cargar = (
            'Ocurrió un error al leer el archivo'
            f' {PATH_GESTOR_DE_DATOS}: {str(e)}'
        )
    except Exception as e:
        mensaje_de_error_al_cargar = (
            'Ocurrió un error inesperado al cargar el '
            f'archivo {PATH_GESTOR_DE_DATOS}: {str(e)}'
        )

    registrar_modelos_qml(gestor_de_datos_de_la_aplicación)

    configurar_fuente_por_defecto()

    engine = QQmlApplicationEngine()
    context = engine.rootContext()
    context.setContextProperty('assets_path', Path(assets.ASSETS_PATH).as_uri())
    context.setContextProperty('mensaje_de_error_al_cargar', mensaje_de_error_al_cargar)
    engine.addImportPath(assets.QML_IMPORT_PATH)
    engine.loadFromModule('QML', "Main")
    
    if not engine.rootObjects():
        return -1

    return app.exec()
