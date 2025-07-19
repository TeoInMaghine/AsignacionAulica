'''
En este módulo se definen validadores de datos para usar en las plantillas.

Los validadores de datos son operadores que excel usa para evitar que los
usuarios ingresen datos no válidos. Estos validadores no se ejecutan en nuestro
programa sino que son parte de excel.
'''
from openpyxl.worksheet.datavalidation import DataValidation

día_de_la_semana = DataValidation(
    type = 'list',
    formula1 = (
        '"Lunes,LUNES,lunes,Martes,MARTES,martes,'
        'Miércoles,MIÉRCOLES,miércoles,Miercoles,MIERCOLES,miercoles,'
        'Jueves,JUEVES,jueves,Viernes,VIERNES,viernes,'
        'Sábado,SÁBADO,sábado,Sabado,SABADO,sabado,Domingo,DOMINGO,domingo"'
    ), # Las dobles comillas son necesarias para que excel no se confunda.
    error = 'Por favor ingresar un día de la semana.',
    errorStyle = 'warning',
    showErrorMessage = True,
    showDropDown = True # True significa False
)
'''
Un validador que acepta los días de la semana (escritos de cualquier forma
medianamente razonable).
'''

no_cambiar_este_valor = DataValidation(
    type='list',
    formula1='""', #Las dobles comillas son necesarias para que excel no se confunda.
    error = 'Por favor no modificar el valor de esta celda.',
    errorStyle = 'stop',
    showErrorMessage = True,
    showDropDown = True # True significa False
)
'''
Un validador que no acepta ningún valor.

Sirve para evitar que los usuarios modifiquen el contenido de una celda.
'''

año_del_calendario = DataValidation(
    type='whole',
    operator='greaterThanOrEqual',
    formula1=2000,
    error = 'El valor de esta celda debe ser un año.',
    errorStyle = 'stop',
    showErrorMessage = True
)
'''
Un validador para números de año.

Solamente acepta números enteros mayores a 1999.
'''

año_del_plan_de_estudios = DataValidation(
    type='whole',
    operator='between',
    formula1=1,
    formula2=9,
    errorTitle = 'El dato ingresado no es válido.',
    error = 'El valor debe ser un año del plan de estudios.\n1, 2, 3, etc.',
    errorStyle = 'warning',
    showErrorMessage = True
)
'''
Un validador para la columna de "Año".

Solamente acepta los números naturales de un dígito.
'''

número_natural = DataValidation(
    type='whole',
    operator='greaterThanOrEqual',
    formula1=0,
    errorTitle = 'El dato ingresado no es válido.',
    error = 'El valor debe ser un número entero no negativo.',
    errorStyle = 'warning',
    showErrorMessage = True
)
'''
Un validador que solamente acepta números naturales (incluyendo el 0).
'''

horario = DataValidation(
    type='time',
    operator = 'between',
    formula1 = 0, # Entre 0 y 1 significa cualquier hora del día
    formula2 = 1,
    error = 'Excel no reconoce el valor ingresado como un horario.',
    errorStyle = 'warning',
    showErrorMessage = True
)
'''
Un validador para horarios.
'''
