from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.backend.preferencias import obtener_penalización
from helper_functions import *

def test_minimiza_capacidad_sobrante_y_excedida():
    '''
    Verifica que minimiza la capacidad sobrante y excedida, dando prioridad a la excedida.
    '''
    aulas = make_aulas(
        dict(capacidad=34, nombre="peor: sobrante=0, excedente=1"), 
        # Importante el orden, esta tiene que ser el de índice 1
        dict(capacidad=40, nombre="óptima: sobrante=5, excedente=0"),
        dict(capacidad=50, nombre="subótima: sobrante=15, excedente=0")
    )

    clases = make_clases(
        dict(cantidad_de_alumnos=35),
    )
    modelo = cp_model.CpModel()

    asignaciones = make_asignaciones(clases, aulas, modelo)

    # Minizar penalización, principalmente capacidad sobrante y excedida
    penalización = obtener_penalización(clases, aulas, modelo, asignaciones)
    modelo.minimize(penalización)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)

    # Espera que se asigne la clase al aula 1, y priorizando no exceder
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 1] == 1
    assert solver.value(penalización) > 0

