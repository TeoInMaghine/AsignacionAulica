from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.lógica_de_asignación.preprocesamiento import AulasPreprocesadas, ClasesPreprocesadasPorDía
from asignacion_aulica.lógica_de_asignación.preferencias import obtener_penalización
from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

from mocks import MockAula, MockClase

@pytest.mark.aulas(
    MockAula(capacidad=34, nombre="0 - peor: sobrante=0, excedente=1"),
    MockAula(capacidad=40, nombre="1 - óptima: sobrante=5, excedente=0"),
    MockAula(capacidad=50, nombre="2 - subótima: sobrante=15, excedente=0")
)
@pytest.mark.clases( MockClase(día=Día.Lunes, cantidad_de_alumnos=35) )
def test_minimiza_capacidad_sobrante_y_excedida(
    clases_preprocesadas: ClasesPreprocesadasPorDía,
    aulas_preprocesadas: AulasPreprocesadas,
    modelo: cp_model.CpModel,
    asignaciones: np.ndarray
):
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

