from ortools.sat.python import cp_model
import numpy as np
import pytest

from asignacion_aulica.lógica_de_asignación import preferencias
from helper_functions import make_aulas, make_clases, make_asignaciones

def test_todas_las_aulas_en_el_edificio_preferido():
    aulas = make_aulas(
        dict(edificio='preferido'),
        dict(edificio='preferido'),
        dict(edificio='preferido')
    )
    clases = make_clases(
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido')
    )
    modelo = cp_model.CpModel()

    # Forzar asignaciones arbitrarias
    asignaciones = make_asignaciones(clases, aulas, modelo, asignaciones_forzadas={ 0: 1, 1: 2 })

    clases_fuera_del_edificio_preferido, cota_superior = preferencias.obtener_cantidad_de_clases_fuera_del_edificio_preferido(clases, aulas, modelo, asignaciones)
    assert cota_superior == 2

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
    clases = make_clases(
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido 2'),
        dict(edificio_preferido='preferido'),
        dict(edificio_preferido='preferido 2'),
        dict(edificio_preferido=None)
    )
    modelo = cp_model.CpModel()

    # Forzar asignaciones arbitrarias
    asignaciones = make_asignaciones(clases, aulas, modelo, asignaciones_forzadas={ 0: 3, 1: 2, 2: 1, 3: 1, 4: 2, 5: 0 })

    clases_fuera_del_edificio_preferido, cota_superior = preferencias.obtener_cantidad_de_clases_fuera_del_edificio_preferido(clases, aulas, modelo, asignaciones)
    # La clase que no tiene edificio preferido no puede estar fuera de su
    # edificio preferido, y la cota máxima refleja este hecho
    assert cota_superior == 5

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
    clases = make_clases(
        dict(edificio_preferido='preferido'),
    )
    modelo = cp_model.CpModel()

    asignaciones = make_asignaciones(clases, aulas, modelo)

    clases_fuera_del_edificio_preferido, cota_superior = preferencias.obtener_cantidad_de_clases_fuera_del_edificio_preferido(clases, aulas, modelo, asignaciones)
    assert cota_superior == 1

    # Pedir al modelo minimizar cantidad de clases fuera del edificio preferido 
    modelo.minimize((1 / cota_superior) * clases_fuera_del_edificio_preferido)

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.solve(modelo)
    if status != cp_model.OPTIMAL:
        pytest.fail(f'El solver terminó con status {solver.status_name(status)}. Alguien escribió mal la prueba.')
    asignaciones_finales = np.vectorize(solver.value)(asignaciones)

    # La clase se debe asignar al aula en el edificio preferido
    assert sum(asignaciones_finales[0,:]) == 1 and asignaciones_finales[0, 2] == 1
    assert solver.value(clases_fuera_del_edificio_preferido) == 0
