from datetime import time

import pytest

from asignacion_aulica.gestor_de_datos.día import Día
from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulaPreprocesada,
    AulasPreprocesadas,
    ClasesPreprocesadas,
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
def test_rango_de_aulas_por_edificio(edificios, aulas):
    rangos_esperados = {'edificio 0': slice(0, 3), 'edificio 1': slice(3, 6), 'edificio 2': slice(6, 7)}
    aulas_preprocesadas = AulasPreprocesadas(edificios, aulas)
    assert aulas_preprocesadas.rangos_de_aulas == rangos_esperados

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
def test_preprocesar_aulas_un_solo_edificio(edificios, aulas):
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            capacidad=25,
            equipamiento={'qué equipazo'},
            horarios=(
                (time(13), time(20)), (time(8), time(20)),
                (time(8), time(20)), (time(8), time(20)),
                (time(8), time(20)), (time(8), time(17)),
                (time(0), time(0))
            )
        ),
        AulaPreprocesada(
            capacidad=50,
            equipamiento=set(),
            horarios=(
                (time(13), time(20)), (time(8), time(20)),
                (time(14), time(19)), (time(8), time(20)),
                (time(15), time(18)), (time(8), time(17)),
                (time(16), time(17))
            )
        )
    ]
    aulas_preprocesadas = AulasPreprocesadas(edificios, aulas)
    assert aulas_preprocesadas.aulas == aulas_preprocesadas_esperadas
    assert aulas_preprocesadas.rangos_de_aulas == {'nombre': slice(0,2)}
    assert aulas_preprocesadas.preferir_no_usar == []
    assert aulas_preprocesadas.aulas_dobles == {}

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
def test_preprocesar_aulas_varios_edificios(edificios, aulas):
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            capacidad=25,
            equipamiento={'qué equipazo'},
            horarios=(
                (time(13), time(20)), (time(8), time(20)), (time(8), time(20)),
                (time(8), time(20)), (time(8), time(20)), (time(8), time(17)),
                (time(0), time(0))
            ),
        ),
        AulaPreprocesada(
            capacidad=50,
            equipamiento=set(),
            horarios=(
                (time(15), time(20)), (time(8, 30), time(20)),
                (time(8), time(20)), (time(8), time(20)), (time(8), time(20)),
                (time(8), time(17)), (time(0), time(0))
            )
        ),
        AulaPreprocesada(
            capacidad=31,
            equipamiento=set(),
            horarios=(
                (time(15), time(20)), (time(8, 30), time(20)),
                (time(8), time(20)), (time(8), time(20)), (time(8), time(20)),
                (time(8), time(17)), (time(0), time(0))
            )
        )
    ]

    aulas_preprocesadas = AulasPreprocesadas(edificios, aulas)
    assert aulas_preprocesadas.aulas == aulas_preprocesadas_esperadas
    assert aulas_preprocesadas.rangos_de_aulas == {'Anasagasti 1': slice(0,1), 'Anasagasti 2': slice(1,1), 'Anasagasti 3': slice(1,3)}
    assert aulas_preprocesadas.preferir_no_usar == [1, 2]
    assert aulas_preprocesadas.aulas_dobles == {}

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
def test_aulas_dobles_en_varios_edificios(edificios, aulas):
    aulas_dobles_esperadas = {0: (1, 2), 4: (5, 6), 8: (10, 12)}
    aulas_preprocesadas = AulasPreprocesadas(edificios, aulas)
    assert aulas_preprocesadas.aulas_dobles == aulas_dobles_esperadas

@pytest.mark.edificios(dict(nombre='abc'), dict(nombre='def'))
@pytest.mark.aulas(
    dict(edificio='abc', nombre='1'),
    dict(edificio='def', nombre='33'),
    dict(edificio='ghi')
)
@pytest.mark.clases(
    dict(día=Día.Lunes, horario_inicio=time(10), horario_fin=time(15), no_cambiar_asignación=True, aula='1', edificio='abc'),
    dict(día=Día.Lunes, horario_inicio=time(1)),
    dict(día=Día.Lunes, horario_inicio=time(20), horario_fin=time(23), no_cambiar_asignación=True, aula='33', edificio='def'),
    dict(día=Día.Lunes, horario_inicio=time(2)),
    dict(día=Día.Lunes, horario_inicio=time(3))
)
def test_separar_asignaciones_manuales(clases, materias, carreras, aulas_preprocesadas):
    clases_preprocesadas = preprocesar_clases(carreras, materias, clases, aulas_preprocesadas)
    clases_lunes = clases_preprocesadas[Día.Lunes]
    assert len(clases_lunes.clases) == 3
    assert clases_lunes.clases[0].horario_inicio == time(1)
    assert clases_lunes.clases[1].horario_inicio == time(2)
    assert clases_lunes.clases[2].horario_inicio == time(3)
    assert clases_lunes.índices_originales == [1, 3, 4]
    assert clases_lunes.aulas_ocupadas == [('abc', '1', time(10), time(15)), ('def', '33', time(20), time(23))]

