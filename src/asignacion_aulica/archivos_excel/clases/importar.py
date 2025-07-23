from openpyxl.worksheet.worksheet import Worksheet

from asignacion_aulica.validación_de_datos.excepciones import DatoInválidoException, ExcelInválidoException
from asignacion_aulica.validación_de_datos.validaciones import validar_año, validar_str_no_vacío

def leer_preámbulo(hoja: Worksheet) -> tuple[str, int, str|int]:
    '''
    Verifica que el preámbulo de una hoja del archivo sea válido y extrae sus
    datos.

    :return: Nombre de la carrera, año, cuatrimestre.
    :raise InvalidExcelException: Si el contenido del preámbulo no es válido.
    '''
    if hoja['C1'].value != 'Carrera: ' or hoja['C2'].value != 'Año: ' or hoja['E2'].value != 'Cuatrimestre: ':
        raise ExcelInválidoException('El encabezado del archivo fue modificado. Por favor usar la plantilla sin modificar el encabezado.')
    
    carrera = validar_str_no_vacío(hoja['D1'].value, 'El nombre de la carrera en la celda D1 no puede estar vacío.')
    año = validar_año(hoja['D2'].value, 'El valor de la celda D2 no es válido.')
    cuatrimestre = hoja['G2'].value

    return carrera, año, cuatrimestre
