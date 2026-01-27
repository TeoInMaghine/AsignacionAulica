'''
Esta prueba carga en un gestor de datos todos los datos del edificio Anasagasti 2
y de la carrera Ingeniería en Computación, hace la asignación automática, y
exporta un excel con los resultados.

El archivo se escribe en el directorio actual por defecto, pero se puede pasar
un nombre de archivo como argumento para sobreescribir ese comportamiento.
'''
from sys import argv
from datetime import time
from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.gestor import GestorDeDatos

gestor = GestorDeDatos()

# Cargar datos de Anasagasti 2
gestor.agregar_edificio()
anasagasti2 = gestor.get_edificio(0)
anasagasti2.nombre = 'Anasagasti 2'

aulas = (
    { 'nombre': "B102-B", 'capacidad': 40, 'equipamiento': {'proyector'} },
    { 'nombre': "B102-A", 'capacidad': 40, 'equipamiento': {'proyector'} },
    { 'nombre': "B101",   'capacidad': 35, 'equipamiento': {'proyector', 'híbrido'} },
    { 'nombre': "B103",   'capacidad': 35, 'equipamiento': {'proyector'} },
    { 'nombre': "B202-B", 'capacidad': 40, 'equipamiento': {'proyector'} },
    { 'nombre': "B202-A", 'capacidad': 40, 'equipamiento': {'proyector'} },
    { 'nombre': "B203",   'capacidad': 20, 'equipamiento': {'proyector', 'computadoras'} },
    { 'nombre': "Pecera", 'capacidad': 8,  'equipamiento': {}},
    { 'nombre': "B102",   'capacidad': 73, 'equipamiento': {'proyector'} },
    { 'nombre': "B202",   'capacidad': 75, 'equipamiento': {'proyector'} }
)

aulas_dobles = (
    (8, 0, 1),
    (9, 4, 5)
)

for i_materia, datos_de_aula in enumerate(aulas):
    gestor.agregar_aula(0)
    aula = gestor.get_aula(0, i_materia)
    aula.nombre = datos_de_aula['nombre']
    aula.capacidad = datos_de_aula['capacidad']
    for e in datos_de_aula['equipamiento']:
        gestor.agregar_equipamiento_a_aula(0, i_materia, e)

for i_aula_doble, aulas in enumerate(aulas_dobles):
    i_grande, i_chica1, i_chica2 = aulas
    gestor.agregar_aula_doble(0)
    aula_doble = gestor.get_aula_doble(0, i_aula_doble)
    aula_doble.aula_grande = gestor.get_aula(0, i_grande)
    aula_doble.aula_chica_1 = gestor.get_aula(0, i_chica1)
    aula_doble.aula_chica_2 = gestor.get_aula(0, i_chica2)

# Cargar datos de ingeniería en computación (1º cuatrimestre 2025)
ing_comp = gestor.agregar_carrera('Ingeniería en Computación')

