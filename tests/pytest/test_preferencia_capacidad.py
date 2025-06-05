from ortools.sat.python import cp_model
import pytest

from asignacion_aulica.backend import preferencias
from helper_functions import *

def test_algunas_clases_exceden_capacidad():
    aulas = make_aulas(
        dict(capacidad=30),
        dict(capacidad=40),
        dict(capacidad=25)
    )

    clases, modelo = make_clases(
        len(aulas),
        dict(cantidad_de_alumnos=31),
        dict(cantidad_de_alumnos=50),
        dict(cantidad_de_alumnos=100),
    )

    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(modelo, clases, aulas)

    # Forzar asignaciones arbitrarias
    modelo.add(clases.loc[0, 'aula_asignada'] == 0)
    modelo.add(clases.loc[1, 'aula_asignada'] == 1)
    modelo.add(clases.loc[2, 'aula_asignada'] == 2)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(cantidad_excedida) == (31 - 30 + 50 - 40 + 100 - 25)

def test_ninguna_clase_excede_capacidad():
    aulas = make_aulas(
        dict(capacidad=250),
        dict(capacidad=400),
        dict(capacidad=100)
    )

    clases, modelo = make_clases(
        len(aulas),
        dict(cantidad_de_alumnos=31),
        dict(cantidad_de_alumnos=50),
        dict(cantidad_de_alumnos=100),
    )

    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(modelo, clases, aulas)

    # Forzar asignaciones arbitrarias
    modelo.add(clases.loc[0, 'aula_asignada'] == 0)
    modelo.add(clases.loc[1, 'aula_asignada'] == 1)
    modelo.add(clases.loc[2, 'aula_asignada'] == 2)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(cantidad_excedida) == 0

def test_entran_justito():
    aulas = make_aulas(
        dict(capacidad=10),
        dict(capacidad=20),
        dict(capacidad=30)
    )

    clases, modelo = make_clases(
        len(aulas),
        dict(cantidad_de_alumnos=10),
        dict(cantidad_de_alumnos=20),
        dict(cantidad_de_alumnos=30),
    )

    # Restricciones para que no estén en el mismo aula
    modelo.add(clases.loc[0, 'aula_asignada'] != clases.loc[1, 'aula_asignada'])
    modelo.add(clases.loc[0, 'aula_asignada'] != clases.loc[2, 'aula_asignada'])
    modelo.add(clases.loc[1, 'aula_asignada'] != clases.loc[2, 'aula_asignada'])

    # Minizar capacidad excedida
    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(modelo, clases, aulas)
    modelo.minimize(cantidad_excedida)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(cantidad_excedida) == 0
    assert solver.value(clases.loc[0, 'aula_asignada']) == 0
    assert solver.value(clases.loc[1, 'aula_asignada']) == 1
    assert solver.value(clases.loc[2, 'aula_asignada']) == 2

def test_minimiza_capacidad_excedida():
    '''
    Esta prueba es para verificar que minimiza la capacidad excedida en total, y
    no el número de aulas con capacidad excedida.

    La idea es que si minimizara el número de aulas pondría la materia más
    grande en el aula más chica y quedaría mucha gente afuera. En cambio si
    minimiza la gente que queda afuera, queda menos gente afuera.
    '''
    aulas = make_aulas(
        dict(capacidad=10),
        dict(capacidad=20),
        dict(capacidad=30)
    )

    clases, modelo = make_clases(
        len(aulas),
        dict(cantidad_de_alumnos=11),
        dict(cantidad_de_alumnos=21),
        dict(cantidad_de_alumnos=31),
    )

    # Restricciones para que no estén en el mismo aula
    modelo.add(clases.loc[0, 'aula_asignada'] != clases.loc[1, 'aula_asignada'])
    modelo.add(clases.loc[0, 'aula_asignada'] != clases.loc[2, 'aula_asignada'])
    modelo.add(clases.loc[1, 'aula_asignada'] != clases.loc[2, 'aula_asignada'])

    # Minizar capacidad excedida
    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(modelo, clases, aulas)
    modelo.minimize(cantidad_excedida)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(clases.loc[0, 'aula_asignada']) == 0
    assert solver.value(clases.loc[1, 'aula_asignada']) == 1
    assert solver.value(clases.loc[2, 'aula_asignada']) == 2
    assert solver.value(cantidad_excedida) == 3
