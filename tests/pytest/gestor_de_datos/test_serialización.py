import logging
from pathlib import Path
import time, datetime
import pytest
import random
from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

@pytest.fixture
def tmp_filename(tmp_path: Path) -> Path:
    '''
    :return: A filename inside a temporary directory created for each  test.
    '''
    return tmp_path / "tmp_file"

def test_roundtrip_vacío(tmp_filename: Path):
    gestor = GestorDeDatos(tmp_filename)
    gestor.guardar()

    gestor2 = GestorDeDatos(tmp_filename)
    gestor2.cargar()
    assert gestor2.cantidad_de_edificios() == 0
    assert gestor2.cantidad_de_carreras() == 0
    assert gestor2.get_equipamientos_existentes() == []

def test_roundtrip_con_aulas(tmp_filename: Path):
    gestor = GestorDeDatos(tmp_filename)
    gestor.cargar()

    gestor.agregar_edificio()
    edificio = gestor.get_edificio(0)
    edificio.preferir_no_usar = True
    edificio.nombre = 'E0'
    edificio.horarios[Día.Martes].fin = datetime.time(1,2)

    gestor.agregar_aula(0)
    gestor.agregar_aula(0)
    aula = gestor.get_aula(0, 1)
    aula.nombre = 'A01'
    
    gestor.agregar_edificio()

    gestor.guardar()

    gestor2 = GestorDeDatos(tmp_filename)
    gestor2.cargar()
    assert gestor2.cantidad_de_edificios() == 2
    edificio2 = gestor2.get_edificio(0)
    assert edificio2.preferir_no_usar is True
    assert edificio2.nombre == 'E0'
    assert edificio2.horarios[Día.Martes].fin == datetime.time(1,2)

    assert gestor2.cantidad_de_aulas(0) == 2
    aula2 = gestor2.get_aula(0, 1)
    assert aula2.nombre == 'A01'
    assert aula2.edificio is edificio2

def test_roundtrip_con_clases(tmp_filename: Path):
    gestor = GestorDeDatos(tmp_filename)
    gestor.cargar()

    gestor.agregar_carrera('C0')
    gestor.agregar_carrera('C1')

    gestor.agregar_materia(1)
    materia = gestor.get_materia(1, 0)
    materia.nombre = 'M 1 0'
    materia.año = 15
    materia.cuatrimestral_o_anual = 'un string'

    gestor.agregar_clase(1, 0)
    clase = gestor.get_clase(1, 0, 0)
    clase.día = Día.Domingo
    clase.cantidad_de_alumnos = 666
    gestor.agregar_equipamiento_a_clase(1, 0, 0, 'A')

    gestor.guardar()

    gestor2 = GestorDeDatos(tmp_filename)
    gestor2.cargar()
    assert gestor2.cantidad_de_carreras() == 2
    assert gestor2.get_carrera(0).nombre == 'C0'
    assert gestor2.get_carrera(1).nombre == 'C1'

    assert gestor2.cantidad_de_carreras() == 2
    materia2 = gestor2.get_materia(1, 0)
    assert materia2.carrera is gestor2.get_carrera(1)
    assert materia2.nombre == 'M 1 0'
    assert materia2.año == 15
    assert materia2.cuatrimestral_o_anual == 'un string'

    assert gestor2.cantidad_de_clases(1, 0) == 1
    clase2 = gestor2.get_clase(1, 0, 0)
    assert clase2.materia is materia2
    assert clase2.día == Día.Domingo
    assert clase2.cantidad_de_alumnos == 666
    assert clase2.equipamiento_necesario == {'A'}
    assert gestor2.get_equipamientos_existentes() == ['A']

