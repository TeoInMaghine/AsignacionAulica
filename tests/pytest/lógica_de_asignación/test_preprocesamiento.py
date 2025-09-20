from datetime import time

import pytest

from asignacion_aulica.gestor_de_datos.día import Día
from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulaPreprocesada,
    calcular_rango_de_aulas_por_edificio,
    preprocesar_aulas,
    calcular_índices_de_aulas_dobles,
    preprocesar_clases
)

@pytest.mark.edificios({}, {}, {})
@pytest.mark.aulas(
    dict(edificio='edificio 0'),
    dict(edificio='edificio 0'),
    dict(edificio='edificio 0'),
    dict(edificio='edificio 1'),
    dict(edificio='edificio 1'),
    dict(edificio='edificio 1'),
    dict(edificio='edificio 2'),
)
def test_calcular_rango_de_aulas_por_edificio(edificios, aulas):
    rangos_esperados = {'edificio 0': (0, 3), 'edificio 1': (3, 6), 'edificio 2': (6, 7)}
    assert calcular_rango_de_aulas_por_edificio(edificios, aulas) == rangos_esperados

@pytest.mark.edificios(dict(
    nombre = 'nombre',
    horario_lunes =     (time(8), time(20)),
    horario_martes =    (time(8), time(20)),
    horario_miércoles = (time(8), time(20)),
    horario_jueves =    (time(8), time(20)),
    horario_viernes =   (time(8), time(20)),
    horario_sábado =    (time(8), time(17)),
    horario_domingo =   (time(0), time(0))
))
@pytest.mark.aulas(
    dict(
        nombre='una',
        edificio='nombre',
        capacidad=25,
        horario_lunes=(time(13), time(20)),
        equipamiento={'qué equipazo'}
    ),
    dict(
        nombre='y otra',
        edificio='nombre',
        capacidad=50,
        horario_lunes=(time(13), time(20)),
        horario_miércoles=(time(14), time(19)),
        horario_viernes=(time(15), time(18)),
        horario_domingo=(time(16), time(17))
    )
)
def test_preprocesar_aulas_un_solo_edificio(edificios, aulas, rangos_de_aulas):
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            0,
            25,
            {'qué equipazo'},
            False,
            ((time(13), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(17)), (time(0), time(0))),
        ),
        AulaPreprocesada(
            0,
            50,
            set(),
            False,
            ((time(13), time(20)), (time(8), time(20)), (time(14), time(19)), (time(8), time(20)), (time(15), time(18)), (time(8), time(17)), (time(16), time(17))),
        )
    ]
    assert preprocesar_aulas(edificios, aulas, rangos_de_aulas) == aulas_preprocesadas_esperadas

@pytest.mark.edificios(
    dict(
        nombre = 'Anasagasti 1',
        horario_lunes =     (time(8), time(20)),
        horario_martes =    (time(8), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0))
    ),
    dict(
        nombre = 'Anasagasti 2',
        horario_lunes =     (time(8), time(20)),
        horario_martes =    (time(8), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0))
    ),
    dict(
        nombre = 'Anasagasti 3',
        horario_lunes =     (time(15), time(20)),
        horario_martes =    (time(8, 30), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0)),
        preferir_no_usar = True
    )
)
@pytest.mark.aulas(
    dict(
        nombre='A102',
        edificio='Anasagasti 1',
        capacidad=25,
        horario_lunes=(time(13), time(20)),
        equipamiento={'qué equipazo'}
    ),
    # Ningún aula en Anasagasti 2
    dict(
        nombre='C306',
        edificio='Anasagasti 3',
        capacidad=50
    ),
    dict(
        nombre='C345',
        edificio='Anasagasti 3',
        capacidad=31
    )
)
def test_preprocesar_aulas_varios_edificios(edificios, aulas, rangos_de_aulas):
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            0,
            25,
            {'qué equipazo'},
            False,
            ((time(13), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(17)), (time(0), time(0))),
        ),
        AulaPreprocesada(
            2,
            50,
            set(),
            True,
            ((time(15), time(20)), (time(8, 30), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(17)), (time(0), time(0))),
        ),
        AulaPreprocesada(
            2,
            31,
            set(),
            True,
            ((time(15), time(20)), (time(8, 30), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(20)), (time(8), time(17)), (time(0), time(0))),
        )
    ]

    assert preprocesar_aulas(edificios, aulas, rangos_de_aulas) == aulas_preprocesadas_esperadas

