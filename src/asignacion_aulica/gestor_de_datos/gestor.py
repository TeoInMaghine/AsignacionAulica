from collections.abc import Sequence
from datetime import time
from itertools import filterfalse
from typing import Callable
from collections import Counter
import logging

from asignacion_aulica.lógica_de_asignación.postprocesamiento import InfoPostAsignación
from asignacion_aulica.lógica_de_asignación.asignación import asignar
from asignacion_aulica.gestor_de_datos.días_y_horarios import RangoHorario, Día
from asignacion_aulica.gestor_de_datos.entidades import (
    Aula,
    AulaDoble,
    Carrera,
    Clase,
    Edificio,
    Materia,
    todas_las_clases
)

logger = logging.getLogger(__name__)

aula_no_seleccionada: Aula = Aula(nombre='Sin Seleccionar', edificio=None, capacidad=0)
'''
Aula dummy usada para inicializar las aulas dobles.
'''

class GestorDeDatos:
    '''
    Objeto encargado de administrar todos los datos de edificios, aulas, y
    clases.

    Internamente usa una base de datos para almacenar los datos de manera
    persistente.

    Los campos de las entidades se identifican con números, los cuales se
    corresponden con el orden de los campos en cada entidad y los mal llamados
    roles de la UI.

    La lista de carreras se mantiene ordenada alfabéticamente, pero la de
    edificios sólo se ordena a pedido.
    '''

    def __init__(self, path_base_de_datos: str|None = None):
        '''
        :param path_base_de_datos: El path absoluto del archivo de la base de
        datos. Si el archivo no existe, es creado. ``None`` para no guardar
        datos.
        '''
        logger.info('Creando gestor de datos con path_base_de_datos=%s', path_base_de_datos)

        self._edificios: list[Edificio] = []
        self._carreras: list[Carrera] = []
        self._equipamientos: Counter[str] = Counter()

    def get_edificios(self) -> list[str]:
        '''
        :return: Los nombres de todos los edificios en la base de datos,
        ordenados alfabéticamente.
        '''
        nombres = [edificio.nombre for edificio in self._edificios]
        nombres.sort(key=lambda nombre: nombre.lower())
        return nombres

    def cantidad_de_edificios(self) -> int:
        return len(self._edificios)

    def get_edificio(self, edificio: int) -> Edificio:
        '''
        Obtener el edificio (no una copia), el cual puede inspeccionarse, y
        algunos de sus miembros modificarse directamente:
        - `nombre`
        - `preferir_no_usar`
        - `horarios`

        :param edificio: El índice del edificio.
        :return: El edificio en el índice dado.
        :raise IndexError: Si el índice está fuera de rango.
        '''
        return self._edificios[edificio]

    def existe_edificio(self, nombre: str) -> bool:
        '''
        :param nombre: Nombre a buscar en la lista de edificios.
        :return: `True` si hay un edificio con ese nombre en la base de datos,
        `False` si no.

        No se distinguen mayúsculas de minúsculas.
        '''
        nombre = nombre.lower().strip()
        return any(
            edificio.nombre.lower() == nombre
            for edificio in self._edificios
        )

    def agregar_edificio(self):
        '''
        Añadir un nuevo edificio después del último índice existente.

        Se inicializa con valores por defecto, asegurando que tenga un nombre
        único.
        '''
        nombres_existentes = [edificio.nombre for edificio in self._edificios]
        nombre_nuevo = _generar_nombre_no_existente('Edificio sin nombre', nombres_existentes)
        self._edificios.append(Edificio(nombre_nuevo))
        logger.debug('Se agregó edificio con nombre %s', nombre_nuevo)

    def borrar_edificio(self, índice: int):
        '''
        Borrar de la base de datos el edificio en el índice dado.

        :raise IndexError: Si el índice está fuera de rango.
        '''
        logger.debug('borrar_edificio %s', índice)

        # Sacar el edificio de la lista
        el_edificio = self._edificios.pop(índice)
        
        # Sacar el edificio de las carreras que lo tienen como preferido
        for carrera in self._carreras:
            if carrera.edificio_preferido is el_edificio:
                carrera.edificio_preferido = None
        
        # Borrar asignaciones a este edificio
        for clase in todas_las_clases(self._carreras):
            if clase.aula_asignada and clase.aula_asignada.edificio is el_edificio:
                clase.aula_asignada = None

    def ordenar_edificios(self):
        '''
        Ordena los edificios alfabéticamente.
        '''
        logger.debug('ordenar_edificios')
        self._edificios.sort(key=lambda edificio: edificio.nombre.lower())

    def get_aulas(self, edificio: int) -> list[str]:
        '''
        :return: Los nombres de todas las aulas de un edificio en la base de
        datos, ordenados alfabéticamente.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        nombres = [aula.nombre for aula in self._edificios[edificio].aulas]
        nombres.sort(key=lambda nombre: nombre.lower())
        return nombres

    def cantidad_de_aulas(self, edificio: int) -> int:
        '''
        :return: La cantidad de aulas de un edificio en la base de datos.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        return len(self._edificios[edificio].aulas)

    def get_aula(self, edificio: int, aula: int) -> Aula:
        '''
        Obtener el aula (no una copia), la cual puede inspeccionarse, y algunos
        de sus miembros modificarse directamente:
        - `nombre`
        - `capacidad`
        - `horarios`

        :param edificio: El índice del edificio.
        :param aula: El índice del aula.
        :return: El aula en los índices dados.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        return self._edificios[edificio].aulas[aula]

    def agregar_aula(self, edificio: int):
        '''
        Añadir al edificio un nuevo aula, después del último índice existente.

        Se inicializa con valores por defecto, asegurando que tenga un nombre
        único.

        :param edificio: El índice del edificio.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        el_edificio = self._edificios[edificio]
        nombres_existentes = [aula.nombre for aula in el_edificio.aulas]
        nombre_nuevo = _generar_nombre_no_existente('Sin nombre', nombres_existentes)
        
        el_edificio.aulas.append(Aula(
            nombre = nombre_nuevo,
            edificio = el_edificio,
            capacidad = 1
        ))

        logger.debug('agregar_aula - edificio=%s nombre=%s', edificio, nombre_nuevo)

    def existe_aula(self, edificio: int, nombre: str) -> bool:
        '''
        :return: `True` si el aula especificada existe en la base de datos,
        `False` si no.

        No se distinguen mayúsculas de minúsculas.

        :param edificio: El índice del edificio.
        :param nombre: El nombre del aula.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        nombre = nombre.lower().strip()
        el_edificio = self._edificios[edificio]
        return any(aula.nombre.lower() == nombre for aula in el_edificio.aulas)

    def borrar_aula(self, edificio: int, índice: int):
        '''
        Borrar de la base de datos el aula especificada.

        :param edificio: El índice del edificio.
        :param índice: El índice del aula.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        logger.debug('borrar_aula - edificio=%s índice=%s', edificio, índice)

        el_edificio = self._edificios[edificio]

        # Sacar el aula de la lista
        el_aula = el_edificio.aulas.pop(índice)
        
        # Borrar aulas dobles que usen este aula
        el_edificio.aulas_dobles[:] = filterfalse(
            lambda ad: ad.aula_grande is el_aula or ad.aula_chica_1 is el_aula or ad.aula_chica_2 is el_aula,
            el_edificio.aulas_dobles
        )

        # Borrar asignaciones a este aula
        for clase in todas_las_clases(self._carreras):
            if clase.aula_asignada is el_aula:
                clase.aula_asignada = None

    def ordenar_aulas(self, edificio: int):
        '''
        Ordena alfabéticamente las aulas del edificio especificado.

        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        logger.debug('ordenar_aulas - edificio=%s', edificio)
        self._edificios[edificio].aulas.sort(key=lambda aula: aula.nombre.lower())

    def cantidad_de_aulas_dobles(self, edificio: int) -> int:
        '''
        :return: La cantidad de aulas dobles de un edificio en la base de datos.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        return len(self._edificios[edificio].aulas_dobles)

    # TODO: re-considerar la interfaz de aulas dobles cuando se implemente en
    # la UI. Quizás es error prone el setear las aulas directamente, se podría
    # accidentalmente asignar un aula de otro edificio por ejemplo.
    def get_aula_doble(self, edificio: int, aula_doble: int) -> AulaDoble:
        '''
        Obtener el aula doble (no una copia), la cual puede inspeccionarse y
        modificarse a qué aulas apuntan sus miembros.

        :param edificio: El índice del edificio.
        :param aula_doble: El índice del aula doble.
        :return: El aula doble en los índices dados.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        return self._edificios[edificio].aulas_dobles[aula_doble]

    def agregar_aula_doble(self, edificio: int):
        '''
        Añadir al edificio un nuevo aula doble, después del último índice
        existente.

        :param edificio: El índice del edificio.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        logger.debug('agregar_aula_doble - edificio=%s', edificio)
        self._edificios[edificio].aulas_dobles.append(AulaDoble(
            aula_no_seleccionada, aula_no_seleccionada, aula_no_seleccionada
        ))

    def existe_aula_en_aulas_dobles(self, edificio: int, aula: int) -> bool:
        '''
        :param edificio: El índice del edificio.
        :param aula: El índice del aula.
        :return: `True` si el aula ya forma parte de un aula doble,
        `False` si no.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        el_edificio: Edificio = self._edificios[edificio]
        el_aula: Aula = el_edificio.aulas[aula]
        aulas_dobles: list[AulaDoble] = el_edificio.aulas_dobles
        return any(
            el_aula in (
                aula_doble.aula_grande,
                aula_doble.aula_chica_1,
                aula_doble.aula_chica_2
            ) for aula_doble in aulas_dobles
        )

    def borrar_aula_doble(self, edificio: int, índice: int):
        '''
        Borrar de la base de datos el aula doble especificada.

        :param edificio: El índice del edificio.
        :param índice: El índice del aula doble.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        logger.debug('borrar_aula_doble - edificio=%s, índice=%s', edificio, índice)
        del self._edificios[edificio].aulas_dobles[índice]

    def ordenar_aulas_dobles(self, edificio: int):
        '''
        Ordena las aulas dobles del edificio especificado, por orden alfabético
        de los nombres de las aulas grandes.

        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        logger.debug('ordenar_aulas_dobles - edificio=%s', edificio)
        self._edificios[edificio].aulas_dobles.sort(key=lambda aula_doble: aula_doble.aula_grande.nombre.lower())

    def cantidad_de_carreras(self) -> int:
        return len(self._carreras)

    def get_carreras(self) -> list[str]:
        '''
        :return: Los nombres de todas las carreras en la base de
        datos, ordenadas alfabéticamente.
        '''
        nombres = [carrera.nombre for carrera in self._carreras]
        return nombres

    def get_carrera(self, índice: int) -> Carrera:
        '''
        :return: La carrera con el índice dado.
        :raise IndexError: Si el índice está fuera de rango.
        '''
        return self._carreras[índice]

    def agregar_carrera(self, nombre: str) -> int:
        '''
        Añadir una nueva carrera con el nombre dado, inicializada con valores
        por defecto.

        :return: El índice de la nueva carrera.
        :raise ValueError: Si `nombre` está vacío o si ya existe una carrera con
        el mismo nombre.
        '''
        logger.info('Agregando carrera: %s', nombre)
        
        nombre = nombre.strip()
        if not nombre:
            raise ValueError('No se puede agregar una carrera son nombre vacío.')
        if self.existe_carrera(nombre):
            raise ValueError(f'Ya existe una carrera llamada {nombre}.')

        nueva = Carrera(nombre)
        self._carreras.append(nueva)
        self._carreras.sort(key=lambda carrera: carrera.nombre.lower())
        return self._carreras.index(nueva)
    
    def existe_carrera(self, nombre: str) -> bool:
        '''
        :return: `True` si hay una carrera con ese nombre, `False` si no.

        No se distinguen mayúsculas de minúsculas.
        '''
        nombre = nombre.lower().strip()
        return any(carrera.nombre.lower() == nombre for carrera in self._carreras)

    def set_carrera_nombre(self, índice: int, nombre_nuevo: str) -> int:
        '''
        Renombrar una carrera existente.

        :return: El nuevo índice de la carrera.
        :raise IndexError: Si el índice está fuera de rango.
        :raise ValueError: Si ya existe una carrera con el nombre dado, o si el
        nombre dado es un string vacío.
        '''
        nombre_nuevo = nombre_nuevo.strip()
        nombre_actual = self._carreras[índice].nombre
        logger.info('Renombrar carrera %s a %s', nombre_actual, nombre_nuevo)
        
        if len(nombre_nuevo) == 0:
            raise ValueError('El nombre de la carrera no puede estar vacío.')

        # Detectar si ya existe una carrera con ese nombre, pero permitir cambio
        # de capitalización
        la_carrera = self._carreras[índice]
        ya_existe: bool = \
            nombre_nuevo.lower() in (
                carrera.nombre.lower()
                for carrera in self._carreras
                if carrera is not la_carrera
            )

        if ya_existe:
            raise ValueError(f'Ya existe una carrera llamada "{nombre_nuevo}".')
        else:
            la_carrera.nombre = nombre_nuevo
            self._carreras.sort(key=lambda carrera: carrera.nombre.lower())
            nuevo_índice = self._carreras.index(la_carrera)
            return nuevo_índice

    def borrar_carrera(self, índice: int):
        '''
        Borrar una carrera de la base de datos.

        :raise IndexError: Si el índice está fuera de rango.
        '''
        logger.info('Borrando carrera %s', self._carreras[índice].nombre)
        del self._carreras[índice]

    def cantidad_de_materias(self, carrera: int) -> int:
        '''
        :param carrera: El índice de la carrera.
        :raise IndexError: Si el índice de la carrera está fuera de rango.
        '''
        return len(self._carreras[carrera].materias)

    def get_materia(self, carrera: int, materia: int) -> Materia:
        '''
        Obtener la materia (no una copia), la cual puede inspeccionarse, y
        algunos de sus miembros modificarse directamente:
        - `nombre`
        - `año`
        - `cuatrimestral_o_anual`

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :return: La materia en los índices dados.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        return self._carreras[carrera].materias[materia]

    def existe_materia(self, carrera: int, nombre: str) -> bool:
        '''
        :return: `True` si la materia especificada existe en la base de datos,
        `False` si no.

        No se distinguen mayúsculas de minúsculas.

        :param carrera: El índice de la carrera.
        :param nombre: El nombre de la materia a buscar.
        :raise IndexError: Si el índice de la carrera está fuera de rango.
        '''
        nombre = nombre.lower().strip()
        la_carrera = self._carreras[carrera]
        return any(materia.nombre.lower() == nombre for materia in la_carrera.materias)

    def agregar_materia(self, carrera: int):
        '''
        Añadir a una carrera una nueva materia, después del último índice
        existente.

        Se inicializa con valores por defecto, asegurando que tenga un nombre
        único.

        :param carrera: El índice de la carrera.
        :raise IndexError: Si el índice de la carrera está fuera de rango.
        '''
        la_carrera = self._carreras[carrera]
        nombres_existentes = [materia.nombre for materia in la_carrera.materias]
        nombre_nuevo = _generar_nombre_no_existente('Sin nombre', nombres_existentes)
        
        la_carrera.materias.append(Materia(
            nombre = nombre_nuevo,
            carrera = la_carrera,
            año = 1
        ))

    def borrar_materia(self, carrera: int, materia: int):
        '''
        Borrar la materia especificada de la base de datos.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        del self._carreras[carrera].materias[materia]

    def ordenar_materias(self, carrera: int):
        '''
        Ordena alfabéticamente las materias de la carrera especificada.

        :raise IndexError: Si el índice de la carrera está fuera de rango.
        '''
        self._carreras[carrera].materias.sort(key=lambda materia: materia.nombre.lower())

    def cantidad_de_clases(self, carrera: int, materia: int) -> int:
        '''
        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :return: la cantidad de clases que tiene la materia especificada.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        return len(self._carreras[carrera].materias[materia].clases)

    def get_clase(self, carrera: int, materia: int, clase: int) -> Clase:
        '''
        Obtener la clase (no una copia), la cual puede inspeccionarse, y
        la mayoría de sus miembros modificarse directamente, excepto:
        - `materia`
        - `equipamiento_necesario`

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param clase: El índice de la clase.
        :return: La clase en los índices dados.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        return self._carreras[carrera].materias[materia].clases[clase]

    def agregar_clase(self, carrera: int, materia: int):
        '''
        Añadir una nueva clase a una carrera, después del último índice
        existente.

        Se inicializa con valores por defecto.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        la_materia = self._carreras[carrera].materias[materia]
        la_materia.clases.append(Clase(
            materia=la_materia,
            día=Día.Lunes,
            horario=RangoHorario(time(10), time(11)),
            virtual=False,
            cantidad_de_alumnos=1
        ))

    def borrar_clase(self, carrera: int, materia: int, clase: int):
        '''
        Borrar de la base de datos la clase especificada.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param clase: El índice de la clase.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        del self._carreras[carrera].materias[materia].clases[clase]

    def get_equipamientos_existentes(self) -> list[str]:
        '''
        :return: Una lista de los equipamientos existentes en aulas y clases, en
        orden alfabético.
        '''
        nombres = list(self._equipamientos.keys())
        nombres.sort(key=lambda nombre: nombre.lower())
        return nombres
    
    def agregar_equipamiento_a_aula(self, edificio: int, aula: int, equipamiento: str):
        '''
        Agrega un equipamiento a un aula.

        El nombre del equipamiento se normaliza para evitar diferencias de
        minúsculas/mayúsculas y de espacios invisibles.

        :param edificio: El índice del edificio.
        :param índice: El índice del aula.
        :param equipamiento: El nombre de un equipamiento.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        # Borrar espacios y unificar mayúsculas/minúsculas
        equipamiento = equipamiento.strip().title()

        equipamientos_del_aula = self._edificios[edificio].aulas[aula].equipamiento

        if equipamiento not in equipamientos_del_aula:
            equipamientos_del_aula.add(equipamiento)
            self._equipamientos[equipamiento] += 1
    
    def borrar_equipamiento_de_aula(self, edificio: int, aula: int, equipamiento: str):
        '''
        :param edificio: El índice del edificio.
        :param índice: El índice del aula.
        :param equipamiento: El nombre de un equipamiento.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        el_aula = self._edificios[edificio].aulas[aula]
        if equipamiento in el_aula.equipamiento:
            el_aula.equipamiento.discard(equipamiento)
            self._equipamientos[equipamiento] -= 1
            # Esto borra los equipamientos con contadores en 0
            self._equipamientos = +self._equipamientos
        
    def agregar_equipamiento_a_clase(self, carrera: int, materia: int, clase: int, equipamiento: str):
        '''
        Agrega un equipamiento necesario en una clase.

        El nombre del equipamiento se normaliza para evitar diferencias de
        minúsculas/mayúsculas y de espacios invisibles.
        
        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param clase: El índice de la clase.
        :param equipamiento: El nombre de un equipamiento.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        # Borrar espacios y unificar mayúsculas/minúsculas
        equipamiento = equipamiento.strip().title()

        equipamientos_de_la_clase = self._carreras[carrera].materias[materia].clases[clase].equipamiento_necesario
        if equipamiento not in equipamientos_de_la_clase:
            equipamientos_de_la_clase.add(equipamiento)
            self._equipamientos[equipamiento] += 1

    def borrar_equipamiento_de_clase(self, carrera: int, materia: int, clase: int, equipamiento: str):
        '''
        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param clase: El índice de la clase.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        la_clase = self._carreras[carrera].materias[materia].clases[clase]
        if equipamiento in la_clase.equipamiento_necesario:
            la_clase.equipamiento_necesario.discard(equipamiento)
            self._equipamientos[equipamiento] -= 1
            # Esto borra los equipamientos con contadores en 0
            self._equipamientos = +self._equipamientos

    def validar_datos(self) -> str|None:
        '''
        Verificar que los datos contenidos en la base de datos sean válidos y
        compatibles entre sí.

        La mayoría de los datos se pueden validar en el momento en el que se
        ingresan, pero hay algunas relaciones entre datos que no se pueden
        validar hasta que todos los datos fueron cargados.

        Las validaciones que se hacen en esta función son:
        - Que la lista de aulas dobles no tenga aulas sin seleccionar.
        - (Puede ser que después se agreguen otras)
        
        :return: Un string con la descripción del primer problema, o `None` si
        no hay ningún problema.
        '''
        for edificio in self._edificios:
            for aula_doble in edificio.aulas_dobles:
                if aula_no_seleccionada in (aula_doble.aula_grande, aula_doble.aula_chica_1, aula_doble.aula_chica_2):
                    return f'En el edificio {edificio.nombre} falta seleccionar una componente de aula doble.'
        
        return None

    def asignar_aulas(self) -> InfoPostAsignación:
        '''
        Asignar aulas a todas las clases que no tengan una asignación forzada.

        :return: Info sobre el resultado de la asignación.
        '''
        return asignar(self._edificios, self._carreras)

    def importar_clases_de_excel(self, path: str, confirmación_de_sobreescritura: Callable[[list[str]], bool]):
        '''
        Leer datos de carreras, materias y clases de un archivo excel e
        incorporarlos a la base de datos.

        Las clases/materias/carreras que estén definidas en el archivo y que no
        existan en la base de datos, se agregan. Las que ya existan, se
        actualizan con los nuevos datos (los datos presentes en el excel se
        sobreescriben, los datos no presentes en el excel -como el equipamiento
        requerido- se dejan como estaban).

        :param path: El path absoluto del archivo.
        :param confirmación_de_sobreescritura: Una función para preguntarle al
        usuario si quiere sobreescribir datos. La función recibe una lista de
        nombres de carreras en las que se sobreescribirán datos, y devuelve un
        `bool`. Si devuelve `True` se continúa con la operación; si devuelve
        `False` se cancela la operación sin hacer ningún cambio en la base de
        datos.

        :raise FileNotFoundError: Si el archivo no existe.
        :raise ExcelInválidoException: Si el formato del archivo no es correcto.
        :raise DatoInválidoException: Si el archivo contiene un dato inválido.
        '''
        # Nota: Este método debería llamar a archivos_excel.clases.importar,
        # y actualizar la base de datos con el resultado.
        # (El módulo archivos_excel todavía no existe, ver Issue #52)
        pass

    def exportar_clases_a_excel(self, path: str, carrera: str|None = None):
        '''
        Escribir los datos de las clases (incluyendo la asignación de aulas) en
        un archivo excel.

        Si se especifica el nombre de una carrera, se exportan solamente las
        clases de esa carrera. Si no se especifica el nombre de una carrera, se
        exportan los datos de todas las carreras, una en cada hoja del archivo.

        :param path: El path absoluto del archivo.
        :param carrera: El nombre de una carrera, o `None`.

        :raise ValueError: Si `carrera` no es `None` y no es el nombre de una
        carrera que existe.
        :raise TBD: Si no se puede escribir el archivo en el path dado.
        '''
        # Nota: Este método debería llamar a archivos_excel.clases.exportar.
        # (El módulo archivos_excel todavía no existe, ver Issue #74)
        pass

    def exportar_cronograma_de_edificios_a_excel(self, path: str, edificio: str|None = None):
        '''
        Generar un archivo excel con el cronograma de cada aula en formato de
        línea de tiempo.

        Si se especifica el nombre de un edificio, se genera solamente el
        cronograma de ese edificio. Si no se especifica el nombre de un
        edificio, se generan los cronogramas de todos los edificios, uno en cada
        hoja del archivo.

        :param path: El path absoluto del archivo.
        :param edificio: El nombre de un edificio, o `None`.

        :raise ValueError: Si `edificio` no es `None` y no es el nombre de un
        edificio que existe.
        :raise TBD: Si no se puede escribir el archivo en el path dado.
        '''
        # Nota: Este método debería llamar a archivos_excel.cronograma.exportar.
        # (El módulo archivos_excel todavía no existe, ver Issue #75)
        pass

def _generar_nombre_no_existente(base: str, nombres_existentes: Sequence[str]) -> str:
    '''
    :return: Un nombre que contenga `base` y que no esté en la lista de nombres
    existentes.
    '''
    nombre_propuesto: str = base
    i = 0
    while nombre_propuesto in nombres_existentes:
        i += 1
        nombre_propuesto = f'{base} {i}'
    
    return nombre_propuesto
