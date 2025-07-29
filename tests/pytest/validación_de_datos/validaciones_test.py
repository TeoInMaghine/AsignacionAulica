import pytest
from datetime import time

from asignacion_aulica.validación_de_datos.excepciones import DatoInválidoException
from asignacion_aulica.validación_de_datos.validaciones import *
from asignacion_aulica.lógica_de_asignación.día import Día

def test_str_posiblemente_vacío():
    assert str_posiblemente_vacío(' hola ') == 'hola'
    assert str_posiblemente_vacío(None) == ''

def test_validar_str_no_vacío():
    assert validar_str_no_vacío('hola', 'msg') == 'hola'
    assert validar_str_no_vacío(' 123  ', 'msg') == '123'

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_str_no_vacío('', 'msg')
    
    assert str(exc_info.value) == 'msg'
    
    with pytest.raises(DatoInválidoException) as exc_info:
        validar_str_no_vacío('  ', 'msg')
    
    assert str(exc_info.value) == 'msg'
    
    with pytest.raises(DatoInválidoException) as exc_info:
        validar_str_no_vacío(None, 'msg')
    
    assert str(exc_info.value) == 'msg'

def test_str_posiblemente_vacío():
    assert str_posiblemente_vacío('') == ''
    assert str_posiblemente_vacío('hola') == 'hola'
    assert str_posiblemente_vacío('  hola\t') == 'hola'
    assert str_posiblemente_vacío(None) == ''
    assert str_posiblemente_vacío([1,23]) == '[1, 23]'

def test_validar_año():
    assert validar_año(2000, 'un mensaje') == 2000
    assert validar_año(2025, 'un mensaje') == 2025
    assert validar_año('2032', 'un mensaje') == 2032

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_año(2025.0, 'msg') # No es int

    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'debe ser un número entero' in mensaje

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_año(32, 'msg') # Es muy chico
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'a partir del 2000' in mensaje

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_año('123hola5', 'msg') # No es un número

    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'debe ser un número entero' in mensaje
    
    with pytest.raises(DatoInválidoException) as exc_info:
        validar_año(None, 'msg') # Celda vacía

    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'no debe estar vacío' in mensaje

def test_validar_año_del_plan_de_estudios():
    assert validar_año_del_plan_de_estudios(4, 'msg') == 4
    assert validar_año_del_plan_de_estudios('8', 'msg') == 8

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_año_del_plan_de_estudios(10, 'msg')
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'debe estar entre 1 y 9' in mensaje
    
    with pytest.raises(DatoInválidoException) as exc_info:
        validar_año_del_plan_de_estudios('123hola5', 'msg') # No es un número

    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'debe ser un número entero' in mensaje
    
    with pytest.raises(DatoInválidoException) as exc_info:
        validar_año_del_plan_de_estudios(None, 'msg') # Celda vacía

    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'no debe estar vacío' in mensaje

def test_validar_día():
    assert validar_día('lunes', 'msg') == Día.LUNES
    assert validar_día('MarTeS', 'msg') == Día.MARTES
    assert validar_día('MIERCOLES', 'msg') == Día.MIÉRCOLES
    assert validar_día('miércoles', 'msg') == Día.MIÉRCOLES
    assert validar_día('sabado', 'msg') == Día.SÁBADO

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_día(None, 'msg')
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'no debe estar vacío' in mensaje

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_día('hola', 'msg')
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'no se reconoce como un día de la semana' in mensaje

def test_validar_int_positivo_opcional():
    assert validar_int_positivo_opcional(15, 'msg') == 15
    assert validar_int_positivo_opcional('1560', 'msg') == 1560
    assert validar_int_positivo_opcional(None, 'msg') == None
    assert validar_int_positivo_opcional('', 'msg') == None

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_int_positivo_opcional('wegggg', 'msg')
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'no se reconoce como un número entero' in mensaje

    with pytest.raises(DatoInválidoException) as exc_info:
        validar_int_positivo_opcional(0, 'msg')
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'debe ser un número entero positivo' in mensaje
    
def test_debería_ser_time():
    assert debería_ser_time(time(15, 30), 'msg') == time(15, 30)
    
    with pytest.raises(DatoInválidoException) as exc_info:
        debería_ser_time(10, 'msg')
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'no se reconoce como un horario' in mensaje

    with pytest.raises(DatoInválidoException) as exc_info:
        debería_ser_time(None, 'msg')
    
    mensaje = str(exc_info.value)
    assert mensaje.startswith('msg')
    assert 'no debe estar vacío' in mensaje
