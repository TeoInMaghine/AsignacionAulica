from datetime import time
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import HorariosSemanales, RangoHorario, Día
from asignacion_aulica.gestor_de_datos.entidades import Carreras, Edificios
from asignacion_aulica.lógica_de_asignación.preprocesamiento import (
    AulaPreprocesada,
    AulasPreprocesadas,
    ClasesPreprocesadas,
    preprocesar_clases
)

from mocks import MockCarrera, MockClase, MockEdificio, MockAula, MockMateria

@pytest.mark.edificios(
    MockEdificio(aulas=(MockAula(), MockAula(), MockAula())),
    MockEdificio(aulas=(MockAula(), MockAula(), MockAula())),
    MockEdificio(aulas=(MockAula(), )),
)
def test_rango_de_aulas_por_edificio(edificios: Edificios):
    rangos_esperados = {'edificio 0': slice(0, 3), 'edificio 1': slice(3, 6), 'edificio 2': slice(6, 7)}
    aulas_preprocesadas = AulasPreprocesadas(edificios)
    assert aulas_preprocesadas.rangos_de_aulas == rangos_esperados

@pytest.mark.edificios(MockEdificio(
    nombre='nombre',
    horario_lunes =     RangoHorario(time(8), time(20)),
    horario_martes =    RangoHorario(time(8), time(20)),
    horario_miércoles = RangoHorario(time(8), time(20)),
    horario_jueves =    RangoHorario(time(8), time(20)),
    horario_viernes =   RangoHorario(time(8), time(20)),
    horario_sábado =    RangoHorario(time(8), time(17)),
    horario_domingo =   RangoHorario(time(0), time(0)),
    aulas=(
        MockAula(
            nombre='una',
            capacidad=25,
            horario_lunes=RangoHorario(time(13), time(20)),
            equipamiento={'qué equipazo'}
        ),
        MockAula(
            nombre='y otra',
            capacidad=50,
            horario_lunes=RangoHorario(time(13), time(20)),
            horario_miércoles=RangoHorario(time(14), time(19)),
            horario_viernes=RangoHorario(time(15), time(18)),
            horario_domingo=RangoHorario(time(16), time(17))
        )
    )
))
def test_preprocesar_aulas_un_solo_edificio(edificios: Edificios):
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            nombre='una',
            edificio=edificios[0],
            capacidad=25,
            equipamiento={'qué equipazo'},
            horarios=HorariosSemanales((
                RangoHorario(time(13), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(17)),
                RangoHorario(time(0), time(0))
            ))
        ),
        AulaPreprocesada(
            nombre='y otra',
            edificio=edificios[0],
            capacidad=50,
            equipamiento=set(),
            horarios=HorariosSemanales((
                RangoHorario(time(13), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(14), time(19)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(15), time(18)),
                RangoHorario(time(8), time(17)),
                RangoHorario(time(16), time(17))
            ))
        )
    ]
    aulas_preprocesadas = AulasPreprocesadas(edificios)
    assert aulas_preprocesadas.aulas == aulas_preprocesadas_esperadas
    assert aulas_preprocesadas.rangos_de_aulas == {'nombre': slice(0,2)}
    assert aulas_preprocesadas.preferir_no_usar == []
    assert aulas_preprocesadas.aulas_dobles == {}

