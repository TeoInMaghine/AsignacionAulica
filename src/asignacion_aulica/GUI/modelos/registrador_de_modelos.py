from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.GUI.modelos.list_aulas import ListAulas
from asignacion_aulica.GUI.modelos.list_edificios import ListEdificios
from asignacion_aulica.GUI.modelos.equipamiento_model import ListEquipamientos
from PyQt6.QtQml import qmlRegisterType


def agregar_defaults_al_constructor(clase: type, **defaults) -> type:
    '''
    Crea una nueva clase que wrappea a ``clase`` y le agrega valores por defecto
    al constructor.

    :param clase: Una clase.
    :param defaults: Un diccionario que mapea nombres de argumentos a valores
    por defecto.
    '''
    class Wrapped(clase):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **(defaults|kwargs))

    return Wrapped

def registrar_modelos_qml(gestor_de_datos: GestorDeDatos):
    '''
    Registrar los modelos de asignación áulica en qml.

    :param gestor_de_datos: El gestor de datos a pasarle a los modelos.
    '''
    # Esta línea es para que el GC no piense que puede limpiar las clases
    # wrapper cuando sale de este scope. Literal python crashea si no.
    # *Achievement unlocked: use after free error in python.*
    global _ListAulas, _ListEquipamientos, _ListEdificios

    _ListEdificios = agregar_defaults_al_constructor(ListEdificios, gestor=gestor_de_datos)
    _ListAulas = agregar_defaults_al_constructor(ListAulas, gestor=gestor_de_datos)
    _ListEquipamientos = agregar_defaults_al_constructor(ListEquipamientos, gestor=gestor_de_datos)

    qmlRegisterType(_ListEdificios, 'ModelosAsignaciónÁulica'.encode(), 1, 0, 'ListEdificios')
    qmlRegisterType(_ListAulas, 'ModelosAsignaciónÁulica'.encode(), 1, 0, 'ListAulas')
    qmlRegisterType(_ListEquipamientos, 'ModelosAsignaciónÁulica'.encode(), 1, 0, 'ListEquipamientos')
