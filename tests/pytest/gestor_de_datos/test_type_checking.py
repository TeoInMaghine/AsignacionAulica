from dataclasses import dataclass
from datetime import time
from asignacion_aulica.gestor_de_datos.días_y_horarios import HorariosSemanales, HorariosSemanalesOpcionales, RangoHorario, crear_horarios_semanales, crear_horarios_semanales_opcionales
from asignacion_aulica.gestor_de_datos.type_checking import is_instance_of_type

def test_None():
    assert is_instance_of_type(None, None)
    assert is_instance_of_type(None, type(None))
    assert not is_instance_of_type('', None)
    assert not is_instance_of_type('', type(None))

def test_str():
    assert is_instance_of_type('', str)
    assert not is_instance_of_type(None, str)
    assert not is_instance_of_type(['a', 'b'], str)

def test_optional_str():
    assert is_instance_of_type('aa', str|None)
    assert is_instance_of_type(None, str|None)
    assert not is_instance_of_type(1, str|None)

def test_set_of_str():
    assert is_instance_of_type({'a', 'b'}, set[str])
    assert is_instance_of_type(set(), set[str])
    assert not is_instance_of_type(['a'], set[str])
    assert not is_instance_of_type([], set[str])
    assert not is_instance_of_type('a', set[str])

def test_list_of_dataclass():
    @dataclass
    class A:
        a: int
    
    assert is_instance_of_type([A(1), A(2)], list[A])
    assert is_instance_of_type([], list[A])
    assert not is_instance_of_type((A(1), A(2)), list[A])

def test_horarios_semanales():
    assert is_instance_of_type(crear_horarios_semanales(), HorariosSemanales)
    assert not is_instance_of_type(crear_horarios_semanales_opcionales(), HorariosSemanales)
    assert not is_instance_of_type((RangoHorario(time(1), time(2)),), HorariosSemanales)

def test_horarios_semanales_opcionales():
    assert is_instance_of_type(crear_horarios_semanales_opcionales(), HorariosSemanalesOpcionales)
    assert is_instance_of_type(crear_horarios_semanales(), HorariosSemanalesOpcionales)
    assert not is_instance_of_type((RangoHorario(time(1), time(2)),), HorariosSemanales)
    assert not is_instance_of_type((None, None), HorariosSemanales)

    horarios_arbitrarios = HorariosSemanalesOpcionales((
        RangoHorario(time(3), time(7)),
        None,
        RangoHorario(time(0), time(3)),
        RangoHorario(time(4), time(23)),
        RangoHorario(time(7), time(15)),
        None,
        RangoHorario(time(2), time(2)),
    ))
    assert is_instance_of_type(horarios_arbitrarios, HorariosSemanalesOpcionales)
