from asignacion_aulica.validación_de_datos.excepciones import DatoInválidoException
from asignacion_aulica.validación_de_datos.validaciones import validar_año, validar_str_no_vacío

import pytest

def test_años_válidos():
    assert validar_año(2000) == 2000
    assert validar_año(2025) == 2025
    assert validar_año('2032') == 2032

def test_años_no_válidos():
    with pytest.raises(DatoInválidoException):
        validar_año(2025.0) # No es int

    with pytest.raises(DatoInválidoException):
        validar_año(32) # Es muy chico

    with pytest.raises(DatoInválidoException):
        validar_año('123hola5') # No es un número

def test_validar_str_no_vacío():
    assert validar_str_no_vacío('hola') == 'hola'
    assert validar_str_no_vacío(' 123  ') == '123'

    with pytest.raises(DatoInválidoException):
        validar_str_no_vacío('')
    
    with pytest.raises(DatoInválidoException):
        validar_str_no_vacío('  ')
    
    with pytest.raises(DatoInválidoException):
        validar_str_no_vacío(None)
