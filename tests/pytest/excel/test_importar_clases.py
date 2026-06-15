from datetime import time, date, datetime
import pytest

from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.entidades import Clase
from asignacion_aulica.validación_de_datos.excepciones import DatoInválidoException, ExcelInválidoException
from asignacion_aulica.excel.importar_clases import leer_encabezado, leer_materias, importar

@pytest.mark.archivo('clases_nominal.xlsx')
def test_preámbulo_nominal(primera_hoja_del_archivo):
    carrera, año, cuatrimestre = leer_encabezado(primera_hoja_del_archivo)
    assert carrera == 'Acá va el nombre de la carrera'
    assert año == 2025
    assert cuatrimestre == 'Primero'

@pytest.mark.archivo('clases_preámbulo_roto.xlsx')
def test_preámbulo_roto(primera_hoja_del_archivo):
    with pytest.raises(ExcelInválidoException) as exc_info:
        leer_encabezado(primera_hoja_del_archivo)
    
    mensaje = str(exc_info.value)
    assert 'El encabezado del archivo fue modificado' in mensaje

@pytest.mark.archivo('clases_carrera_vacía.xlsx')
def test_carrera_vacía(primera_hoja_del_archivo):
    with pytest.raises(DatoInválidoException) as exc_info:
        leer_encabezado(primera_hoja_del_archivo)

    mensaje = str(exc_info.value)
    assert 'El nombre de la carrera en la celda D1 no puede estar vacío' in mensaje

@pytest.mark.archivo('clases_nominal.xlsx')
def test_tabla_nominal(primera_hoja_del_archivo):
    materias = leer_materias(primera_hoja_del_archivo)
    
    assert len(materias) == 2
    assert materias[0].nombre == 'Introducción a cosas'
    assert materias[0].año == 1
    assert materias[0].cuatrimestral_o_anual == 'Cuatrimestral'

    assert len(materias[0].clases) == 1
    assert materias[0].clases[0].día == Día.Lunes
    assert materias[0].clases[0].horario == RangoHorario(time(15, 30), time(18))
    assert materias[0].clases[0].virtual == False
    assert materias[0].clases[0].cantidad_de_alumnos == 100
    assert materias[0].clases[0].edificio == 'Anasagasti 7'
    assert materias[0].clases[0].aula == 'B202'
    assert materias[0].clases[0].comisión == 'COM1B'
    assert materias[0].clases[0].teórica_o_práctica == 'Las dos cosas'
    assert materias[0].clases[0].promocionable == 'Si (8)'
    assert materias[0].clases[0].docente == 'Charly García'
    assert materias[0].clases[0].auxiliar == 'Nadie'

    assert materias[1].nombre == 'Hormigón Armado 3'
    assert materias[1].año == 5
    assert materias[1].cuatrimestral_o_anual == 'Anual'

    assert len(materias[1].clases) == 2
    assert materias[1].clases[0].día == Día.Sábado
    assert materias[1].clases[0].horario == RangoHorario(time(22), time(23, 30))
    assert materias[1].clases[0].virtual == False
    assert materias[1].clases[0].cantidad_de_alumnos == 3
    assert materias[1].clases[0].edificio is None
    assert materias[1].clases[0].aula is None
    assert materias[1].clases[0].comisión == ''
    assert materias[1].clases[0].teórica_o_práctica == ''
    assert materias[1].clases[0].promocionable == ''
    assert materias[1].clases[0].docente == ''
    assert materias[1].clases[0].auxiliar == ''

    assert materias[1].clases[1].día == Día.Miércoles
    assert materias[1].clases[1].horario == RangoHorario(time(7), time(10))
    assert materias[1].clases[1].virtual == True
    assert materias[1].clases[1].cantidad_de_alumnos is None
    assert materias[1].clases[1].edificio is None
    assert materias[1].clases[1].aula is None
    assert materias[1].clases[1].comisión == ''
    assert materias[1].clases[1].teórica_o_práctica == ''
    assert materias[1].clases[1].promocionable == ''
    assert materias[1].clases[1].docente == ''
    assert materias[1].clases[1].auxiliar == ''

@pytest.mark.archivo('clases_carrera_vacía.xlsx')
def test_tabla_vacía(primera_hoja_del_archivo):
    clases = leer_materias(primera_hoja_del_archivo)
    assert len(clases) == 0, 'TODO: Decidir si esto tiene que tirar excepción o no.'

