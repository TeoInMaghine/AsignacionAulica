from typing import Any
import pytest
from datetime import time

from asignacion_aulica.lógica_de_asignación.asignación import asignar
from asignacion_aulica.lógica_de_asignación.preprocesamiento import AulasPreprocesadas, ClasesPreprocesadas
from asignacion_aulica.lógica_de_asignación.restricciones import no_asignar_aulas_ocupadas
from asignacion_aulica.lógica_de_asignación.excepciones import AsignaciónImposibleException
from asignacion_aulica.gestor_de_datos.día import Día

@pytest.mark.edificios(
    dict(nombre='edificio 0', aulas_dobles={'1': ('0', '2')})
)
@pytest.mark.aulas(
    dict(edificio='edificio 0', nombre='0'),
    dict(edificio='edificio 0', nombre='1'),
    dict(edificio='edificio 0', nombre='2'),
)
@pytest.mark.clases(
    dict(día=Día.Martes, horario_inicio=time(19), horario_fin=time(23)),
    dict(
        día=Día.Martes, horario_inicio=time(20), horario_fin=time(22),
        no_cambiar_asignación=True, edificio='edificio 0', aula='1'
    )
)
def test_asignación_manual_al_aula_doble(
    edificios, aulas, carreras, materias, clases,
    aulas_preprocesadas, clases_preprocesadas
):
    '''
    Verificar que si se asigna manualmente al aula doble, las aulas individuales
    también se bloquean en ese horario.
    '''
    clases_martes: ClasesPreprocesadas = clases_preprocesadas[Día.Martes]

    # Probar que se separaron las asignaciones manuales
    assert len(clases_martes.clases) == 1
    assert clases_martes.índices_originales == [0]
    assert clases_martes.aulas_ocupadas == [(1, time(20), time(22))]

    # Probar no_asignar_aulas_ocupadas
    prohibidas = set(no_asignar_aulas_ocupadas(clases_martes, aulas_preprocesadas))
    assert (0, 1) in prohibidas
    assert (0, 0) in prohibidas
    assert (0, 2) in prohibidas

    # Probar asignar
    with pytest.raises(AsignaciónImposibleException) as exc_info:
        asignar(edificios, aulas, carreras, materias, clases)
    
    assert exc_info.value.días_sin_asignar == (Día.Martes,)
    