materias = (
    {
        'nombre': 'B6000 - Matematica I',
        'año': 1,
        'clases': (
            {'comisión': 'C1', 'día': Día.Jueves, 'horario': RangoHorario(time(11), time(15)), 'alumnos': 65, 'promocionable': 'Si (8)', 'docente': 'C. Molina'},
            {'comisión': 'C1', 'día': Día.Miércoles, 'horario': RangoHorario(time(15), time(19)), 'alumnos': 65, 'promocionable': 'Si (8)', 'auxiliar': 'LUCIFERO'},
            {'comisión': 'C2', 'día': Día.Martes, 'horario': RangoHorario(time(13), time(17)), 'alumnos': 65, 'promocionable': 'Si (8)', 'docente': 'N. Werning'},
            {'comisión': 'C2', 'día': Día.Lunes, 'horario': RangoHorario(time(15), time(19)), 'alumnos': 65, 'promocionable': 'Si (8)', 'auxiliar': 'GIANA, FABIAN'},
            {'comisión': 'C3', 'día': Día.Jueves, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 65, 'docente': 'GOUZDEN'},
            {'comisión': 'C3', 'día': Día.Viernes, 'horario': RangoHorario(time(9), time(13)), 'alumnos': 65, 'auxiliar': 'MAGGI'}
        )
    },
    {
        'nombre': 'B6001 - Introducción a la Ing. En Computación',
        'año': 1,
        'clases': (
            {'comisión': 'C1', 'día': Día.Martes, 'horario': RangoHorario(time(9), time(13)), 'alumnos': 65, 'promocionable': 'Si (8)', 'docente': 'P. Britos', 'auxiliar': 'M. Fermin / CATALANO', 'virtual': True},
            {'comisión': 'C1', 'día': Día.Miércoles, 'horario': RangoHorario(time(18), time(22)), 'alumnos': 65, 'promocionable': 'Si (8)', 'docente': 'P. Britos', 'auxiliar': 'M. Fermin / CATALANO', 'virtual': True},
            {'comisión': 'C2', 'día': Día.Martes, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 65, 'promocionable': 'Si (8)', 'docente': 'P. Argañaras', 'auxiliar': 'M. Fermin / CATALANO', 'virtual': True},
            {'comisión': 'C2', 'día': Día.Jueves, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 65, 'promocionable': 'Si (8)', 'docente': 'P. Argañaras', 'auxiliar': 'M. Fermin / CATALANO'}
        )
    },
    {
        'nombre': 'T0002 - Introducción a la Lectura y Escritura Académica',
        'año': 1,
        'clases': (
            {'comisión': 'C1', 'día': Día.Miércoles, 'horario': RangoHorario(time(15), time(17)), 'alumnos': 50, 'promocionable': 'Si (7)', 'docente': 'I. Silin', 'auxiliar': 'M. Rey'},
            {'comisión': 'C1', 'día': Día.Viernes, 'horario': RangoHorario(time(15), time(17)), 'alumnos': 50, 'promocionable': 'Si (7)', 'docente': 'I. Silin', 'auxiliar': 'M. Rey'},
            {'comisión': 'C2', 'día': Día.Miércoles, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 50, 'promocionable': 'Si (7)', 'docente': 'I. Silin', 'auxiliar': 'M. Rey'},
            {'comisión': 'C2', 'día': Día.Viernes, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 50, 'promocionable': 'Si (7)', 'docente': 'I. Silin', 'auxiliar': 'M. Rey'},
            {'comisión': 'C3', 'día': Día.Viernes, 'horario': RangoHorario(time(15), time(17)), 'alumnos': 50, 'promocionable': 'Si (7)', 'docente': 'MAGARIL', 'virtual': True},
            {'comisión': 'C3', 'día': Día.Viernes, 'horario': RangoHorario(time(15), time(17)), 'alumnos': 50, 'promocionable': 'Si (7)', 'docente': 'MAGARIL', 'virtual': True} # Esta en realidad es asincrónica pero nuestro modelo de datos no soporta eso.
        )
    },
    {
        'nombre': 'B6006 - Matematica II',
        'año': 2,
        'clases': (
            {'día': Día.Martes, 'horario': RangoHorario(time(11), time(15)), 'alumnos': 70, 'promocionable': 'Si (8)', 'docente': 'C. Molina'},
            {'día': Día.Jueves, 'horario': RangoHorario(time(11), time(15)), 'alumnos': 70, 'promocionable': 'Si (8)', 'auxiliar': 'ALBORNOZ, L.'}
        )
    },
    {
        'nombre': 'B6008 - Programación II',
        'año': 2,
        'clases': (
            {'día': Día.Miércoles, 'horario': RangoHorario(time(17), time(20)), 'alumnos': 75, 'promocionable': 'Si (7)', 'docente': 'M. Vilugron'},
            {'día': Día.Viernes, 'horario': RangoHorario(time(18), time(21)), 'alumnos': 75, 'promocionable': 'Si (7)', 'docente': 'MARIGUIN'}
        )
    },
    {
        'nombre': 'B6009 - Arquitectura de Computadoras I',
        'año': 2,
        'clases': (
            {'día': Día.Lunes, 'horario': RangoHorario(time(17), time(20)), 'alumnos': 80, 'docente': 'I. Nomdedeu', 'promocionable': 'Si (7)', 'virtual': True},
            {'día': Día.Miércoles, 'horario': RangoHorario(time(20), time(23)), 'alumnos': 80, 'docente': 'I. Nomdedeu', 'promocionable': 'Si (7)'}
        )
    },
    {
        'nombre': 'B6011 - Física General II',
        'año': 2,
        'clases': (
            {'día': Día.Martes, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 50, 'docente': 'Albornoz L.', 'auxiliar': 'Baez L.', 'promocionable': 'Si (8)', 'virtual': True},
            {'día': Día.Viernes, 'horario': RangoHorario(time(9), time(13)), 'alumnos': 50, 'docente': 'Albornoz L.', 'auxiliar': 'Baez L.', 'promocionable': 'Si (8)'}
        )
    },
    {
        'nombre': 'B6013 - Bases de Datos',
        'año': 3,
        'clases': (
            {'día': Día.Miércoles, 'horario': RangoHorario(time(18), time(21)), 'alumnos': 40, 'docente': 'C. Tejero', 'promocionable': 'Si (8)'},
            {'día': Día.Lunes, 'horario': RangoHorario(time(18), time(21)), 'alumnos': 40, 'docente': 'C. Tejero', 'promocionable': 'Si (8)', 'virtual': True}
        )
    },
    {
        'nombre': 'B6014 - Introducción a los Sistemas Distribuidos y Paralelos',
        'año': 3,
        'clases': (
            {'día': Día.Martes, 'horario': RangoHorario(time(16), time(21)), 'alumnos': 45, 'docente': 'WALTER AGÜERO', 'virtual': True},
            {'día': Día.Jueves, 'horario': RangoHorario(time(16), time(17)), 'alumnos': 45, 'docente': 'WALTER AGÜERO', 'virtual': True}
        )
    },
    {
        'nombre': 'B6016 - Laboratorio de Sistemas Embebidos',
        'año': 3,
        'clases': (
            {'día': Día.Jueves, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 45, 'docente': 'Castillo', 'promocionable': 'No', 'virtual': True},
            {'día': Día.Viernes, 'horario': RangoHorario(time(17), time(21)), 'alumnos': 45, 'docente': 'Castillo', 'promocionable': 'No'}
        )
    },
    {
        'nombre': 'B6017 - Seguridad Ambiental',
        'año': 3,
        'clases': (
            {'día': Día.Viernes, 'horario': RangoHorario(time(13), time(17)), 'alumnos': 40, 'promocionable': 'Si (8)', 'docente': 'RIBERI, V'},
        )
    },
    {
        'nombre': 'B6021 - INGENIERIA DE SOFTWARE I',
        'año': 4,
        'clases': (
            {'día': Día.Martes, 'horario': RangoHorario(time(17, 30), time(20, 30)), 'alumnos': 30, 'promocionable': 'Si (8)', 'docente': 'Britos', 'virtual': True},
            {'día': Día.Jueves, 'horario': RangoHorario(time(17, 30), time(20, 30)), 'alumnos': 30, 'promocionable': 'Si (8)', 'docente': 'Britos', 'virtual': True}
        )
    },
    {
        'nombre': 'B6022 - PROBABILIDAD, ESTADISTICA Y PROCESOS ALEATORIOS',
        'año': 4,
        'clases': (
            {'día': Día.Martes, 'horario': RangoHorario(time(19), time(22)), 'alumnos': 30, 'docente': 'Reynoso Andrés'},
            {'día': Día.Jueves, 'horario': RangoHorario(time(18), time(21)), 'alumnos': 30, 'docente': 'Reynoso Andrés', 'virtual': True}
        )
    },
    {
        'nombre': 'B6024 - ARQUITECTURA DE COMPUTADORAS II',
        'año': 4,
        'clases': (
            {'día': Día.Lunes, 'horario': RangoHorario(time(17), time(20)), 'alumnos': 50, 'docente': 'Nomdedeu', 'virtual': True},
            {'día': Día.Miércoles, 'horario': RangoHorario(time(20), time(23)), 'alumnos': 50, 'docente': 'Nomdedeu', 'virtual': True}
        )
    },
    {
        'nombre': 'V1275 - CIENCIA DE DATOS APLICADA',
        'año': 4,
        'clases': (
            {'día': Día.Lunes, 'horario': RangoHorario(time(17), time(20)), 'alumnos': 30, 'promocionable': 'Si (7)', 'docente': 'Britos', 'virtual': True},
            {'día': Día.Miércoles, 'horario': RangoHorario(time(17), time(20)), 'alumnos': 30, 'promocionable': 'Si (7)', 'docente': 'Britos', 'virtual': True}
        )
    },
    {
        'nombre': 'B5672 - COMUNICACIONES ANALOGICAS Y DIGITALES',
        'año': 5,
        'clases': (
            {'día': Día.Martes, 'horario': RangoHorario(time(13), time(16)), 'alumnos': 30, 'promocionable': 'Si (7)', 'docente': 'COGO Jorge'},
            {'día': Día.Jueves, 'horario': RangoHorario(time(13), time(16)), 'alumnos': 30, 'promocionable': 'Si (7)', 'docente': 'COGO Jorge'}
        )
    },
    {
        'nombre': 'B6038 - ECONOMIA Y ORGANIZACION INDUSTRIAL',
        'año': 5,
        'clases': (
            {'día': Día.Sábado, 'horario': RangoHorario(time(8, 30), time(12, 30)), 'alumnos': 30, 'promocionable': 'Si (8)', 'docente': 'Contin'},
        )
    }
)

