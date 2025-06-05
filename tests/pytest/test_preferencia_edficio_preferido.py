from ortools.sat.python import cp_model
import pytest

from asignacion_aulica.backend import preferencias
from helper_functions import *

def test_todas_las_aulas_en_el_edificio_preferido():
    aulas = make_aulas(
        dict(edificio='preferido'),
        dict(edificio='preferido'),
        dict(edificio='preferido')
    )

    clases, modelo = make_clases(
        len(aulas),
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido')
    )

    clases_fuera_del_edificio_preferido = preferencias.obtener_cantidad_de_clases_fuera_del_edificio_preferido(modelo, clases, aulas)

    # Forzar asignaciones arbitrarias
    modelo.add(clases.loc[0, 'aula_asignada'] == 1)
    modelo.add(clases.loc[1, 'aula_asignada'] == 2)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(clases_fuera_del_edificio_preferido) == 0

def test_algunas_aulas_en_el_edificio_preferido():
    aulas = make_aulas(
        dict(edificio='preferido'),
        dict(edificio='no preferido'),
        dict(edificio='preferido'),
        dict(edificio='preferido 2')
    )

    clases, modelo = make_clases(
        len(aulas),
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido 2'),
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido 2'),
        dict(edificio_preferido='preferido')
    )

    clases_fuera_del_edificio_preferido = preferencias.obtener_cantidad_de_clases_fuera_del_edificio_preferido(modelo, clases, aulas)

    # Forzar asignaciones arbitrarias (generadas aleatoriamente)
    modelo.add(clases.loc[0, 'aula_asignada'] == 3)
    modelo.add(clases.loc[1, 'aula_asignada'] == 2)
    modelo.add(clases.loc[2, 'aula_asignada'] == 1)
    modelo.add(clases.loc[3, 'aula_asignada'] == 1)
    modelo.add(clases.loc[4, 'aula_asignada'] == 2)
    modelo.add(clases.loc[5, 'aula_asignada'] == 0)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(clases_fuera_del_edificio_preferido) == 4

def test_elije_aula_en_edificio_preferido():
    aulas = make_aulas(
        dict(edificio='no preferido 1'),
        dict(edificio='no preferido 2'),
        dict(edificio='preferido'), # Importante el orden, tiene que ser el índice 2
        dict(edificio='no preferido 3'),
        dict(edificio='no preferido 4')
    )

    clases, modelo = make_clases(
        len(aulas),
        dict(edificio_preferido='preferido'),
    )

    clases_fuera_del_edificio_preferido = preferencias.obtener_cantidad_de_clases_fuera_del_edificio_preferido(modelo, clases, aulas)

    # Pedir al modelo minimizar cantidad de clases fuera del edificio preferido 
    modelo.minimize(clases_fuera_del_edificio_preferido)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')

    # La clase se debe asignar al aula en el edificio preferido
    assert solver.value(clases_fuera_del_edificio_preferido) == 0
    assert solver.value(clases.loc[0, 'aula_asignada']) == 2

