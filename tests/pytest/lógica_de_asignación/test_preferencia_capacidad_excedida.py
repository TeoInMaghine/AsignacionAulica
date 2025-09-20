from itertools import combinations
from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.gestor_de_datos.día import Día
from asignacion_aulica.lógica_de_asignación.restricciones import no_superponer_clases
from asignacion_aulica.lógica_de_asignación import preferencias

@pytest.mark.aulas(
    dict(capacidad=30),
    dict(capacidad=40),
    dict(capacidad=25)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=31, día=Día.Lunes),
    dict(cantidad_de_alumnos=50, día=Día.Lunes),
    dict(cantidad_de_alumnos=100, día=Día.Lunes)
)
@pytest.mark.asignaciones_forzadas({ 0: 0, 1: 1, 2: 2 }) # Asignaciones arbitrarias (clase i con aula i)
def test_algunas_clases_exceden_capacidad(aulas_preprocesadas, clases_preprocesadas, rangos_de_aulas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes][0]
    cantidad_excedida, cota_superior = preferencias.cantidad_de_alumnos_fuera_del_aula(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    assert cota_superior == (31 - 30 + 50 - 40 + 100 - 25)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    # Como está forzado, la cantidad excedida es igual a su cota superior
    assert solver.value(cantidad_excedida) == cota_superior

@pytest.mark.aulas(
    dict(capacidad=250),
    dict(capacidad=400),
    dict(capacidad=100)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=31, día=Día.Lunes),
    dict(cantidad_de_alumnos=50, día=Día.Lunes),
    dict(cantidad_de_alumnos=100, día=Día.Lunes)
)
def test_ninguna_clase_excede_capacidad(aulas_preprocesadas, clases_preprocesadas, rangos_de_aulas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes][0]
    cantidad_excedida, cota_superior = preferencias.cantidad_de_alumnos_fuera_del_aula(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    # La cota superior sería 0, pero en cambio se devuelve 1 porque si no
    # fallaría al normalizar, siendo que debe dividir por la cota superior
    assert cota_superior == 1

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(cantidad_excedida) == 0

@pytest.mark.aulas(
    dict(capacidad=10),
    dict(capacidad=20),
    dict(capacidad=30)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=10, día=Día.Lunes),
    dict(cantidad_de_alumnos=20, día=Día.Lunes),
    dict(cantidad_de_alumnos=30, día=Día.Lunes)
)
def test_entran_justito(aulas_preprocesadas, clases_preprocesadas, rangos_de_aulas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes][0]

    # Restricciones para que no estén en el mismo aula
    for i_clase1, i_clase2 in combinations(range(len(clases_lunes)), 2):
        for i_aula in range(len(aulas_preprocesadas)):
            modelo.add( asignaciones[i_clase1, i_aula] + asignaciones[i_clase2, i_aula] <= 1 )

    # Minimizar capacidad excedida
    cantidad_excedida, cota_superior = preferencias.cantidad_de_alumnos_fuera_del_aula(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    assert cota_superior == (10 - 10 + 20 - 10 + 30 - 10)

    # Resolver
    modelo.minimize((1 / cota_superior) * cantidad_excedida)
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 0] == 1
    assert sum(asignaciones_finales[1,:]) == 1 and asignaciones_finales[1, 1] == 1
    assert sum(asignaciones_finales[2,:]) == 1 and asignaciones_finales[2, 2] == 1
    assert solver.value(cantidad_excedida) == 0

@pytest.mark.aulas(
    dict(capacidad=10),
    dict(capacidad=20),
    dict(capacidad=30)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=11, día=Día.Lunes),
    dict(cantidad_de_alumnos=21, día=Día.Lunes),
    dict(cantidad_de_alumnos=31, día=Día.Lunes)
)
def test_minimiza_capacidad_excedida(aulas_preprocesadas, clases_preprocesadas, rangos_de_aulas, modelo, asignaciones):
    '''
    Esta prueba es para verificar que minimiza la capacidad excedida en total, y
    no el número de aulas con capacidad excedida.

    La idea es que si minimizara el número de aulas pondría la materia más
    grande en el aula más chica y quedaría mucha gente afuera. En cambio si
    minimiza la gente que queda afuera, queda menos gente afuera.
    '''
    clases_lunes = clases_preprocesadas[Día.Lunes][0]

    # Restricciones para que no estén en el mismo aula
    for i_clase1, i_clase2 in combinations(range(len(clases_lunes)), 2):
        for i_aula in range(len(aulas_preprocesadas)):
            modelo.add( asignaciones[i_clase1, i_aula] + asignaciones[i_clase2, i_aula] <= 1 )

    # Minimizar capacidad excedida
    cantidad_excedida, cota_superior = preferencias.cantidad_de_alumnos_fuera_del_aula(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    assert cota_superior == (31 - 10 + 21 - 10 + 11 - 10)

    # Resolver
    modelo.minimize((1 / cota_superior) * cantidad_excedida)
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')

    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 0] == 1
    assert sum(asignaciones_finales[1,:]) == 1 and asignaciones_finales[1, 1] == 1
    assert sum(asignaciones_finales[2,:]) == 1 and asignaciones_finales[2, 2] == 1
    assert solver.value(cantidad_excedida) == 3
