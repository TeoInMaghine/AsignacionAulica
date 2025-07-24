from datetime import time
import openpyxl
import pytest

from asignacion_aulica.validación_de_datos.excepciones import DatoInválidoException, ExcelInválidoException
from asignacion_aulica.archivos_excel.clases.importar import leer_preámbulo, leer_tabla
from asignacion_aulica.archivos_excel.clases.clase import Clase
from asignacion_aulica.lógica_de_asignación.día import Día

@pytest.mark.archivo('clases_nominal.xlsx')
def test_preámbulo_nominal(primera_hoja_del_archivo):
    carrera, año, cuatrimestre = leer_preámbulo(primera_hoja_del_archivo)
    assert carrera == 'Acá va el nombre de la carrera'
    assert año == 2025
    assert cuatrimestre == 'Primero'

@pytest.mark.archivo('clases_preámbulo_roto.xlsx')
def test_preámbulo_roto(primera_hoja_del_archivo):
    with pytest.raises(ExcelInválidoException) as exc_info:
        leer_preámbulo(primera_hoja_del_archivo)
    
    mensaje = str(exc_info.value)
    assert 'El encabezado del archivo fue modificado' in mensaje

@pytest.mark.archivo('clases_carrera_vacía.xlsx')
def test_carrera_vacía(primera_hoja_del_archivo):
    with pytest.raises(DatoInválidoException) as exc_info:
        leer_preámbulo(primera_hoja_del_archivo)

    mensaje = str(exc_info.value)
    assert 'El nombre de la carrera en la celda D1 no puede estar vacío' in mensaje

@pytest.mark.archivo('clases_nominal.xlsx')
def test_tabla_nominal(primera_hoja_del_archivo):
    clases = leer_tabla(primera_hoja_del_archivo)
    
    assert len(clases) == 2
    assert clases[0] == Clase(
        año = 1,
        materia = 'Introducción a cosas',
        cuatrimestral_o_anual = 'Cuatrimestral',
        comisión = 'COM1B',
        teórica_o_práctica = 'Las dos cosas',
        día = Día.LUNES,
        horario_inicio = time(15, 30),
        horario_fin = time(18),
        cantidad_de_alumnos = 100,
        docente = 'Charly García',
        auxiliar = 'Nadie',
        promocionable = 'Si (8)',
        edificio = 'Anasagasti 7',
        aula = ''
    )
    assert clases[1] == Clase(
        año = 5,
        materia = 'Hormigón Armado 3',
        cuatrimestral_o_anual = 'Anual',
        comisión = '',
        teórica_o_práctica = '',
        día = Día.SÁBADO,
        horario_inicio = time(22),
        horario_fin = time(23, 30),
        cantidad_de_alumnos = 3,
        docente = '',
        auxiliar = '',
        promocionable = '',
        edificio = '',
        aula = ''
    )
