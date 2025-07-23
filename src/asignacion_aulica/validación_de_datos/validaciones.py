from .excepciones import DatoInválidoException

def validar_año(valor: int|str, mensaje: str = '') -> int:
    '''
    Validar que un dato ingresado sea un número de año.

    Se consideran números de año sólo a partir del 2000.

    :param valor: Un número o un str que debería representar un año.
    :param mensaje: Se usa como prefijo en el mensaje de la excepción.
    :return: El mismo valor, convertido a int.
    :raise DatoInválidoException: Si `valor` no es un número entero mayor a 1999.
    '''
    es_número_entero = isinstance(valor, int) or (isinstance(valor, str) and valor.isdigit())
    if not es_número_entero:
        raise DatoInválidoException(mensaje+'No se reconoce como un número de año (debe ser un número entero).')
    
    valor = int(valor)
    if valor < 2000:
        raise DatoInválidoException(mensaje+'No se reconoce como un número de año (sólo se aceptan años a partir del 2000).')
    
    return valor

def validar_str_no_vacío(valor: str|None, mensaje: str = '') -> str:
    '''
    Validar que un dato ingresado no esté vacío.

    :param valor: El valor a validar.
    :param mensaje: Se usa como mensaje para la excepción.
    :return: El mismo string pero sin espacios al principio y final.
    :raise DatoInválidoException: Si `valor` está vacío.
    '''
    if valor is None: 
        raise DatoInválidoException(mensaje)

    valor = valor.strip()
    if not valor:
        raise DatoInválidoException(mensaje)
    
    return valor