@pytest.mark.aulas({}, {})
@pytest.mark.clases(
    dict(día=Día.Lunes, horario_inicio=time(10), horario_fin=time(13)),
    dict(
        día=Día.Lunes, horario_inicio=time(10), horario_fin=time(13),
        no_cambiar_asignación=True, edificio='edificio 0', aula='aula 0'
    )
)
def test_dos_clases_al_mismo_tiempo_con_una_asignación_manual(
    edificios, aulas, carreras, materias, clases,
    aulas_preprocesadas, clases_preprocesadas
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    
    # Probar que se separaron las asignaciones manuales
    assert len(clases_lunes.clases) == 1
    assert clases_lunes.índices_originales == [0]
    assert clases_lunes.aulas_ocupadas == [(0, time(10), time(13))]
    
    # Probar no_asignar_aulas_ocupadas
    prohibidas = set(no_asignar_aulas_ocupadas(clases_lunes, aulas_preprocesadas))
    assert prohibidas == {(0, 0)}

    # Probar asignar
    asignar(edificios, aulas, carreras, materias, clases)
    assert clases[0].aula == 'aula 1'
    assert clases[1].aula == 'aula 0'

@pytest.mark.aulas({}, {}, {})
@pytest.mark.clases(
    dict(
        día=Día.Lunes, horario_inicio=time(10), horario_fin=time(13),
        no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1'
    ),
    dict(día=Día.Lunes,   horario_inicio=time(10), horario_fin=time(13)), # Mismo horario
    dict(día=Día.Domingo, horario_inicio=time(10), horario_fin=time(13)), # Mismo horario pero otro día
    dict(día=Día.Lunes,   horario_inicio=time(11), horario_fin=time(12)), # Superposición completa
    dict(día=Día.Lunes,   horario_inicio=time( 9), horario_fin=time(11)), # Parcialmente antes
    dict(día=Día.Lunes,   horario_inicio=time(12), horario_fin=time(15)), # Parcialmente después
    dict(día=Día.Lunes,   horario_inicio=time(13), horario_fin=time(16)), # Mismo día y se tocan justo
    dict(día=Día.Lunes,   horario_inicio=time(17), horario_fin=time(20)), # Mismo día pero otro horario
)
def test_una_asignación_y_varias_superposiciones(
    edificios, aulas, carreras, materias, clases,
    aulas_preprocesadas, clases_preprocesadas
):
    clases_lunes = clases_preprocesadas[Día.Lunes]
    clases_domingo = clases_preprocesadas[Día.Domingo]
    
    # Probar que se separaron las asignaciones manuales
    assert len(clases_lunes.clases) == 6
    assert clases_lunes.índices_originales == [1, 3, 4, 5, 6, 7]
    assert clases_lunes.aulas_ocupadas == [(1, time(10), time(13))]

    assert len(clases_domingo.clases) == 1
    assert clases_domingo.índices_originales == [2]
    assert clases_domingo.aulas_ocupadas == []
    
    # Probar no_asignar_aulas_ocupadas
    prohibidas = set(no_asignar_aulas_ocupadas(clases_lunes, aulas_preprocesadas))
    assert prohibidas == {(0, 1), (1, 1), (2, 1), (3, 1)}

    # Probar asignar
    asignar(edificios, aulas, carreras, materias, clases)
    assert clases[0].aula == 'aula 1'
    clases_que_se_superponen = [1, 3, 4, 5]
    clases_que_no_se_superponen = [2, 6, 7]
    assert all( clases[i].aula != 'aula 1' for i in clases_que_se_superponen )
    assert all( clases[i].aula is not None for i in clases_que_no_se_superponen ) # Se asignaron, no importa a qué aula

@pytest.mark.aulas(*[{}]*10) # Re críptico pero esto significa 10 aulas con valores default
@pytest.mark.clases(
    dict(día=Día.Martes, horario_inicio=time(10), horario_fin=time(13)),
    dict(día=Día.Martes, horario_inicio=time(10), horario_fin=time(13), no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1'), # Mismo horario
    dict(día=Día.Jueves, horario_inicio=time(10), horario_fin=time(13), no_cambiar_asignación=True, edificio='edificio 0', aula='aula 2'), # Mismo horario pero otro día
    dict(día=Día.Martes, horario_inicio=time(11), horario_fin=time(12), no_cambiar_asignación=True, edificio='edificio 0', aula='aula 3'), # Superposición completa
    dict(día=Día.Martes, horario_inicio=time( 9), horario_fin=time(11), no_cambiar_asignación=True, edificio='edificio 0', aula='aula 4'), # Parcialmente antes
    dict(día=Día.Martes, horario_inicio=time(12), horario_fin=time(15), no_cambiar_asignación=True, edificio='edificio 0', aula='aula 5'), # Parcialmente después
    dict(día=Día.Martes, horario_inicio=time(13), horario_fin=time(16), no_cambiar_asignación=True, edificio='edificio 0', aula='aula 6'), # Mismo día y se tocan justo
    dict(día=Día.Martes, horario_inicio=time(17), horario_fin=time(20), no_cambiar_asignación=True, edificio='edificio 0', aula='aula 7'), # Mismo día pero otro horario
)
def test_varias_asignaciones_y_una_no_asignada(
    edificios, aulas, carreras, materias, clases,
    aulas_preprocesadas, clases_preprocesadas
):
    clases_martes = clases_preprocesadas[Día.Martes]
    clases_jueves = clases_preprocesadas[Día.Jueves]
    
    # Probar que se separaron las asignaciones manuales
    assert len(clases_martes.clases) == 1
    assert clases_martes.índices_originales == [0]
    assert clases_martes.aulas_ocupadas == [
        (1, time(10), time(13)),
        (3, time(11), time(12)),
        (4, time( 9), time(11)),
        (5, time(12), time(15)),
        (6, time(13), time(16)),
        (7, time(17), time(20)),
    ]

    assert len(clases_jueves.clases) == 0
    assert clases_jueves.índices_originales == []
    assert clases_jueves.aulas_ocupadas == [(2, time(10), time(13))]

    # Probar no_asignar_aulas_ocupadas
    prohibidas = set(no_asignar_aulas_ocupadas(clases_martes, aulas_preprocesadas))
    assert prohibidas == {(0, 1), (0, 3), (0, 4), (0, 5)}

    # Probar asignar
    asignar(edificios, aulas, carreras, materias, clases)
    assert clases[0].aula not in (1, 3, 4, 5)
    assert all( clases[i].aula == f'aula {i}' for i in range(1, 8) )

@pytest.mark.aulas(
    dict(),
    dict(horario_viernes=(time(0), time(0))),
    dict(),
    dict(capacidad=20, equipamiento={'pizarrón'}),
)
@pytest.mark.clases(
    dict[str, Any](día=Día.Miércoles), # No se superpone con ninguna de las asignaciones manuales
    dict[str, Any](día=Día.Martes,  no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1', horario_inicio=time(10), horario_fin=time(13)),    # Mismo aula al mismo tiempo
    dict[str, Any](día=Día.Martes,  no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1', horario_inicio=time(11), horario_fin=time(12)),
    dict[str, Any](día=Día.Sábado,  no_cambiar_asignación=True, edificio='edificio 0', aula='aula 0', horario_inicio=time(15), horario_fin=time(19)),    # Aula doble y aula individual al mismo tiempo
    dict[str, Any](día=Día.Sábado,  no_cambiar_asignación=True, edificio='edificio 0', aula='aula 3', horario_inicio=time(18), horario_fin=time(20)),
    dict[str, Any](día=Día.Martes,  no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1', horario_inicio=time(19), horario_fin=time(23)),    # Asignadas a un aula cerrada
    dict[str, Any](día=Día.Viernes, no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1'),
    dict[str, Any](día=Día.Jueves,  no_cambiar_asignación=True, edificio='edificio 0', aula='aula 3', cantidad_de_alumnos=30),                           # Capacidad insuficiente
    dict[str, Any](día=Día.Jueves,  no_cambiar_asignación=True, edificio='edificio 0', aula='aula 3', equipamiento_necesario={'pizarrón', 'proyector'}), # Equipamiento insuficiente
)
def test_asignaciones_manuales_que_inclumplen_restricciones(
    edificios, aulas, carreras, materias, clases
):
    '''
    Verificar que se respetan las asignaciones manuales aunque no cumplan con
    algunas restricciones
    '''
    asignar(edificios, aulas, carreras, materias, clases)
    assert clases[0].aula is not None # Verificar que se asignó algún aula
    assert clases[1].aula == 'aula 1'
    assert clases[2].aula == 'aula 1'
    assert clases[3].aula == 'aula 0'
    assert clases[4].aula == 'aula 3'
    assert clases[5].aula == 'aula 1'
    assert clases[6].aula == 'aula 1'
    assert clases[7].aula == 'aula 3'
    assert clases[8].aula == 'aula 3'

@pytest.mark.aulas(*[{}]*5) # Re críptico pero esto significa 5 aulas con valores default
@pytest.mark.clases(
    dict(no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1'),
    dict(no_cambiar_asignación=True, edificio='edificio 0', aula='aula 3'),
    dict(no_cambiar_asignación=True, edificio='edificio 0', aula='aula 0'),
    dict(no_cambiar_asignación=True, edificio='edificio 0', aula='aula 2'),
    dict(no_cambiar_asignación=True, edificio='edificio 0', aula='aula 4'),
    dict(no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1'),
    dict(no_cambiar_asignación=True, edificio='edificio 0', aula='aula 1'),
)
def test_todas_las_aulas_asignadas_manuales(edificios, aulas, carreras, materias, clases):
    '''
    Verificar que cuando todas las asignaciones son manuales, se maneja
    correctamente (no saltan excepciones ni se cambian las asignaciones).
    '''
    asignar(edificios, aulas, carreras, materias, clases)

    assert clases[0].aula == 'aula 1'
    assert clases[1].aula == 'aula 3'
    assert clases[2].aula == 'aula 0'
    assert clases[3].aula == 'aula 2'
    assert clases[4].aula == 'aula 4'
    assert clases[5].aula == 'aula 1'
    assert clases[6].aula == 'aula 1'

