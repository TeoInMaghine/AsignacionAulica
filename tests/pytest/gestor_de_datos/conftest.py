import pytest
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

@pytest.fixture
def gestor() -> GestorDeDatos:
    '''
    Devuelve un gestor de datos inicialmente vacío.
    '''
    return GestorDeDatos()