for i_materia, datos_de_materia in enumerate(materias):
    gestor.agregar_materia(ing_comp)
    materia = gestor.get_materia(ing_comp, i_materia)
    materia.nombre = datos_de_materia['nombre']
    materia.año = datos_de_materia['año']
    materia.cuatrimestral_o_anual = 'Cuatrimestral'
    for i_clase, datos_de_clase in enumerate(datos_de_materia['clases']):
        gestor.agregar_clase(ing_comp, i_materia)
        clase = gestor.get_clase(ing_comp, i_materia, i_clase)
        clase.día = datos_de_clase['día']
        clase.horario = datos_de_clase['horario']
        clase.virtual = datos_de_clase.get('virtual', False)
        clase.cantidad_de_alumnos = datos_de_clase['alumnos']
        clase.comisión = datos_de_clase.get('comisión', '')
        clase.teórica_o_práctica = datos_de_clase.get('teórica o práctica', 'Teórico/Práctica')
        clase.promocionable = datos_de_clase.get('promocionable', '')
        clase.docente = datos_de_clase.get('docente', '')
        clase.auxiliar = datos_de_clase.get('auxiliar', '')
        for e in datos_de_clase.get('equipamiento', set()):
            gestor.agregar_equipamiento_a_clase(ing_comp, i_materia, i_clase, e)

# Asignar aulas y exportar datos
result = gestor.asignar_aulas()
if result.días_sin_asignar:
    print(f'No se pudieron asignar los días: {result.días_sin_asignar}')

print(f'Clases con aula chica: {len(result.clases_con_aula_chica)}')

filename = argv[1] if len(argv) > 1 else './IngenieríaEnComputación.xlsx'
gestor.exportar_clases_a_excel(filename)
