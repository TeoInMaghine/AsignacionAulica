from datetime import time
import pytest

from asignacion_aulica.lógica_de_asignación.preprocesamiento import AulasPreprocesadas, ClasesPreprocesadas, ClasesPreprocesadasPorDía
from asignacion_aulica.lógica_de_asignación.restricciones import no_asignar_aulas_ocupadas
from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.entidades import Carreras, Edificios
from asignacion_aulica.lógica_de_asignación.asignación import asignar

from mocks import MockAula, MockClase, MockEdificio

@pytest.mark.edificios(MockEdificio(
        aulas=(
            MockAula(nombre='0'),
            MockAula(nombre='1'),
            MockAula(nombre='2'),
        ),
        aulas_dobles={1: (0, 2)}
))
@pytest.mark.clases(
    MockClase(
        día=Día.Martes, horario=RangoHorario(time(19), time(23))
    ),
    MockClase(
        día=Día.Martes, horario=RangoHorario(time(20), time(22)),
        no_cambiar_asignación=True, aula_asignada=(0, 1)
    )
)
def test_asignación_manual_al_aula_doble(
    edificios: Edificios,
    carreras: Carreras,
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía
):
    '''
    Verificar que si se asigna manualmente al aula doble, las aulas individuales
    también se bloquean en ese horario.
    '''
    clases_martes: ClasesPreprocesadas = clases_preprocesadas[Día.Martes]

    # Probar que se separaron las asignaciones manuales
    assert len(clases_martes.clases) == 1
    assert clases_martes.aulas_ocupadas == [(1, RangoHorario(time(20), time(22)))]

    # Probar no_asignar_aulas_ocupadas
    prohibidas = set(no_asignar_aulas_ocupadas(clases_martes, aulas_preprocesadas))
    assert (0, 1) in prohibidas
    assert (0, 0) in prohibidas
    assert (0, 2) in prohibidas

    # Probar asignar
    result = asignar(edificios, carreras)
    
    assert not result.todo_ok()
    assert result.días_sin_asignar == [Día.Martes,]
    

