from asignacion_aulica.gestor_de_datos import GestorDeDatos
from asignacion_aulica.GUI.modelos.list_model import ListAulas
from asignacion_aulica.GUI.modelos.equipamiento_model import ListEquipamientos
from typing import Any


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

def args_para_registrar_modelos_qml(
        gestor_de_datos: GestorDeDatos
    ) -> tuple[tuple[Any, ...]]:
    '''
    Por alguna razón desconocida por el momento, no se pueden registrar tipos
    dentro de otro archivo que no sea el main, así que en cambio se devuelven
    los argumentos necesarios para usar qmlRegisterType.

    :param gestor_de_datos: El gestor de datos a pasarle a los modelos.
    :return: Una tupla de tuplas con los argumentos a pasar a qmlRegisterType.
    '''
    _ListAulas = agregar_defaults_al_constructor(ListAulas, gestor=gestor_de_datos)
    _ListEquipamientos = agregar_defaults_al_constructor(ListEquipamientos, gestor=gestor_de_datos)

    return (
        (_ListAulas, 'ModelosAsignaciónÁulica'.encode(), 1, 0, 'ListAulas'),
        (_ListEquipamientos, 'ModelosAsignaciónÁulica'.encode(), 1, 0, 'ListEquipamientos')
    )