@pytest.mark.edificios(
    MockEdificio(
        nombre = 'Anasagasti 1',
        horario_lunes =     RangoHorario(time(8), time(20)),
        horario_martes =    RangoHorario(time(8), time(20)),
        horario_miércoles = RangoHorario(time(8), time(20)),
        horario_jueves =    RangoHorario(time(8), time(20)),
        horario_viernes =   RangoHorario(time(8), time(20)),
        horario_sábado =    RangoHorario(time(8), time(17)),
        horario_domingo =   RangoHorario(time(0), time(0)),
        aulas=(
            MockAula(
                nombre='A102',
                capacidad=25,
                horario_lunes=RangoHorario(time(13), time(20)),
                equipamiento={'qué equipazo'}
            ),
        )
    ),
    MockEdificio(
        nombre = 'Anasagasti 2',
        horario_lunes =     RangoHorario(time(8), time(20)),
        horario_martes =    RangoHorario(time(8), time(20)),
        horario_miércoles = RangoHorario(time(8), time(20)),
        horario_jueves =    RangoHorario(time(8), time(20)),
        horario_viernes =   RangoHorario(time(8), time(20)),
        horario_sábado =    RangoHorario(time(8), time(17)),
        horario_domingo =   RangoHorario(time(0), time(0))
        # Ningún aula en Anasagasti 2
    ),
    MockEdificio(
        nombre = 'Anasagasti 3',
        horario_lunes =     RangoHorario(time(15), time(20)),
        horario_martes =    RangoHorario(time(8, 30), time(20)),
        horario_miércoles = RangoHorario(time(8), time(20)),
        horario_jueves =    RangoHorario(time(8), time(20)),
        horario_viernes =   RangoHorario(time(8), time(20)),
        horario_sábado =    RangoHorario(time(8), time(17)),
        horario_domingo =   RangoHorario(time(0), time(0)),
        preferir_no_usar = True,
        aulas=(
            MockAula(
                nombre='C306',
                capacidad=50
            ),
            MockAula(
                nombre='C345',
                capacidad=31
            )
        )
    )
)
def test_preprocesar_aulas_varios_edificios(edificios: Edificios):
    aulas_preprocesadas_esperadas = [
        AulaPreprocesada(
            nombre='A102',
            edificio=edificios[0],
            capacidad=25,
            equipamiento={'qué equipazo'},
            horarios=(
                RangoHorario(time(13), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(17)),
                RangoHorario(time(0), time(0))
            ),
        ),
        AulaPreprocesada(
            nombre='C306',
            edificio=edificios[2],
            capacidad=50,
            equipamiento=set(),
            horarios=(
                RangoHorario(time(15), time(20)),
                RangoHorario(time(8, 30), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(17)),
                RangoHorario(time(0), time(0))
            )
        ),
        AulaPreprocesada(
            nombre='C345',
            edificio=edificios[2],
            capacidad=31,
            equipamiento=set(),
            horarios=(
                RangoHorario(time(15), time(20)),
                RangoHorario(time(8, 30), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(20)),
                RangoHorario(time(8), time(17)),
                RangoHorario(time(0), time(0))
            )
        )
    ]

    aulas_preprocesadas = AulasPreprocesadas(edificios)
    assert aulas_preprocesadas.aulas == aulas_preprocesadas_esperadas
    assert aulas_preprocesadas.rangos_de_aulas == {'Anasagasti 1': slice(0,1), 'Anasagasti 2': slice(1,1), 'Anasagasti 3': slice(1,3)}
    assert aulas_preprocesadas.preferir_no_usar == [1, 2]
    assert aulas_preprocesadas.aulas_dobles == {}

@pytest.mark.edificios(
    MockEdificio(
        nombre = 'Anasagasti 1',
        horario_lunes =     RangoHorario(time(8), time(20)),
        horario_martes =    RangoHorario(time(8), time(20)),
        horario_miércoles = RangoHorario(time(8), time(20)),
        horario_jueves =    RangoHorario(time(8), time(20)),
        horario_viernes =   RangoHorario(time(8), time(20)),
        horario_sábado =    RangoHorario(time(8), time(17)),
        horario_domingo =   RangoHorario(time(0), time(0)),
        aulas = (
            MockAula(nombre='A102'),
            MockAula(nombre='A102A'),
            MockAula(nombre='A102B'),
            MockAula(nombre='A103')
        ),
        aulas_dobles = {0: (1, 2)}
    ),
    MockEdificio(
        nombre = 'Anasagasti 2',
        horario_lunes =     RangoHorario(time(8), time(20)),
        horario_martes =    RangoHorario(time(8), time(20)),
        horario_miércoles = RangoHorario(time(8), time(20)),
        horario_jueves =    RangoHorario(time(8), time(20)),
        horario_viernes =   RangoHorario(time(8), time(20)),
        horario_sábado =    RangoHorario(time(8), time(17)),
        horario_domingo =   RangoHorario(time(0), time(0)),
        aulas = (
            MockAula(nombre='B102'),
            MockAula(nombre='B102A'),
            MockAula(nombre='B102B'),
            MockAula(nombre='B103'),
            MockAula(nombre='B202'),
            MockAula(nombre='B202A'),
            MockAula(nombre='B202B'),
            MockAula(nombre='B202C'),
            MockAula(nombre='B202D')
        ),
        aulas_dobles = {0: (1, 2), 4: (5, 8)}
    ),
    MockEdificio(
        nombre = 'Anasagasti 3',
        horario_lunes =     RangoHorario(time(15), time(20)),
        horario_martes =    RangoHorario(time(8, 30), time(20)),
        horario_miércoles = RangoHorario(time(8), time(20)),
        horario_jueves =    RangoHorario(time(8), time(20)),
        horario_viernes =   RangoHorario(time(8), time(20)),
        horario_sábado =    RangoHorario(time(8), time(17)),
        horario_domingo =   RangoHorario(time(0), time(0)),
        preferir_no_usar = True,
        aulas = (
            MockAula(nombre='B202'), # No son aulas dobles, pero tienen los mismos nombres que en el otro edificio
            MockAula(nombre='B202A'),
            MockAula(nombre='B202B')
        )
    )
)
def test_aulas_dobles_en_varios_edificios(edificios: Edificios):
    aulas_dobles_esperadas = {0: (1, 2), 4: (5, 6), 8: (9, 12)}
    aulas_preprocesadas = AulasPreprocesadas(edificios)
    assert aulas_preprocesadas.aulas_dobles == aulas_dobles_esperadas

