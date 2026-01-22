from datetime import time
from typing import Any

from asignacion_aulica.gestor_de_datos.días_y_horarios import Día

from .excepciones import DatoInválidoException

def _es_número_entero(valor: int|str|Any) -> bool:
    return isinstance(valor, int) or (isinstance(valor, str) and valor.isdigit())

def _validar_no_vacío(valor: Any, mensaje: str) -> Any:
    '''
    Validar que `valor` no sea `None` ni un string vacío.

    :param valor: El valor a validar.
    :param mensaje: Se usa como prefijo en el mensaje de la excepción.
    :return: El mismo valor.
    :raise DatoInválidoException: Si `valor` es `None` o el string vacío.
    '''
    if valor is None or valor == '':
        raise DatoInválidoException(mensaje + 'no debe estar vacío.')
    else:
        return valor

def str_posiblemente_vacío(valor: str|Any) -> str:
    '''
    Convertir `valor` a string, excepto que sea `None`.

    Eliminar espacios al principio y final de string.

    :return: `valor` convertido a string, o el string vacío si `valor` es `None`.
    '''
    if valor is None:
        return ''
    else:
        return str(valor).strip()

def validar_str_no_vacío(valor: str|Any, mensaje: str) -> str:
    '''
    Validar que un dato ingresado no esté vacío.

    :param valor: El valor a validar.
    :param mensaje: Se usa como mensaje para la excepción.
    :return: El valor, convertido a string y sin espacios al principio y final.
    :raise DatoInválidoException: Si `valor` está vacío.
    '''
    if valor is not None: 
        valor = str(valor).strip()

    if not valor:
        raise DatoInválidoException(mensaje)
    
    return valor

def validar_año(valor: int|str|Any, mensaje: str) -> int:
    '''
    Validar que un dato ingresado sea un número de año.

    Se consideran números de año sólo a partir del 2000.

    :param valor: Un número o un str que debería representar un año.
    :param mensaje: Se usa como prefijo en el mensaje de la excepción.
    :return: El mismo valor, convertido a int.
    :raise DatoInválidoException: Si `valor` no es un número entero mayor a 1999.
    '''
    _validar_no_vacío(valor, mensaje)

    if not _es_número_entero(valor):
        raise DatoInválidoException(mensaje + 'no se reconoce como un número de año (debe ser un número entero).')
    
    valor = int(valor)
    if valor < 2000:
        raise DatoInválidoException(mensaje + 'no se reconoce como un número de año (sólo se aceptan años a partir del 2000).')
    
    return valor

def validar_año_del_plan_de_estudios(valor: int|str|Any, mensaje) -> int:
    '''
    Validar que un dato ingresado sea un número de año del plan de estudios.

    Se consideran años del plan de estudios los números enteros entre 1 y 9.

    :param valor: Un número o un str que debería representar un año.
    :param mensaje: Se usa como prefijo en el mensaje de la excepción.
    :return: El mismo valor, convertido a int.
    :raise DatoInválidoException: Si `valor` no es un número entero entre 1 y 9.
    '''
    _validar_no_vacío(valor, mensaje)

    if not _es_número_entero(valor):
        raise DatoInválidoException(mensaje + f'"{valor} no se reconoce como un año del plan de estudios (debe ser un número entero).')
    
    valor_int = int(valor)
    if not 0 < valor_int < 10:
        raise DatoInválidoException(mensaje + f'"{valor} no se reconoce como un año del plan de estudios (debe estar entre 1 y 9).')
    
    return valor_int

def validar_día(valor: str|Any, mensaje: str) -> Día:
    '''
    Valida que `valor` sea un string con el nombre de un día de la semana (en
    castellano).

    :param valor: El valor a verificar.
    :param mensaje: Se usa como prefijo en el mensaje de la excepción.
    :return: El día de la semana.
    :raise DatoInválidoException: Si `valor` no es el nombre de un día de la semana.
    '''
    if valor is None or valor == '':
        raise DatoInválidoException(mensaje + 'el día de la semana no debe estar vacío.')
    elif not isinstance(valor, str):
        raise DatoInválidoException(mensaje + 'no se reconoce como un día de la semana.')
    
    valor_mayúculas = valor.upper()

    # Permitir que les falte la tilde
    if valor_mayúculas == 'MIERCOLES':
        valor_mayúculas = 'MIÉRCOLES'
    elif valor_mayúculas == 'SABADO':
        valor_mayúculas = 'SÁBADO'
    
    if valor_mayúculas not in Día:
        raise DatoInválidoException(mensaje + f'"{valor}" no se reconoce como un día de la semana.')
    
    return Día[valor_mayúculas]

def validar_int_positivo_opcional(valor: int|str|None|Any, mensaje: str) -> int|None:
    '''
    Validar que `valor` sea un número entero positivo, un string vacío, o
    `None`.

    Se aceptan como números valores de tipo int y str.

    :param valor: El valor a validar.
    :param mensaje: Se usa como prefijo para el mensaje de la excepción.
    :return: Si `valor` es un número, el mismo valor convertido a int. Si
        `valor` es el string vacío o `None`, `None`.
    :raise DatoInválidoException: Si `valor` no es `None` ni un entero positivo.
    '''
    if valor is None or valor == '':
        return None
    else:
        if not _es_número_entero(valor):
            raise DatoInválidoException(mensaje + f'"{valor}" no se reconoce como un número entero.')
        
        valor_int = int(valor)
        if valor_int <= 0:
            raise DatoInválidoException(mensaje + 'debe ser un número entero positivo.')
        
        return valor_int

def debería_ser_time(valor: time|Any, mensaje: str) -> time:
    '''
    Verificar que `valor` sea de tipo `time`.

    :param valor: El valor a validar.
    :param mensaje: Se usa como prefijo en el mensaje de la excepción.
    :raise DatoInválidoException: Si `valor` no es de tipo `time`.
    '''
    _validar_no_vacío(valor, mensaje)

    if not isinstance(valor, time):
        raise DatoInválidoException(mensaje + f'"{valor}" no se reconoce como un horario.')
    else:
        return valor