@pytest.mark.parametrize(
    ('celda_con_error', 'valor', 'mensaje_esperado'),
    [
        # Casos de error para la columna Año
        ('A4', 2026, 'no se reconoce como un año del plan de estudios'),
        ('A7', 'esto no es un número xd123', 'debe ser un número'),
        ('A28', 4.0, 'debe ser un número entero'),
        ('A5', None, 'no debe estar vacío'),

        # Casos de error para la columna Materia
        ('B5', None, 'no debe estar vacío'),

        # Casos de error para la columna Día
        ('F5', None, 'no debe estar vacío'),
        ('F5', '', 'no debe estar vacío'),
        ('F4', 'mañana', 'no se reconoce como un día de la semana'),
        ('F4', 55, 'no se reconoce como un día de la semana'),
        ('F4', time(15, 30), 'no se reconoce como un día de la semana'),

        # Casos de error para las columnas Horario de inicio y Horario de fin
        ('G5', None, 'no debe estar vacío'),
        ('G4', 55, 'no se reconoce como un horario'),
        ('G4', '20hs', 'no se reconoce como un horario'),
        ('G4', date(2025,7,25), 'no se reconoce como un horario'),
        ('H4', None, 'no debe estar vacío'),
        ('H5', 16, 'no se reconoce como un horario'),
        ('H5', '8AM', 'no se reconoce como un horario'),
        ('H5', datetime(2025,7,25,10,45), 'no se reconoce como un horario'),
        
        # Casos de error para la columna Cupo
        ('I4', None, 'no debe estar vacío'),
        ('I4', '', 'no debe estar vacío'),
        ('I4', 'abc', 'no se reconoce como un número entero'),
        ('I4', 10.7, 'no se reconoce como un número entero'),
        ('I4', -1, 'positivo')
    ]
)
@pytest.mark.archivo('clases_nominal.xlsx')
def test_valores_inválidos_en_la_tabla(primera_hoja_del_archivo, celda_con_error, valor, mensaje_esperado):
    '''
    Verificar que si hay valores inválidos en la tabla se tira una excepción
    del tipo correcto, y que el mensaje incluye la celda y la razón del error.
    '''
    # Insertar el error
    primera_hoja_del_archivo[celda_con_error].value = valor

    # Intentar leer la tabla
    with pytest.raises(DatoInválidoException) as exc_info:
        leer_materias(primera_hoja_del_archivo)

    # Verificar el error
    mensaje = str(exc_info.value)
    assert celda_con_error in mensaje
    assert mensaje_esperado in mensaje

@pytest.mark.archivo('clases_nominal.xlsx')
def test_columna_faltante(primera_hoja_del_archivo):
    # Borrar una columna cualquiera
    primera_hoja_del_archivo.delete_cols(5)

    with pytest.raises(ExcelInválidoException) as exc_info:
        leer_materias(primera_hoja_del_archivo)
    
    mensaje = str(exc_info.value)
    assert 'Se quitaron columnas de la tabla' in mensaje

@pytest.mark.archivo('clases_nominal.xlsx')
def test_columna_cambiada(primera_hoja_del_archivo):
    # Cambiar el nombre de una columna cualquiera
    primera_hoja_del_archivo['E3'].value = 'hola amiga'

    with pytest.raises(ExcelInválidoException) as exc_info:
        leer_materias(primera_hoja_del_archivo)
    
    mensaje = str(exc_info.value)
    assert 'Se cambió una columna' in mensaje
    assert 'E3' in mensaje

@pytest.mark.archivo('clases_nominal.xlsx')
def test_importar_nominal(archivo):
    data = importar(archivo)
    assert len(data) == 1

    carrera, año, cuatrimestre, clases = data[0]
    assert carrera == 'Acá va el nombre de la carrera'
    assert año == 2025
    assert cuatrimestre == 'Primero'
    assert len(clases) == 3 # El contenido de las clases se verifica en otro caso de prueba.

@pytest.mark.archivo('clases_nominal_dos_hojas.xlsx')
def test_importar_nominal_con_dos_hojas(archivo):
    data = importar(archivo)
    assert len(data) == 2

    carrera, año, cuatrimestre, clases = data[0]
    assert carrera == 'Acá va el nombre de la carrera'
    assert año == 2025
    assert cuatrimestre == 'Primero'
    assert len(clases) == 2
    assert clases[0] == Clase(
        año = 1,
        materia = 'Introducción a cosas',
        cuatrimestral_o_anual = 'Cuatrimestral',
        comisión = 'COM1B',
        teórica_o_práctica = 'Las dos cosas',
        día = Día.Lunes,
        horario_inicio = time(15, 30),
        horario_fin = time(18),
        cantidad_de_alumnos = 100,
        docente = 'Charly García',
        auxiliar = 'Nadie',
        promocionable = 'Si (8)',
        edificio = 'Anasagasti 7',
        aula = '',
        virtual = False
    )
    assert clases[1] == Clase(
        año = 5,
        materia = 'Hormigón Armado 3',
        cuatrimestral_o_anual = 'Anual',
        comisión = '',
        teórica_o_práctica = '',
        día = Día.Sábado,
        horario_inicio = time(22),
        horario_fin = time(23, 30),
        cantidad_de_alumnos = 3,
        docente = '',
        auxiliar = '',
        promocionable = '',
        edificio = '',
        aula = '',
        virtual = False
    )
    assert data[0] == data[1]

@pytest.mark.archivo('clases_error_en_la_segunda_hoja.xlsx')
def test_importar_con_error_en_una_hoja(archivo):
    '''Verificar que se incluye el nombre de la hoja en los mensajes de error.'''
    with pytest.raises(DatoInválidoException) as exc_info:
        importar(archivo)
    
    mensaje = str(exc_info.value)
    assert 'Hoja 2' in mensaje
