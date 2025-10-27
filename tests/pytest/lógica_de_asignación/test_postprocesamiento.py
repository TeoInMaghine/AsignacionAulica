import pytest

from asignacion_aulica.gestor_de_datos.entidades import Carreras, Edificios, todas_las_clases
from asignacion_aulica.lógica_de_asignación.postprocesamiento import InfoPostAsignación

from mocks import MockAula, MockCarrera, MockClase, MockEdificio, MockMateria

@pytest.mark.aulas(
    MockAula(capacidad = 30),
    MockAula(capacidad = 100),
    MockAula(capacidad = 10) # Esta queda justito para la clase 0
)
@pytest.mark.clases(
    MockClase(cantidad_de_alumnos = 10, aula_asignada=(0, 2)),
    MockClase(cantidad_de_alumnos = 25, aula_asignada=(0, 0)),
    MockClase(cantidad_de_alumnos = 80, aula_asignada=(0, 1))
)
def test_ningún_aula_chica(carreras: Carreras, edificios: Edificios):
    info = InfoPostAsignación(edificios, carreras)
    assert len(info.clases_con_aula_chica) == 0
    assert info.todo_ok()

@pytest.mark.aulas(
    MockAula(capacidad = 30),
    MockAula(capacidad = 10) # Esta queda justito para la clase 0
)
@pytest.mark.clases(
    MockClase(cantidad_de_alumnos = 10, aula_asignada=(0, 1)),
    MockClase(cantidad_de_alumnos = 25, aula_asignada=(0, 0)),
    MockClase(cantidad_de_alumnos = 80, aula_asignada=(0, 0))
)
def test_algún_aula_chica(carreras: Carreras, edificios: Edificios):
    info = InfoPostAsignación(edificios, carreras)
    assert len(info.clases_con_aula_chica) == 1
    assert info.clases_con_aula_chica[0] == carreras[0].materias[0].clases[2]

    assert len(info.clases_fuera_de_su_edificio_preferido) == 0
    assert len(info.días_sin_asignar) == 0
    assert not info.todo_ok()

@pytest.mark.aulas(
    MockAula(capacidad = 24),
    MockAula(capacidad = 10)
)
@pytest.mark.clases(
    MockClase(cantidad_de_alumnos = 50, aula_asignada=(0, 0)),
    MockClase(cantidad_de_alumnos = 25, aula_asignada=(0, 0)),
    MockClase(cantidad_de_alumnos = 80, aula_asignada=(0, 1))
)
def test_todas_las_clases_excedidas(carreras: Carreras, edificios: Edificios):
    info = InfoPostAsignación(edificios, carreras)
    assert len(info.clases_con_aula_chica) == 3
    assert all( clase in info.clases_con_aula_chica for clase in carreras[0].materias[0].clases)

    assert len(info.clases_fuera_de_su_edificio_preferido) == 0
    assert len(info.días_sin_asignar) == 0
    assert not info.todo_ok()

@pytest.mark.edificios(
    MockEdificio(aulas=(MockAula(),)*2),
    MockEdificio(aulas=(MockAula(),)*3),
    MockEdificio(aulas=(MockAula(),)*2)
)
@pytest.mark.carreras(
    MockCarrera(
        edificio_preferido=0,
        materias=(
            MockMateria(
                clases=(
                    MockClase(aula_asignada=(1, 0)),
                    MockClase(aula_asignada=(2, 1)),
                )
            ),
        )
    ),
    MockCarrera(
        edificio_preferido=1,
        materias=(
            MockMateria(
                clases=(MockClase(aula_asignada=(2, 0)),)
            ),
        )
    ),
    MockCarrera(
        edificio_preferido=2,
        materias=(
            MockMateria(
                clases=(MockClase(aula_asignada=(0, 1)),)
            ),
        )
    )
)
def test_todas_fuera_del_edificio_preferido(carreras: Carreras, edificios: Edificios):
    info = InfoPostAsignación(edificios, carreras)
    assert len(info.clases_fuera_de_su_edificio_preferido) == 4
    assert all( clase in info.clases_fuera_de_su_edificio_preferido for clase in todas_las_clases(carreras))

    assert len(info.clases_con_aula_chica) == 0
    assert len(info.días_sin_asignar) == 0
    assert not info.todo_ok()

@pytest.mark.edificios(
    MockEdificio(aulas=(MockAula(),)*2),
    MockEdificio(aulas=(MockAula(),)*3),
    MockEdificio(aulas=(MockAula(),)*2)
)

@pytest.mark.carreras(
    MockCarrera(
        edificio_preferido=0,
        materias=(
            MockMateria(
                clases=(
                    MockClase(aula_asignada=(0, 1)),
                    MockClase(aula_asignada=(2, 1)),
                )
            ),
        )
    ),
    MockCarrera(
        edificio_preferido=1,
        materias=(
            MockMateria(
                clases=(MockClase(aula_asignada=(2, 0)),)
            ),
        )
    ),
    MockCarrera(
        edificio_preferido=2,
        materias=(
            MockMateria(
                clases=(MockClase(aula_asignada=(0, 0)),)
            ),
        )
    )
)
def test_una_sola_en_el_edificio_preferido(carreras: Carreras, edificios: Edificios):
    info = InfoPostAsignación(edificios, carreras)
    assert len(info.clases_fuera_de_su_edificio_preferido) == 3
    assert carreras[0].materias[0].clases[1] in info.clases_fuera_de_su_edificio_preferido
    assert carreras[1].materias[0].clases[0] in info.clases_fuera_de_su_edificio_preferido
    assert carreras[2].materias[0].clases[0] in info.clases_fuera_de_su_edificio_preferido

    assert len(info.clases_con_aula_chica) == 0
    assert len(info.días_sin_asignar) == 0
    assert not info.todo_ok()
