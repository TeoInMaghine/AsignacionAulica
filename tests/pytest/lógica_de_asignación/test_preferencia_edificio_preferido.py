from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.gestor_de_datos.día import Día
from asignacion_aulica.lógica_de_asignación import preferencias

@pytest.mark.edificios(dict(nombre='preferido'))
@pytest.mark.aulas(
    dict(edificio='preferido'),
    dict(edificio='preferido'),
    dict(edificio='preferido')
)
@pytest.mark.carreras(dict(nombre='c', edificio_preferido='preferido'))
@pytest.mark.materias(dict(nombre='m', carrera='c'))
@pytest.mark.clases(
    dict(carrera='c', materia='m', día=Día.Lunes),
    dict(carrera='c', materia='m', día=Día.Lunes)
)
@pytest.mark.asignaciones_forzadas({ 0: 1, 1: 2 })
def test_todas_las_aulas_en_el_edificio_preferido(aulas_preprocesadas, clases_preprocesadas, rangos_de_aulas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes][0]
    clases_fuera_del_edificio_preferido, cota_superior = preferencias.cantidad_de_clases_fuera_del_edificio_preferido(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    assert cota_superior == 2

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(clases_fuera_del_edificio_preferido) == 0

@pytest.mark.edificios(
    dict(nombre='a preferido'),
    dict(nombre='b no preferido'),
    dict(nombre='c preferido')
)
@pytest.mark.aulas(
    dict(nombre='0', edificio='a preferido'),
    dict(nombre='1', edificio='a preferido'),
    dict(nombre='2', edificio='b no preferido'),
    dict(nombre='3', edificio='c preferido')
)
@pytest.mark.carreras(
    dict(nombre='a', edificio_preferido='a preferido'),
    dict(nombre='b', edificio_preferido='c preferido'),
    dict(nombre='c', edificio_preferido=None)
)
@pytest.mark.materias(
    dict(nombre='a', carrera='a'),
    dict(nombre='b', carrera='b'),
    dict(nombre='c', carrera='c')
)
@pytest.mark.clases(
    dict(carrera='a', materia='a', día=Día.Lunes),
    dict(carrera='a', materia='a', día=Día.Lunes),
    dict(carrera='b', materia='b', día=Día.Lunes),
    dict(carrera='a', materia='a', día=Día.Lunes),
    dict(carrera='b', materia='b', día=Día.Lunes),
    dict(carrera='c', materia='c', día=Día.Lunes)
)
@pytest.mark.asignaciones_forzadas({ 0: 2, 1: 1, 2: 2, 3: 2, 4: 0, 5: 0 })
def test_algunas_aulas_en_el_edificio_preferido(aulas_preprocesadas, clases_preprocesadas, rangos_de_aulas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes][0]
    clases_fuera_del_edificio_preferido, cota_superior = preferencias.cantidad_de_clases_fuera_del_edificio_preferido(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    # La clase que no tiene edificio preferido no puede estar fuera de su
    # edificio preferido, y la cota máxima refleja este hecho
    assert cota_superior == len(clases_lunes) - 1

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    assert solver.value(clases_fuera_del_edificio_preferido) == 4

@pytest.mark.edificios(
    dict(nombre='0 no preferido'),
    dict(nombre='1 no preferido'),
    dict(nombre='2 preferido'), # Importante el orden, tiene que ser el índice 2
    dict(nombre='3 no preferido'),
    dict(nombre='4 no preferido')
)
@pytest.mark.aulas(
    dict(nombre='0', edificio='0 no preferido'),
    dict(nombre='1', edificio='1 no preferido'),
    dict(nombre='2', edificio='2 preferido'), # Importante el orden, tiene que ser el índice 2
    dict(nombre='3', edificio='3 no preferido'),
    dict(nombre='4', edificio='4 no preferido')
)
@pytest.mark.carreras(dict(nombre='c', edificio_preferido='2 preferido') )
@pytest.mark.materias(dict(nombre='m', carrera='c'))
@pytest.mark.clases(dict(carrera='c', materia='m', día=Día.Lunes))
def test_elije_aula_en_edificio_preferido(aulas_preprocesadas, clases_preprocesadas, rangos_de_aulas, modelo, asignaciones):
    clases_lunes = clases_preprocesadas[Día.Lunes][0]
    clases_fuera_del_edificio_preferido, cota_superior = preferencias.cantidad_de_clases_fuera_del_edificio_preferido(clases_lunes, aulas_preprocesadas, rangos_de_aulas, modelo, asignaciones)
    assert cota_superior == 1

    # Pedir al modelo minimizar cantidad de clases fuera del edificio preferido 
    modelo.minimize((1 / cota_superior) * clases_fuera_del_edificio_preferido)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    
    # La clase se debe asignar al aula en el edificio preferido
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 2] == 1
    assert solver.value(clases_fuera_del_edificio_preferido) == 0
