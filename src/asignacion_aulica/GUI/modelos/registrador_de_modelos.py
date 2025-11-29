from asignacion_aulica.GUI.modelos.list_carreras import ListCarreras
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos
from asignacion_aulica.GUI.modelos.list_aulas import ListAulas
from asignacion_aulica.GUI.modelos.list_edificios import ListEdificios
from asignacion_aulica.GUI.modelos.list_equipamientos_aula import ListEquipamientosDeAula
from PyQt6.QtQml import qmlRegisterType

modelos_registrados: list[type] = []
'''
Guardamos referencias a los modelos registrados para que el GC no piense que
puede limpiar las clases wrapper cuando sale de este scope. Literal python
crashea si no.
*Achievement unlocked: use after free error in python.*
'''

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
    qml_module = 'ModelosAsignaciónÁulica'.encode()
    for modelo in (ListEdificios, ListAulas, ListEquipamientosDeAula, ListCarreras):
        modelo_wrapeado = agregar_defaults_al_constructor(modelo, gestor=gestor_de_datos)
        qmlRegisterType(modelo_wrapeado, qml_module, 1, 0, modelo.__name__)
        modelos_registrados.append(modelo_wrapeado)
