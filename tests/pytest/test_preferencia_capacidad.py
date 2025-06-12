from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.backend.lógica_de_asignación import crear_matriz_de_asignaciones
from asignacion_aulica.backend.restricciones import no_superponer_clases
from asignacion_aulica.backend import preferencias
from helper_functions import *

def test_algunas_clases_exceden_capacidad():
    aulas = make_aulas(
        dict(capacidad=30),
        dict(capacidad=40),
        dict(capacidad=25)
    )
    clases = make_clases(
        dict(cantidad_de_alumnos=31),
        dict(cantidad_de_alumnos=50),
        dict(cantidad_de_alumnos=100),
    )
    modelo = cp_model.CpModel()

    # Forzar asignaciones arbitrarias (clase i con aula i)
    asignaciones = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(clases, aulas, modelo, asignaciones)

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
    clases = make_clases(
        dict(cantidad_de_alumnos=31),
        dict(cantidad_de_alumnos=50),
        dict(cantidad_de_alumnos=100),
    )
    modelo = cp_model.CpModel()

    # Forzar asignaciones arbitrarias (clase i con aula i)
    asignaciones = np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])

    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(clases, aulas, modelo, asignaciones)

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
    clases = make_clases(
        dict(cantidad_de_alumnos=10),
        dict(cantidad_de_alumnos=20),
        dict(cantidad_de_alumnos=30),
    )
    modelo = cp_model.CpModel()

    asignaciones = crear_matriz_de_asignaciones(clases, aulas, modelo)

    # Restricciones para que no estén en el mismo aula
    for predicado in no_superponer_clases(clases, aulas, asignaciones):
        modelo.add(predicado)

    # Minizar capacidad excedida
    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(clases, aulas, modelo, asignaciones)
    modelo.minimize(cantidad_excedida)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    
    assert solver.value(cantidad_excedida) == 0
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 0] == 1
    assert sum(asignaciones_finales[1,:]) == 1 and asignaciones_finales[1, 1] == 1
    assert sum(asignaciones_finales[2,:]) == 1 and asignaciones_finales[2, 2] == 1

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

    clases = make_clases(
        dict(cantidad_de_alumnos=11),
        dict(cantidad_de_alumnos=21),
        dict(cantidad_de_alumnos=31),
    )
    modelo = cp_model.CpModel()

    asignaciones = crear_matriz_de_asignaciones(clases, aulas, modelo)

    # Restricciones para que no estén en el mismo aula
    for predicado in no_superponer_clases(clases, aulas, asignaciones):
        modelo.add(predicado)

    # Minizar capacidad excedida
    cantidad_excedida = preferencias.obtener_cantidad_de_alumnos_fuera_del_aula(clases, aulas, modelo, asignaciones)
    modelo.minimize(cantidad_excedida)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)

    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 0] == 1
    assert sum(asignaciones_finales[1,:]) == 1 and asignaciones_finales[1, 1] == 1
    assert sum(asignaciones_finales[2,:]) == 1 and asignaciones_finales[2, 2] == 1
    assert solver.value(cantidad_excedida) == 3