@pytest.mark.stress_test
def test_stress_guardar_validar_leer(tmp_filename: Path):
    '''
    Medir el tiempo que se tarda en validar, escribir, y leer un volumen de
    datos realista.
    '''
    # Popular un gestor con una cantidad realista de datos
    gestor = GestorDeDatos(tmp_filename)
    gestor.cargar()
    _popular_gestor_con_datos_más_o_menos_realistas(gestor)

    # Medir el tiempo que tarda en validar
    t_start = time.monotonic()
    gestor.validar_datos()
    t_end = time.monotonic()
    t_delta = datetime.timedelta(seconds=t_end-t_start)
    logging.info('Validación de datos demoró %s', t_delta)

    # Medir el tiempo que tarda en guardar
    t_start = time.monotonic()
    gestor.guardar()
    t_end = time.monotonic()
    t_delta = datetime.timedelta(seconds=t_end-t_start)
    logging.info('Guardar los datos demoró %s', t_delta)

    # Medir el tiempo que tarda en leer
    t_start = time.monotonic()
    _gestor2 = GestorDeDatos(tmp_filename)
    _gestor2.cargar()
    t_end = time.monotonic()
    t_delta = datetime.timedelta(seconds=t_end-t_start)
    logging.info('Leer los datos demoró %s', t_delta)

def _popular_gestor_con_datos_más_o_menos_realistas(gestor: GestorDeDatos):
    '''
    Agregar a un gestor de datos (inicialmente vacío) un volumen realista de
    datos de edificios y carreras.

    Los datos generados son pseudoaleatorios, pero se usa una semilla fija para
    que sean reproducibles.
    '''
    n_edificios = 5
    n_carreras = 30
    n_materias_por_carrera = 5 * 4 * 2 # 5 años * 4 materias/cuatri * 2 cuatris/año
    equipamientos_posibles = [str(i) for i in range(6)]

    rand = random.Random()
    rand.seed(1)

    for i_edificio in range(n_edificios):
        gestor.agregar_edificio()
        
        n_aulas = rand.randint(20, 100)
        for i_aula in range(n_aulas):
            gestor.agregar_aula(i_edificio)

            n_equipamientos = rand.randint(0, 3)
            equipamientos = rand.sample(equipamientos_posibles, n_equipamientos)
            for equipamiento in equipamientos:
                gestor.agregar_equipamiento_a_aula(i_edificio, i_aula, equipamiento)
            
            n_horarios_no_default = rand.randint(0, 2)
            for i in range(n_horarios_no_default):
                día = rand.choice(list(Día))
                gestor.get_aula(i_edificio, i_aula).horarios[día] = RangoHorario(datetime.time(i), datetime.time(i+1, 30))
        
        n_aulas_dobles = rand.randint(0, 3)
        aulas_dobles = rand.sample(gestor.get_edificio(i_edificio).aulas, n_aulas_dobles*3)
        for i_aula_doble in range(n_aulas_dobles):
            gestor.agregar_aula_doble(i_edificio)
            aula_doble = gestor.get_aula_doble(i_edificio, i_aula_doble)
            aula_doble.aula_grande = aulas_dobles.pop()
            aula_doble.aula_chica_1 = aulas_dobles.pop()
            aula_doble.aula_chica_2 = aulas_dobles.pop()
    
    for i in range(n_carreras):
        i_carrera = gestor.agregar_carrera(f'Carrera {i}')
        carrera = gestor.get_carrera(i_carrera)

        tiene_edificio_preferido = rand.random() < 0.3 # 3% de las carreras tienen edificio preferido
        if tiene_edificio_preferido:
            i_edificio_preferido = rand.randint(0, gestor.cantidad_de_edificios()-1)
            carrera.edificio_preferido = gestor.get_edificio(i_edificio_preferido)

        for i_materia in range(n_materias_por_carrera):
            gestor.agregar_materia(i_carrera)

            n_clases = rand.randint(1, 20) # desde 1 clase por semana hasta 10 comisiones de 2 clases por semana
            for i_clase in range(n_clases):
                gestor.agregar_clase(i_carrera, i_materia)
                clase = gestor.get_clase(i_carrera, i_materia, i_clase)

                n_equipamientos = rand.randint(0, 2)
                equipamientos = rand.sample(equipamientos_posibles, n_equipamientos)
                for equipamiento in equipamientos:
                    gestor.agregar_equipamiento_a_clase(i_carrera, i_materia, i_clase, equipamiento)
                
                # Asignar aulas de una manera claramente no válida
                # (pero poner no_cambiar_asignación=True para que sea técnicamente válido)
                i_edificio = rand.randint(0, gestor.cantidad_de_edificios()-1)
                i_aula = rand.randint(0, gestor.cantidad_de_aulas(i_edificio)-1)
                clase.aula_asignada = gestor.get_aula(i_edificio, i_aula)
                clase.no_cambiar_asignación = True

