from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.lógica_de_asignación.preferencias import obtener_penalización
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

@pytest.mark.aulas(
    dict(capacidad=34, nombre="1 - peor: sobrante=0, excedente=1"),
    # Importante el orden, esta tiene que ser el de índice 1
    dict(capacidad=40, nombre="2 - óptima: sobrante=5, excedente=0"),
    dict(capacidad=50, nombre="3 - subótima: sobrante=15, excedente=0")
)
@pytest.mark.clases( dict(día=Día.Lunes, cantidad_de_alumnos=35) )
def test_minimiza_capacidad_sobrante_y_excedida(clases_preprocesadas, aulas_preprocesadas, modelo, asignaciones):
    '''
    Verifica que minimiza la capacidad sobrante y excedida, dando prioridad a la excedida.
    '''
    # Minimizar penalización, principalmente capacidad sobrante y excedida
    clases_lunes = clases_preprocesadas[Día.Lunes]
    penalización = obtener_penalización(clases_lunes, aulas_preprocesadas, modelo, asignaciones)
    modelo.minimize(penalización)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)

    # Espera que se asigne la clase al aula 1, y priorizando no exceder
    assert sum(asignaciones_finales[0,:]) == 1, 'Se debería asignar a exactamente un aula.'
    assert asignaciones_finales[0, 1] == 1