@pytest.mark.aulas(MockAula(), MockAula())
@pytest.mark.clases(
    MockClase(
        día=Día.Lunes, horario=RangoHorario(time(10), time(13))
    ),
    MockClase(
        día=Día.Lunes, horario=RangoHorario(time(10), time(13)),
        no_cambiar_asignación=True, aula_asignada=(0, 0)
    )
)
def test_dos_clases_al_mismo_tiempo_con_una_asignación_manual(
    edificios: Edificios,
    carreras: Carreras,
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    
    # Probar que se separaron las asignaciones manuales
    assert len(clases_lunes.clases) == 1
    assert clases_lunes.aulas_ocupadas == [(0, RangoHorario(time(10), time(13)))]
    
    # Probar no_asignar_aulas_ocupadas
    prohibidas = list(no_asignar_aulas_ocupadas(clases_lunes, aulas_preprocesadas))
    assert prohibidas == [(0, 0)]

    # Probar asignar
    result = asignar(edificios, carreras)
    assert result.todo_ok()

    assert carreras[0].materias[0].clases[0].aula_asignada == edificios[0].aulas[1]
    assert carreras[0].materias[0].clases[1].aula_asignada == edificios[0].aulas[0]

@pytest.mark.aulas(MockAula(), MockAula(), MockAula())
@pytest.mark.clases(
    MockClase(
        día=Día.Lunes, horario=RangoHorario(time(10), time(13)),
        no_cambiar_asignación=True, aula_asignada=(0, 1)
    ),
    MockClase(día=Día.Lunes,   horario=RangoHorario(time(10), time(13))), # Mismo horario
    MockClase(día=Día.Domingo, horario=RangoHorario(time(10), time(13))), # Mismo horario pero otro día
    MockClase(día=Día.Lunes,   horario=RangoHorario(time(11), time(12))), # Superposición completa
    MockClase(día=Día.Lunes,   horario=RangoHorario(time( 9), time(11))), # Parcialmente antes
    MockClase(día=Día.Lunes,   horario=RangoHorario(time(12), time(15))), # Parcialmente después
    MockClase(día=Día.Lunes,   horario=RangoHorario(time(13), time(16))), # Mismo día y se tocan justo
    MockClase(día=Día.Lunes,   horario=RangoHorario(time(17), time(20))), # Mismo día pero otro horario
)
def test_una_asignación_y_varias_superposiciones(
    edificios: Edificios,
    carreras: Carreras,
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    clases_domingo = clases_preprocesadas[Día.Domingo]
    
    # Probar que se separaron las asignaciones manuales
    assert len(clases_lunes.clases) == 6
    assert clases_lunes.aulas_ocupadas == [(1, RangoHorario(time(10), time(13)))]

    assert len(clases_domingo.clases) == 1
    assert clases_domingo.aulas_ocupadas == []
    
    # Probar no_asignar_aulas_ocupadas
    prohibidas = list(no_asignar_aulas_ocupadas(clases_lunes, aulas_preprocesadas))
    assert prohibidas == [(0, 1), (1, 1), (2, 1), (3, 1)]

    # Probar asignar
    result = asignar(edificios, carreras)
    assert result.todo_ok()

    assert carreras[0].materias[0].clases[0].aula_asignada == edificios[0].aulas[1]
    clases_que_se_superponen = [1, 3, 4, 5]
    clases_que_no_se_superponen = [2, 6, 7]
    assert all( carreras[0].materias[0].clases[i].aula_asignada != edificios[0].aulas[1] for i in clases_que_se_superponen )
    assert all( carreras[0].materias[0].clases[i].aula_asignada is not None for i in clases_que_no_se_superponen ) # Se asignaron, no importa a qué aula

@pytest.mark.aulas(*[MockAula()]*10) # Re críptico pero esto significa 10 aulas con valores default
@pytest.mark.clases(
    MockClase(día=Día.Martes, horario=RangoHorario(time(10), time(13))),
    MockClase(día=Día.Martes, horario=RangoHorario(time(10), time(13)), no_cambiar_asignación=True, aula_asignada=(0, 1)), # Mismo horario
    MockClase(día=Día.Jueves, horario=RangoHorario(time(10), time(13)), no_cambiar_asignación=True, aula_asignada=(0, 2)), # Mismo horario pero otro día
    MockClase(día=Día.Martes, horario=RangoHorario(time(11), time(12)), no_cambiar_asignación=True, aula_asignada=(0, 3)), # Superposición completa
    MockClase(día=Día.Martes, horario=RangoHorario(time( 9), time(11)), no_cambiar_asignación=True, aula_asignada=(0, 4)), # Parcialmente antes
    MockClase(día=Día.Martes, horario=RangoHorario(time(12), time(15)), no_cambiar_asignación=True, aula_asignada=(0, 5)), # Parcialmente después
    MockClase(día=Día.Martes, horario=RangoHorario(time(13), time(16)), no_cambiar_asignación=True, aula_asignada=(0, 6)), # Mismo día y se tocan justo
    MockClase(día=Día.Martes, horario=RangoHorario(time(17), time(20)), no_cambiar_asignación=True, aula_asignada=(0, 7)), # Mismo día pero otro horario
)
def test_varias_asignaciones_y_una_no_asignada(
    edificios: Edificios,
    carreras: Carreras,
    aulas_preprocesadas: AulasPreprocesadas,
    clases_preprocesadas: ClasesPreprocesadasPorDía
):
    clases_martes = clases_preprocesadas[Día.Martes]
    clases_jueves = clases_preprocesadas[Día.Jueves]
    
    # Probar que se separaron las asignaciones manuales
    assert len(clases_martes.clases) == 1
    assert clases_martes.aulas_ocupadas == [
        (1, RangoHorario(time(10), time(13))),
        (3, RangoHorario(time(11), time(12))),
        (4, RangoHorario(time( 9), time(11))),
        (5, RangoHorario(time(12), time(15))),
        (6, RangoHorario(time(13), time(16))),
        (7, RangoHorario(time(17), time(20)))
    ]

    assert len(clases_jueves.clases) == 0
    assert clases_jueves.aulas_ocupadas == [(2, RangoHorario(time(10), time(13)))]

    # Probar no_asignar_aulas_ocupadas
    prohibidas = list(no_asignar_aulas_ocupadas(clases_martes, aulas_preprocesadas))
    assert prohibidas == [(0, 1), (0, 3), (0, 4), (0, 5)]

    # Probar asignar
    result = asignar(edificios, carreras)
    assert result.todo_ok()

    assert carreras[0].materias[0].clases[0].aula_asignada is not None
    assert carreras[0].materias[0].clases[0].aula_asignada.nombre not in ('aula 1', 'aula 3', 'aula 4', 'aula 5')
    assert all( carreras[0].materias[0].clases[i].aula_asignada == edificios[0].aulas[i] for i in range(1, 8) )

@pytest.mark.aulas(
    MockAula(),
    MockAula(horario_viernes=RangoHorario(time(0), time(0))),
    MockAula(),
    MockAula(capacidad=20, equipamiento={'pizarrón'}),
)
@pytest.mark.clases(
    MockClase(día=Día.Miércoles), # No se superpone con ninguna de las asignaciones manuales
    MockClase(día=Día.Martes,  no_cambiar_asignación=True, aula_asignada=(0, 1), horario=RangoHorario(time(10), time(13))), # Mismo aula al mismo tiempo
    MockClase(día=Día.Martes,  no_cambiar_asignación=True, aula_asignada=(0, 1), horario=RangoHorario(time(11), time(12))),
    MockClase(día=Día.Sábado,  no_cambiar_asignación=True, aula_asignada=(0, 0), horario=RangoHorario(time(15), time(19))), # Aula doble y aula individual al mismo tiempo
    MockClase(día=Día.Sábado,  no_cambiar_asignación=True, aula_asignada=(0, 3), horario=RangoHorario(time(18), time(20))),
    MockClase(día=Día.Martes,  no_cambiar_asignación=True, aula_asignada=(0, 1), horario=RangoHorario(time(19), time(23))), # Asignadas a un aula cerrada
    MockClase(día=Día.Viernes, no_cambiar_asignación=True, aula_asignada=(0, 1)),
    MockClase(día=Día.Jueves,  no_cambiar_asignación=True, aula_asignada=(0, 3), cantidad_de_alumnos=30),                           # Capacidad insuficiente
    MockClase(día=Día.Jueves,  no_cambiar_asignación=True, aula_asignada=(0, 3), equipamiento_necesario={'pizarrón', 'proyector'}), # Equipamiento insuficiente
)
def test_asignaciones_manuales_que_inclumplen_restricciones(edificios: Edificios, carreras: Carreras):
    '''
    Verificar que se respetan las asignaciones manuales aunque no cumplan con
    algunas restricciones
    '''
    result = asignar(edificios, carreras)
    assert result.todo_ok()

    assert carreras[0].materias[0].clases[0].aula_asignada is not None # Verificar que se asignó algún aula
    assert carreras[0].materias[0].clases[1].aula_asignada == edificios[0].aulas[1]
    assert carreras[0].materias[0].clases[2].aula_asignada == edificios[0].aulas[1]
    assert carreras[0].materias[0].clases[3].aula_asignada == edificios[0].aulas[0]
    assert carreras[0].materias[0].clases[4].aula_asignada == edificios[0].aulas[3]
    assert carreras[0].materias[0].clases[5].aula_asignada == edificios[0].aulas[1]
    assert carreras[0].materias[0].clases[6].aula_asignada == edificios[0].aulas[1]
    assert carreras[0].materias[0].clases[7].aula_asignada == edificios[0].aulas[3]
    assert carreras[0].materias[0].clases[8].aula_asignada == edificios[0].aulas[3]

@pytest.mark.aulas(*[MockAula()]*5) # Re críptico pero esto significa 5 aulas con valores default
@pytest.mark.clases(
    MockClase(no_cambiar_asignación=True, aula_asignada=(0, 1)),
    MockClase(no_cambiar_asignación=True, aula_asignada=(0, 3)),
    MockClase(no_cambiar_asignación=True, aula_asignada=(0, 0)),
    MockClase(no_cambiar_asignación=True, aula_asignada=(0, 2)),
    MockClase(no_cambiar_asignación=True, aula_asignada=(0, 4)),
    MockClase(no_cambiar_asignación=True, aula_asignada=(0, 1)),
    MockClase(no_cambiar_asignación=True, aula_asignada=(0, 1)),
)
def test_todas_las_aulas_asignadas_manuales(edificios: Edificios, carreras: Carreras):
    '''
    Verificar que cuando todas las asignaciones son manuales, se maneja
    correctamente (no saltan excepciones ni se cambian las asignaciones).
    '''
    result = asignar(edificios, carreras)
    assert result.todo_ok()

    assert carreras[0].materias[0].clases[0].aula_asignada == edificios[0].aulas[1]
    assert carreras[0].materias[0].clases[1].aula_asignada == edificios[0].aulas[3]
    assert carreras[0].materias[0].clases[2].aula_asignada == edificios[0].aulas[0]
    assert carreras[0].materias[0].clases[3].aula_asignada == edificios[0].aulas[2]
    assert carreras[0].materias[0].clases[4].aula_asignada == edificios[0].aulas[4]
    assert carreras[0].materias[0].clases[5].aula_asignada == edificios[0].aulas[1]
    assert carreras[0].materias[0].clases[6].aula_asignada == edificios[0].aulas[1]