@pytest.mark.edificios(
    MockEdificio(
        nombre='abc',
        aulas=(MockAula(nombre='1'),)
    ),
    MockEdificio(
        nombre='def',
        aulas=(MockAula(nombre='33'),)
    ),
    MockEdificio(
        nombre='ghi'
    )
)
@pytest.mark.clases(
    MockClase(día=Día.Lunes, horario=RangoHorario(time(10), time(15)), no_cambiar_asignación=True, aula_asignada=(0, 0)),
    MockClase(día=Día.Lunes, horario=RangoHorario(time(1), time(10))),
    MockClase(día=Día.Lunes, horario=RangoHorario(time(20), time(23)), no_cambiar_asignación=True, aula_asignada=(1, 0)),
    MockClase(día=Día.Lunes, horario=RangoHorario(time(2), time(10))),
    MockClase(día=Día.Lunes, horario=RangoHorario(time(3), time(10)))
)
def test_separar_asignaciones_manuales(carreras: Carreras, aulas_preprocesadas: AulasPreprocesadas):
    clases_preprocesadas = preprocesar_clases(carreras, aulas_preprocesadas)
    clases_lunes = clases_preprocesadas[Día.Lunes]
    assert len(clases_lunes.clases) == 3
    assert clases_lunes.clases[0].horario == RangoHorario(time(1), time(10))
    assert clases_lunes.clases[1].horario == RangoHorario(time(2), time(10))
    assert clases_lunes.clases[2].horario == RangoHorario(time(3), time(10))
    assert clases_lunes.aulas_ocupadas == [
        (0, RangoHorario(time(10), time(15))),
        (1, RangoHorario(time(20), time(23)))
    ]

@pytest.mark.carreras(MockCarrera(
    materias=(
        MockMateria(
            clases=(MockClase(día=Día.Martes),)
        ),
        MockMateria(
            clases=(
                MockClase(día=Día.Jueves),
                MockClase(día=Día.Martes),
                MockClase(día=Día.Sábado),
            )
        ),
        MockMateria(clases=(MockClase(día=Día.Martes),)),
        MockMateria(clases=(MockClase(día=Día.Lunes),)),
    )
))
def test_separar_clases_por_día(carreras: Carreras, aulas_preprocesadas: AulasPreprocesadas):
    clases_preprocesadas = preprocesar_clases(carreras, aulas_preprocesadas)
    
    # Lunes
    assert len(clases_preprocesadas[Día.Lunes].clases) == 1
    assert clases_preprocesadas[Día.Lunes].clases[0].materia.nombre == 'materia 3'
    assert clases_preprocesadas[Día.Lunes].aulas_ocupadas == []

    # Martes
    assert len(clases_preprocesadas[Día.Martes].clases) == 3
    assert clases_preprocesadas[Día.Martes].clases[0].materia.nombre == 'materia 0'
    assert clases_preprocesadas[Día.Martes].clases[1].materia.nombre == 'materia 1'
    assert clases_preprocesadas[Día.Martes].clases[2].materia.nombre == 'materia 2'
    assert clases_preprocesadas[Día.Martes].aulas_ocupadas == []

    # Jueves
    assert len(clases_preprocesadas[Día.Jueves].clases) == 1
    assert clases_preprocesadas[Día.Jueves].clases[0].materia.nombre == 'materia 1'
    assert clases_preprocesadas[Día.Jueves].aulas_ocupadas == []

    # Sábado
    assert len(clases_preprocesadas[Día.Sábado].clases) == 1
    assert clases_preprocesadas[Día.Sábado].clases[0].materia.nombre == 'materia 1'
    assert clases_preprocesadas[Día.Sábado].aulas_ocupadas == []

    # Los otros días
    sin_clases = ClasesPreprocesadas()
    assert clases_preprocesadas[Día.Miércoles] == sin_clases
    assert clases_preprocesadas[Día.Viernes] == sin_clases
    assert clases_preprocesadas[Día.Domingo] == sin_clases

@pytest.mark.edificios(
    MockEdificio(
        nombre='no preferido',
        aulas=(MockAula(),)*3
    ),
    MockEdificio(
        nombre='preferido',
        aulas=(MockAula(),)*2
    )
)
@pytest.mark.carreras(
    MockCarrera(
        materias=(
            MockMateria(
                clases=(
                    MockClase(día=Día.Lunes),
                    MockClase(día=Día.Jueves)
                )
            ),
        )
    ),
    MockCarrera(
        edificio_preferido=1,
        materias=(
            MockMateria(
                clases=(
                    MockClase(día=Día.Jueves),
                )
            )
        ,)
    )
)
def test_preprocesar_clases_con_edificio_preferido(carreras: Carreras, aulas_preprocesadas: AulasPreprocesadas):
    clases_preprocesadas = preprocesar_clases(carreras, aulas_preprocesadas)
    assert clases_preprocesadas[Día.Lunes].rangos_de_aulas_preferidas == []
    assert clases_preprocesadas[Día.Jueves].rangos_de_aulas_preferidas == [(slice(1, 2), slice(3, 5))]
