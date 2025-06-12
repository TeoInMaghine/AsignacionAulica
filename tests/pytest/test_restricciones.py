from helper_functions import *

from asignacion_aulica.backend.lógica_de_asignación import crear_matriz_de_asignaciones
from asignacion_aulica.backend import restricciones

# TODO: Arreglar los assert de estos tests. O no lol.
# Para el que prueba no_superponer_clases sería el único que "haría falta" ver
# los predicados (o borrar el test xd). Para el resto se podría verificar que
# se seteen constantes en la matriz de asignaciones.

def test_superposición():
    aulas = make_aulas({})
    clases = make_clases(
        dict(horario_inicio=1, horario_fin=3),
        dict(horario_inicio=2, horario_fin=4),
        dict(horario_inicio=5, horario_fin=6)
    )
    modelo = cp_model.CpModel()

    asignaciones = crear_matriz_de_asignaciones(clases, aulas, modelo)

    predicados = list(restricciones.no_superponer_clases(clases, aulas, asignaciones))

    # Debería generar solamente un predicado entre las primeras dos clases
    assert len(predicados) == 1
    predicado = predicados[0]
    assert predicado_es_nand_entre_dos_variables_bool(predicado)
    assert asignaciones[0,0] in predicado.vars
    assert asignaciones[0,0] in predicado.vars

def test_aulas_cerradas():
    aulas = make_aulas(
        dict(horario_apertura=10, horario_cierre=13), # Igual que la clase
        dict(horario_apertura=10, horario_cierre=11), # Cierra temprano
        dict(horario_apertura=11, horario_cierre=13), # Abre tarde
        dict(horario_apertura=9,  horario_cierre=14), # Sobra
        dict(horario_apertura=11, horario_cierre=12), # Abre tarde y cierra temprano
    )
    clases = make_clases(
        dict(horario_inicio=10, horario_fin=13)
    )
    modelo = cp_model.CpModel()
    asignaciones = crear_matriz_de_asignaciones(clases, aulas, modelo)

    prohibidas = list(restricciones.no_asignar_en_aula_cerrada(clases, aulas))

    # Debería generar restricciones con las aulas 1, 2, y 4
    assert len(prohibidas) == 3
    assert (0, 1) in prohibidas
    assert (0, 2) in prohibidas
    assert (0, 4) in prohibidas

def test_capacidad_suficiente():
    aulas = make_aulas(
        dict(capacidad = 100),
        dict(capacidad = 50),
        dict(capacidad = 10)
    )
    clases = make_clases(
        dict(cantidad_de_alumnos = 50)
    )
    modelo = cp_model.CpModel()
    asignaciones = crear_matriz_de_asignaciones(clases, aulas, modelo)

    prohibidas = list(restricciones.asignar_aulas_con_capacidad_suficiente(clases, aulas))

    # Debería generar una sola restricción con el aula 2
    assert len(prohibidas) == 1
    assert (0, 2) in prohibidas

def test_equipamiento():
    aulas = make_aulas(
        dict(equipamiento = set(('proyector',))),
        dict(equipamiento = set(('proyector', 'otra cosa'))),
        dict(equipamiento = set())
    )
    clases = make_clases(
        dict(equipamiento_necesario = set(('proyector',)))
    )
    modelo = cp_model.CpModel()
    asignaciones = crear_matriz_de_asignaciones(clases, aulas, modelo)

    prohibidas = list(restricciones.asignar_aulas_con_el_equipamiento_requerido(clases, aulas))

    # Debería generar una sola restricción con el aula 2
    assert len(prohibidas) == 1
    assert (0, 2) in prohibidas

