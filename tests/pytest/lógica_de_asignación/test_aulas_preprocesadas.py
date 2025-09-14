from datetime import time

from asignacion_aulica.lógica_de_asignación import aulas_preprocesadas
from asignacion_aulica.lógica_de_asignación.aulas_preprocesadas import preprocesar_aulas, AulaPreprocesada
from asignacion_aulica.gestor_de_datos import Edificio, Aula

def test_un_solo_edificio():
    edificios = [Edificio(
        'nombre',
        (time(8), time(20)),
        (time(8), time(20)),
        (time(8), time(20)),
        (time(8), time(20)),
        (time(8), time(20)),
        (time(8), time(17)),
        (time(0), time(0))
    )]
    aulas = [
        Aula(
            'una',
            edificios[0].nombre,
            25,
            horario_lunes=(time(13), time(20)),
            equipamiento={'qué equipazo'}
        ),
        Aula(
            'otra',
            edificios[0].nombre,
            50,
            horario_lunes=(time(13), time(20)),
            horario_miércoles=(time(14), time(19)),
            horario_viernes=(time(15), time(18)),
            horario_domingo=(time(16), time(17))
        )
    ]
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            0,
            25,
            {'qué equipazo'},
            False,
            ((13*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 17*60), (0, 0)),
        ),
        AulaPreprocesada(
            0,
            50,
            set(),
            False,
            ((13*60, 20*60), (8*60, 20*60), (14*60, 19*60), (8*60, 20*60), (15*60, 18*60), (8*60, 17*60), (16*60, 17*60)),
        )
    ]

    assert preprocesar_aulas(edificios, aulas) == aulas_preprocesadas_esperadas

def test_varios_edificios():
    edificios = [
        Edificio(
            'nombre',
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(17)),
            (time(0), time(0))
        ),
        Edificio(
            'este no tiene ningún aula',
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(17)),
            (time(0), time(0))
        ),
        Edificio(
            'este si tiene aulas',
            (time(15), time(20)),
            (time(8, 30), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(20)),
            (time(8), time(17)),
            (time(0), time(0)),
            preferir_no_usar=True
        ),
    ]
    aulas = [
        Aula(
            'una',
            edificios[0].nombre,
            25,
            horario_lunes=(time(13), time(20)),
            equipamiento={'qué equipazo'}
        ),
        Aula(
            'otra',
            edificios[2].nombre,
            50,
        ),
        Aula(
            'otra más',
            edificios[2].nombre,
            31,
        )
    ]
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            0,
            25,
            {'qué equipazo'},
            False,
            ((13*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 17*60), (0, 0)),
        ),
        AulaPreprocesada(
            2,
            50,
            set(),
            True,
            ((15*60, 20*60), (8*60+30, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 17*60), (0, 0)),
        ),
        AulaPreprocesada(
            2,
            31,
            set(),
            True,
            ((15*60, 20*60), (8*60+30, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 20*60), (8*60, 17*60), (0, 0)),
        )
    ]

    assert preprocesar_aulas(edificios, aulas) == aulas_preprocesadas_esperadas

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
def test_aulas_dobles_ninguna(edificios, aulas):
    assert calcular_índices_de_aulas_dobles(edificios, aulas) == {}

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
    assert calcular_índices_de_aulas_dobles(edificios, aulas) == {
        0: (1, 2), 4: (5, 6), 8: (10, 12)
    }
