import pytest


from asignacion_aulica.gestor_de_datos.entidades import (
    fieldnames_Aula, fieldnames_AulaDoble, fieldnames_Carrera, fieldnames_Clase,
    fieldnames_Edificio, fieldnames_Materia
)
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

# Índices de los campos, en diccionarios para más legibilidad:
campo_Edificio:  dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Edificio)}
campo_Aula:      dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Aula)}
campo_AulaDoble: dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_AulaDoble)}
campo_Carrera:   dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Carrera)}
campo_Materia:   dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Materia)}
campo_Clase:     dict[str, int] = {nombre: índice for índice, nombre in enumerate(fieldnames_Clase)}

@pytest.fixture
def gestor() -> GestorDeDatos:
    '''
    Devuelve un gestor de datos inicialmente vacío.
    '''
    return GestorDeDatos()