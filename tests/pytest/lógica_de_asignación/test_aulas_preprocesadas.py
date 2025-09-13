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