@pytest.mark.clases(
    dict(materia='1', día=Día.Martes),
    dict(materia='2', día=Día.Jueves),
    dict(materia='2', día=Día.Martes),
    dict(materia='2', día=Día.Sábado),
    dict(materia='3', día=Día.Martes),
    dict(materia='4', día=Día.Lunes)
)
def test_separar_clases_por_día(clases, materias, carreras, aulas_preprocesadas):
    clases_preprocesadas = preprocesar_clases(carreras, materias, clases, aulas_preprocesadas)
    
    # Lunes
    assert len(clases_preprocesadas[Día.Lunes].clases) == 1
    assert clases_preprocesadas[Día.Lunes].clases[0].materia == '4'
    assert clases_preprocesadas[Día.Lunes].índices_originales == [5]
    assert clases_preprocesadas[Día.Lunes].aulas_ocupadas == []

    # Martes
    assert len(clases_preprocesadas[Día.Martes].clases) == 3
    assert clases_preprocesadas[Día.Martes].clases[0].materia == '1'
    assert clases_preprocesadas[Día.Martes].clases[1].materia == '2'
    assert clases_preprocesadas[Día.Martes].clases[2].materia == '3'
    assert clases_preprocesadas[Día.Martes].índices_originales == [0, 2, 4]
    assert clases_preprocesadas[Día.Martes].aulas_ocupadas == []

    # Jueves
    assert len(clases_preprocesadas[Día.Jueves].clases) == 1
    assert clases_preprocesadas[Día.Jueves].clases[0].materia == '2'
    assert clases_preprocesadas[Día.Jueves].índices_originales == [1]
    assert clases_preprocesadas[Día.Jueves].aulas_ocupadas == []

    # Sábado
    assert len(clases_preprocesadas[Día.Sábado].clases) == 1
    assert clases_preprocesadas[Día.Sábado].clases[0].materia == '2'
    assert clases_preprocesadas[Día.Sábado].índices_originales == [3]
    assert clases_preprocesadas[Día.Sábado].aulas_ocupadas == []

    # Los otros días
    sin_clases = ClasesPreprocesadas([], [], [], [])
    assert clases_preprocesadas[Día.Miércoles] == sin_clases
    assert clases_preprocesadas[Día.Viernes] == sin_clases
    assert clases_preprocesadas[Día.Domingo] == sin_clases

@pytest.mark.edificios(dict(nombre='no preferido'), dict(nombre='preferido'))
@pytest.mark.aulas(
    dict(edificio='no preferido'),
    dict(edificio='no preferido'),
    dict(edificio='no preferido'),
    dict(edificio='preferido'),
    dict(edificio='preferido')
)
@pytest.mark.carreras(dict(nombre='c1'))
@pytest.mark.carreras(dict(nombre='c2', edificio_preferido='preferido'))
@pytest.mark.materias(dict(nombre='m1', carrera='c1'))
@pytest.mark.materias(dict(nombre='m2', carrera='c2'))
@pytest.mark.clases(
    dict(carrera='c1', materia='m1', día=Día.Lunes),
    dict(carrera='c1', materia='m1', día=Día.Jueves),
    dict(carrera='c2', materia='m2', día=Día.Jueves)
    
)
def test_preprocesar_clases_con_edificio_preferido(clases, materias, carreras, aulas_preprocesadas):
    clases_preprocesadas = preprocesar_clases(carreras, materias, clases, aulas_preprocesadas)
    assert clases_preprocesadas[Día.Lunes].rangos_de_aulas_preferidas == []
    assert clases_preprocesadas[Día.Jueves].rangos_de_aulas_preferidas == [(slice(1, 2), slice(3, 5))]
