from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.lógica_de_asignación.restricciones import no_superponer_clases
from asignacion_aulica.lógica_de_asignación import preferencias

@pytest.mark.aulas(
    dict(capacidad=31),
    dict(capacidad=50),
    dict(capacidad=100)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=30),
    dict(cantidad_de_alumnos=40),
    dict(cantidad_de_alumnos=25),
    )
@pytest.mark.asignaciones_forzadas({ 0: 0, 1: 1, 2: 2 }) # Asignaciones arbitrarias: clase i con aula i
def test_a_algunas_clases_les_sobra_capacidad(aulas, clases, modelo, asignaciones):
    cantidad_sobrante, cota_superior = preferencias.obtener_capacidad_sobrante(clases, aulas, modelo, asignaciones)
    assert cota_superior == (31 - 30 + 50 - 40 + 100 - 25)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    # Como está forzado, la cantidad sobrante es igual a su cota superior
    assert solver.value(cantidad_sobrante) == cota_superior

@pytest.mark.aulas(
    dict(capacidad=31),
    dict(capacidad=50),
    dict(capacidad=100)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=250),
    dict(cantidad_de_alumnos=400),
    dict(cantidad_de_alumnos=100),
)
def test_a_ninguna_clase_le_sobra_capacidad(aulas, clases, modelo, asignaciones):
    cantidad_sobrante, cota_superior = preferencias.obtener_capacidad_sobrante(clases, aulas, modelo, asignaciones)
    # La cota superior sería 0, pero en cambio se devuelve 1 porque si no
    # fallaría al normalizar, siendo que debe dividir por la cota superior
    assert cota_superior == 1

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(cantidad_sobrante) == 0

@pytest.mark.aulas(
    dict(capacidad=10),
    dict(capacidad=20),
    dict(capacidad=30)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=10),
    dict(cantidad_de_alumnos=20),
    dict(cantidad_de_alumnos=30),
)
def test_entran_justito(aulas, clases, modelo, asignaciones):
    # Restricciones para que no estén en el mismo aula
    for predicado in no_superponer_clases(clases, aulas, {}, asignaciones):
        modelo.add(predicado)

    # Minimizar capacidad sobrante
    cantidad_sobrante, cota_superior = preferencias.obtener_capacidad_sobrante(clases, aulas, modelo, asignaciones)
    assert cota_superior == (30 - 10 + 30 - 20 + 30 - 30)

    # Resolver
    modelo.minimize((1 / cota_superior) * cantidad_sobrante)
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 0] == 1
    assert sum(asignaciones_finales[1,:]) == 1 and asignaciones_finales[1, 1] == 1
    assert sum(asignaciones_finales[2,:]) == 1 and asignaciones_finales[2, 2] == 1
    assert solver.value(cantidad_sobrante) == 0

@pytest.mark.aulas(
    dict(capacidad=11),
    dict(capacidad=21),
    dict(capacidad=31)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=10),
    dict(cantidad_de_alumnos=20),
    dict(cantidad_de_alumnos=30),
)
def test_minimiza_capacidad_sobrante(aulas, clases, modelo, asignaciones):
    '''
    Esta prueba es para verificar que minimiza la capacidad sobrante en total, y
    no el número de aulas con capacidad sobrante.

    La idea es que si minimizara el número de aulas pondría la materia más
    chica en el aula más grande y quedaría mucha gente afuera. En cambio si
    minimiza la gente que queda afuera, queda menos gente afuera.
    '''
    # Restricciones para que no estén en el mismo aula
    for predicado in no_superponer_clases(clases, aulas, {}, asignaciones):
        modelo.add(predicado)

    # Minimizar capacidad sobrante
    cantidad_sobrante, cota_superior = preferencias.obtener_capacidad_sobrante(clases, aulas, modelo, asignaciones)
    assert cota_superior == (31 - 10 + 31 - 20 + 31 - 30)

    # Resolver
    modelo.minimize((1 / cota_superior) * cantidad_sobrante)
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)

    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 0] == 1
    assert sum(asignaciones_finales[1,:]) == 1 and asignaciones_finales[1, 1] == 1
    assert sum(asignaciones_finales[2,:]) == 1 and asignaciones_finales[2, 2] == 1
    assert solver.value(cantidad_sobrante) == 3