@pytest.mark.edificios(
    dict(
        nombre = 'Anasagasti 1',
        horario_lunes =     (time(8), time(20)),
        horario_martes =    (time(8), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0))
    ),
    dict(
        nombre = 'Anasagasti 2',
        horario_lunes =     (time(8), time(20)),
        horario_martes =    (time(8), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0))
    ),
    dict(
        nombre = 'Anasagasti 3',
        horario_lunes =     (time(15), time(20)),
        horario_martes =    (time(8, 30), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0)),
        preferir_no_usar = True
    )
)
@pytest.mark.aulas(
    dict(
        nombre='A102',
        edificio='Anasagasti 1',
        capacidad=25,
        horario_lunes=(time(13), time(20)),
        equipamiento={'qué equipazo'}
    ),
    # Ningún aula en Anasagasti 2
    dict(
        nombre='C306',
        edificio='Anasagasti 3',
        capacidad=50
    ),
    dict(
        nombre='C345',
        edificio='Anasagasti 3',
        capacidad=31
    )
)
def test_aulas_dobles_ninguna(edificios, aulas, rangos_de_aulas):
    assert calcular_índices_de_aulas_dobles(edificios, aulas, rangos_de_aulas) == {}

@pytest.mark.edificios(
    dict(
        nombre = 'Anasagasti 1',
        horario_lunes =     (time(8), time(20)),
        horario_martes =    (time(8), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0)),
        aulas_dobles = {'A102': ('A102A', 'A102B')}
    ),
    dict(
        nombre = 'Anasagasti 2',
        horario_lunes =     (time(8), time(20)),
        horario_martes =    (time(8), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0)),
        aulas_dobles = {'B102': ('B102A', 'B102B'), 'B202': ('B202B', 'B202D')}
    ),
    dict(
        nombre = 'Anasagasti 3',
        horario_lunes =     (time(15), time(20)),
        horario_martes =    (time(8, 30), time(20)),
        horario_miércoles = (time(8), time(20)),
        horario_jueves =    (time(8), time(20)),
        horario_viernes =   (time(8), time(20)),
        horario_sábado =    (time(8), time(17)),
        horario_domingo =   (time(0), time(0)),
        preferir_no_usar = True
    )
)
@pytest.mark.aulas(
    dict(nombre='A102', edificio='Anasagasti 1'),
    dict(nombre='A102A', edificio='Anasagasti 1'),
    dict(nombre='A102B', edificio='Anasagasti 1'),
    dict(nombre='A103', edificio='Anasagasti 1'),
    dict(nombre='B102', edificio='Anasagasti 2'),
    dict(nombre='B102A', edificio='Anasagasti 2'),
    dict(nombre='B102B', edificio='Anasagasti 2'),
    dict(nombre='B103', edificio='Anasagasti 2'),
    dict(nombre='B202', edificio='Anasagasti 2'),
    dict(nombre='B202A', edificio='Anasagasti 2'),
    dict(nombre='B202B', edificio='Anasagasti 2'),
    dict(nombre='B202C', edificio='Anasagasti 2'),
    dict(nombre='B202D', edificio='Anasagasti 2'),
    dict(nombre='B202', edificio='Anasagasti 3'), # No son aulas dobles, pero tienen los mismos nombres que en el otro edificio
    dict(nombre='B202A', edificio='Anasagasti 3'),
    dict(nombre='B202B', edificio='Anasagasti 3')
)
def test_aulas_dobles_en_varios_edificios(edificios, aulas, rangos_de_aulas):
    aulas_dobles = {0: (1, 2), 4: (5, 6), 8: (10, 12)}
    assert calcular_índices_de_aulas_dobles(edificios, aulas, rangos_de_aulas) == aulas_dobles

