from ortools.sat.python import cp_model
from itertools import combinations
import numpy as np
import pytest

from asignacion_aulica.lógica_de_asignación.restricciones import no_superponer_clases
from asignacion_aulica.lógica_de_asignación import preferencias
from asignacion_aulica.gestor_de_datos.día import Día

@pytest.mark.aulas(
    dict(capacidad=31),
    dict(capacidad=50),
    dict(capacidad=100)
)
@pytest.mark.clases(
    dict(cantidad_de_alumnos=30, día=Día.Lunes),
    dict(cantidad_de_alumnos=40, día=Día.Lunes),
    dict(cantidad_de_alumnos=25, día=Día.Lunes)
    )
@pytest.mark.asignaciones_forzadas({ 0: 0, 1: 1, 2: 2 }) # Asignaciones arbitrarias: clase i con aula i
def test_a_algunas_clases_les_sobra_capacidad(aulas_preprocesadas, clases_preprocesadas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    cantidad_sobrante, cota_superior = preferencias.capacidad_sobrante(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
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
    dict(cantidad_de_alumnos=250, día=Día.Lunes),
    dict(cantidad_de_alumnos=400, día=Día.Lunes),
    dict(cantidad_de_alumnos=100, día=Día.Lunes)
)
def test_a_ninguna_clase_le_sobra_capacidad(aulas_preprocesadas, clases_preprocesadas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    cantidad_sobrante, cota_superior = preferencias.capacidad_sobrante(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
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
    dict(cantidad_de_alumnos=10, día=Día.Lunes),
    dict(cantidad_de_alumnos=20, día=Día.Lunes),
    dict(cantidad_de_alumnos=30, día=Día.Lunes)
)
def test_entran_justito(aulas_preprocesadas, clases_preprocesadas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes]

    # Restricciones para que no estén en el mismo aula
    for i_clase1, i_clase2 in combinations(range(len(clases_lunes.clases)), 2):
        for i_aula in range(len(aulas_preprocesadas.aulas)):
            modelo.add( asignaciones[i_clase1, i_aula] + asignaciones[i_clase2, i_aula] <= 1 )

    # Minimizar capacidad sobrante
    cantidad_sobrante, cota_superior = preferencias.capacidad_sobrante(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
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
    dict(cantidad_de_alumnos=10, día=Día.Lunes),
    dict(cantidad_de_alumnos=20, día=Día.Lunes),
    dict(cantidad_de_alumnos=30, día=Día.Lunes)
)
def test_minimiza_capacidad_sobrante(aulas_preprocesadas, clases_preprocesadas, modelo, asignaciones):
    '''
    Esta prueba es para verificar que minimiza la capacidad sobrante en total, y
    no el número de aulas con capacidad sobrante.

    La idea es que si minimizara el número de aulas pondría la materia más
    chica en el aula más grande y quedaría mucha gente afuera. En cambio si
    minimiza la gente que queda afuera, queda menos gente afuera.
    '''
    clases_lunes = clases_preprocesadas[Día.Lunes]

    # Restricciones para que no estén en el mismo aula
    for i_clase1, i_clase2 in combinations(range(len(clases_lunes.clases)), 2):
        for i_aula in range(len(aulas_preprocesadas.aulas)):
            modelo.add( asignaciones[i_clase1, i_aula] + asignaciones[i_clase2, i_aula] <= 1 )

    # Minimizar capacidad sobrante
    cantidad_sobrante, cota_superior = preferencias.capacidad_sobrante(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
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
