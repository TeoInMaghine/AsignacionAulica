import pytest
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

from mocks import (
    pytest_configure,
    Edificios,
    edificios
)

@pytest.fixture
def gestor(edificios: Edificios) -> GestorDeDatos:
    '''
    Devuelve un gestor de datos.

    El gestor tiene inicialmente cargados algunos datos del fixture edificios
    (TODO: cargar todos los datos, cuando haga falta).
    '''
    gestor = GestorDeDatos()

    for edificio in edificios:
        i_edificio = gestor.cantidad_de_edificios()
        gestor.agregar_edificio()
        gestor.get_edificio(i_edificio).nombre = edificio.nombre
        for aula in edificio.aulas:
            i_aula = gestor.cantidad_de_aulas(i_edificio)
            gestor.agregar_aula(i_edificio)
            gestor.get_aula(i_edificio, i_aula).nombre = aula.nombre
    
    return gestor