@pytest.mark.clases(
    dict(aula='1', edificio='abc', no_cambiar_asignación=True, día=Día.Lunes, horario_inicio=time(10), horario_fin=time(15)),
    dict(día=Día.Lunes, horario_inicio=time(1)),
    dict(aula='33', edificio='def', no_cambiar_asignación=True, día=Día.Lunes, horario_inicio=time(20), horario_fin=time(23)),
    dict(día=Día.Lunes, horario_inicio=time(2)),
    dict(día=Día.Lunes, horario_inicio=time(3))
)
def test_separar_asignaciones_manuales(clases, materias, carreras):
    clases_preprocesadas = preprocesar_clases(clases, materias, carreras)
    clases_a_asignar, índices, aulas_ocupadas = clases_preprocesadas[Día.Lunes]

    assert len(clases_a_asignar) == 3
    assert clases_a_asignar[0].horario_inicio == time(1)
    assert clases_a_asignar[1].horario_inicio == time(2)
    assert clases_a_asignar[2].horario_inicio == time(3)
    assert índices == [1, 3, 4]
    assert aulas_ocupadas == {('abc', '1', time(10), time(15)), ('def', '33', time(20), time(23))}

@pytest.mark.clases(
    dict(materia='1', día=Día.Martes),
    dict(materia='2', día=Día.Jueves),
    dict(materia='2', día=Día.Martes),
    dict(materia='2', día=Día.Sábado),
    dict(materia='3', día=Día.Martes),
    dict(materia='4', día=Día.Lunes)
)
def test_separar_clases_por_día(clases, materias, carreras):
    clases_preprocesadas = preprocesar_clases(clases, materias, carreras)
    
    # Lunes
    clases_a_asignar, índices, aulas_ocupadas = clases_preprocesadas[Día.Lunes]
    assert len(clases_a_asignar) == 1
    assert clases_a_asignar[0].materia == '4'
    assert índices == [5]
    assert aulas_ocupadas == set()

    # Martes
    clases_a_asignar, índices, aulas_ocupadas = clases_preprocesadas[Día.Martes]
    assert len(clases_a_asignar) == 3
    assert clases_a_asignar[0].materia == '1'
    assert clases_a_asignar[1].materia == '2'
    assert clases_a_asignar[2].materia == '3'
    assert índices == [0, 2, 4]
    assert aulas_ocupadas == set()

    # Jueves
    clases_a_asignar, índices, aulas_ocupadas = clases_preprocesadas[Día.Jueves]
    assert len(clases_a_asignar) == 1
    assert clases_a_asignar[0].materia == '2'
    assert índices == [1]
    assert aulas_ocupadas == set()

    # Sábado
    clases_a_asignar, índices, aulas_ocupadas = clases_preprocesadas[Día.Sábado]
    assert len(clases_a_asignar) == 1
    assert clases_a_asignar[0].materia == '2'
    assert índices == [3]
    assert aulas_ocupadas == set()

    # Los otros días
    assert clases_preprocesadas[Día.Miércoles] == ([], [], set())
    assert clases_preprocesadas[Día.Viernes] == ([], [], set())
    assert clases_preprocesadas[Día.Domingo] == ([], [], set())

@pytest.mark.carreras(dict(nombre='c', edificio_preferido='preferido'))
@pytest.mark.materias(dict(nombre='m', carrera='c'))
@pytest.mark.clases(
    dict(carrera='c', materia='m', día=Día.Lunes),
    dict(carrera='c', materia='m', día=Día.Jueves)
)
def test_preprocesar_clases_con_edificio_preferido(clases, materias, carreras):
    clases_preprocesadas = preprocesar_clases(clases, materias, carreras)
    assert clases_preprocesadas[Día.Lunes][0][0].edificio_preferido == 'preferido'
    assert clases_preprocesadas[Día.Jueves][0][0].edificio_preferido == 'preferido'
