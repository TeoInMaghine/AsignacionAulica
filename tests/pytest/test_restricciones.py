from helper_functions import *
from asignacion_aulica.backend import restricciones

def test_superposición():
    aulas = make_aulas({})
    clases, modelo = make_clases(
        len(aulas),
        dict(horario_inicio=1, horario_fin=3),
        dict(horario_inicio=2, horario_fin=4),
        dict(horario_inicio=5, horario_fin=6)
    )

    predicados = list(restricciones.no_superponer_clases(clases, aulas))

    # Debería generar solamente un predicado entre las primeras dos clases
    assert len(predicados) == 1
    predicado = predicados[0]
    assert predicado_es_not_equals_entre__dos_variables(predicado)
    assert clases.loc[0, 'aula_asignada'] in predicado.vars
    assert clases.loc[1, 'aula_asignada'] in predicado.vars

def test_aulas_cerradas():
    aulas = make_aulas(
        dict(horario_apertura=10, horario_cierre=13), # Igual que la clase
        dict(horario_apertura=10, horario_cierre=11), # Cierra temprano
        dict(horario_apertura=11, horario_cierre=13), # Abre tarde
        dict(horario_apertura=9,  horario_cierre=14), # Sobra
        dict(horario_apertura=11, horario_cierre=12), # Abre tarde y cierra temprano
        )
    clases, modelo = make_clases(
        len(aulas),
        dict(horario_inicio=10, horario_fin=13)
    )

    predicados = list(restricciones.no_asignar_en_aula_cerrada(clases, aulas))

    # Debería generar restricciones con las aulas 1, 2, y 4
    assert len(predicados) == 3
    assert any(predicado_es_not_equals_entre_variable_y_constante(p, 1) for p in predicados)
    assert any(predicado_es_not_equals_entre_variable_y_constante(p, 2) for p in predicados)
    assert any(predicado_es_not_equals_entre_variable_y_constante(p, 4) for p in predicados)

def test_capacidad_suficiente():
    aulas = make_aulas(
        dict(capacidad = 100),
        dict(capacidad = 10)
        )
    clases, modelo = make_clases(
        len(aulas),
        dict(cantidad_de_alumnos = 50)
    )

    predicados = list(restricciones.asignar_aulas_con_capacidad_suficiente(clases, aulas))

    # Debería generar una sola restricción con el aula 2
    assert len(predicados) == 1
    assert predicado_es_not_equals_entre_variable_y_constante(predicados[0], 2)

def test_equipamiento():
    aulas = make_aulas(
        dict(equipamiento = set(('proyector',))),
        dict(equipamiento = set(('proyector', 'otra cosa'))),
        dict(equipamiento = set())
    )
    clases, modelo = make_clases(
        len(aulas),
        dict(equipamiento_necesario = set(('proyector',)))
    )

    predicados = list(restricciones.asignar_aulas_con_el_equipamiento_requerido(clases, aulas))

    # Debería generar una sola restricción con el aula 2
    assert len(predicados) == 1
    assert predicado_es_not_equals_entre_variable_y_constante(predicados[0], 2)
