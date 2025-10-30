from itertools import filterfalse
from typing import Callable, Any
from collections import Counter

from asignacion_aulica.gestor_de_datos.entidades import (
    Aula,
    AulaDoble,
    Carrera,
    Edificio,
    fieldnames_Aula,
    fieldnames_AulaDoble,
    fieldnames_Edificio,
    fieldtypes_Aula,
    fieldtypes_Edificio
)

aula_no_seleccionada: Aula = Aula(nombre='Seleccionar', edificio=None, capacidad=0)
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
    '''

    def __init__(self, path_base_de_datos: str|None = None):
        '''
        :param path_base_de_datos: El path absoluto del archivo de la base de
        datos. Si el archivo no existe, es creado. ``None`` para no guardar
        datos.
        '''
        self._edificios: list[Edificio] = []
        self._carreras: list[Carrera] = []
        self._equipamientos: Counter[str] = Counter()

    def get_edificios(self) -> list[str]:
        '''
        :return: Los nombres de todos los edificios en la base de datos,
        ordenados alfabéticamente.
        '''
        nombres = [edificio.nombre for edificio in self._edificios]
        nombres.sort()
        return nombres

    def cantidad_de_edificios(self) -> int:
        return len(self._edificios)

    def get_from_edificio(self, edificio: int, campo: int) -> Any:
        '''
        :param edificio: El índice de un edificio.
        :param campo: El índice de un campo.
        :return: El valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        field_name: str = fieldnames_Edificio[campo]
        return getattr(self._edificios[edificio], field_name)

    def existe_edificio(self, nombre: str) -> bool:
        '''
        :return: `True` si hay un edificio con ese nombre en la base de datos,
        `False` si no.
        '''
        return any(edificio.nombre == nombre for edificio in self._edificios)

    def set_in_edificio(self, edificio: int, campo: int, valor: Any):
        '''
        Actualizar el valor de un campo de un edificio existente.

        El valor dado se asume como válido.

        :param edificio: El índice del edificio.
        :param campo: El índice del campo.
        :param valor: El nuevo valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        :raise TypeError: Si el tipo de ``valor`` no es correcto.
        '''
        el_edificio = self._edificios[edificio]
        field_name: str = fieldnames_Edificio[campo]
        expected_type = fieldtypes_Edificio[campo]
        if isinstance(valor, expected_type):
            setattr(el_edificio, field_name, valor)
        else:
            raise TypeError(f'No se puede asignar un objeto de tipo {type(valor)} al campo "Edificio.{field_name}" de tipo {expected_type}')

    def add_edificio(self):
        '''
        Añadir un nuevo edificio después del último índice existente.

        Se inicializa con valores por defecto, asegurando que tenga un nombre
        único.
        '''
        nombres_existentes = [edificio.nombre for edificio in self._edificios]
        nombre_propuesto = 'Edificio sin nombre'
        i = 0
        while nombre_propuesto in nombres_existentes:
            i += 1
            nombre_propuesto = f'Edificio sin nombre {i}'
        self._edificios.append(Edificio(nombre_propuesto))

    def borrar_edificio(self, índice: int):
        '''
        Borrar de la base de datos el edificio en el índice dado.

        :raise IndexError: Si el índice está fuera de rango.
        '''
        del self._edificios[índice]

    def ordenar_edificios(self):
        '''
        Ordena los edificios alfabéticamente.
        '''
        self._edificios.sort(key=lambda edificio: edificio.nombre)

    def cantidad_de_aulas(self, edificio: int) -> int:
        '''
        :return: La cantidad de aulas de un edificio en la base de datos.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        return len(self._edificios[edificio].aulas)

    def get_aulas(self, edificio: int) -> list[str]:
        '''
        :return: Los nombres de todas las aulas de un edificio en la base de
        datos, ordenados alfabéticamente.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        nombres = [aula.nombre for aula in self._edificios[edificio].aulas]
        nombres.sort()
        return nombres

    def get_from_aula(self, edificio: int, índice: int, campo: int) -> Any:
        '''
        :param edificio: El índice del edificio.
        :param índice: El índice del aula.
        :param campo: El índice del campo.
        :return: El valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        fieldname = fieldnames_Aula[campo]
        return getattr(self._edificios[edificio].aulas[índice], fieldname)

    def set_in_aula(self, edificio: int, índice: int, campo: int, valor: Any):
        '''
        Actualizar el valor de un campo de un aula existente.

        El valor dado se asume como válido.

        :param edificio: El índice del edificio.
        :param índice: El índice del aula.
        :param campo: El índice del campo.
        :param valor: El nuevo valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        :raise TypeError: Si el tipo de ``valor`` no es correcto.
        '''
        el_aula = self._edificios[edificio].aulas[índice]
        field_name: str = fieldnames_Aula[campo]
        expected_type = fieldtypes_Aula[campo]
        if isinstance(valor, expected_type):
            setattr(el_aula, field_name, valor)
        else:
            raise TypeError(f'No se puede asignar un objeto de tipo {type(valor)} al campo "Aula.{field_name}" de tipo {expected_type}')

    def add_aula(self, edificio: int):
        '''
        Añadir al edificio un nuevo aula, después del último índice existente.

        Se inicializa con valores por defecto, asegurando que tenga un nombre
        único.

        :param edificio: El índice del edificio.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        el_edificio = self._edificios[edificio]
        nombres_existentes = [aula.nombre for aula in el_edificio.aulas]
        nombre_propuesto = 'Aula sin nombre'
        i = 0
        while nombre_propuesto in nombres_existentes:
            i += 1
            nombre_propuesto = f'Aula sin nombre {i}'
        
        el_edificio.aulas.append(Aula(
            nombre = nombre_propuesto,
            edificio = el_edificio,
            capacidad = 1
        ))

    def existe_aula(self, edificio: int, nombre: str) -> bool:
        '''
        :return: `True` si el aula especificada existe en la base de datos,
        `False` si no.

        :param edificio: El índice del edificio.
        :param nombre: El nombre del aula.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        el_edificio = self._edificios[edificio]
        return any(aula.nombre == nombre for aula in el_edificio.aulas)

    def borrar_aula(self, edificio: int, índice: int):
        '''
        Borrar de la base de datos el aula especificada.

        :param edificio: El índice del edificio.
        :param índice: El índice del aula.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        el_edificio = self._edificios[edificio]

        # Sacar el aula de la lista
        aula = el_edificio.aulas.pop(índice)
        
        # Borrar aulas dobles que usen este aula
        el_edificio.aulas_dobles[:] = filterfalse(
            lambda ad: ad.aula_grande is aula or ad.aula_chica_1 is aula or ad.aula_chica_2 is aula,
            el_edificio.aulas_dobles
        )

    def ordenar_aulas(self, edificio: int):
        '''
        Ordena alfabéticamente las aulas del edificio especificado.

        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        self._edificios[edificio].aulas.sort(key=lambda aula: aula.nombre)

    def cantidad_de_aulas_dobles(self, edificio: int) -> int:
        '''
        :return: La cantidad de aulas dobles de un edificio en la base de datos.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        return len(self._edificios[edificio].aulas_dobles)

    def get_from_aula_doble(self, edificio: int, aula_doble: int, campo: int) -> Any:
        '''
        :param edificio: El índice del edificio.
        :param aula_doble: El índice del aula doble.
        :param campo: El índice del campo.
        :return: El valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        fieldname = fieldnames_AulaDoble[campo]
        return getattr(self._edificios[edificio].aulas_dobles[aula_doble], fieldname)

    def set_in_aula_doble(self, edificio: int, aula_doble: int, campo: int, valor: Aula):
        '''
        Actualizar el valor de un campo de un aula doble existente.

        El valor dado se asume como válido.

        :param edificio: El índice del edificio.
        :param aula_doble: El índice del aula doble.
        :param campo: El índice del campo.
        :param valor: El nuevo valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        :raise TypeError: Si el tipo de ``valor`` no es correcto.
        '''
        el_aula_doble = self._edificios[edificio].aulas_dobles[aula_doble]
        field_name: str = fieldnames_AulaDoble[campo]
        if isinstance(valor, Aula):
            setattr(el_aula_doble, field_name, valor)
        else:
            raise TypeError(f'No se puede asignar un objeto de tipo {type(valor)} al campo "AulaDoble.{field_name}" de tipo {expected_type}')

    def add_aula_doble(self, edificio: int):
        '''
        Añadir al edificio un nuevo aula doble, después del último índice
        existente.

        :param edificio: El índice del edificio.
        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        self._edificios[edificio].aulas_dobles.append(AulaDoble(
            aula_no_seleccionada, aula_no_seleccionada, aula_no_seleccionada
        ))

    def borrar_aula_doble(self, edificio: int, índice: int):
        '''
        Borrar de la base de datos el aula doble especificada.

        :param edificio: El índice del edificio.
        :param índice: El índice del aula doble.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        del self._edificios[edificio].aulas_dobles[índice]

    def ordenar_aulas_dobles(self, edificio: int):
        '''
        Ordena las aulas dobles del edificio especificado, por orden alfabético
        de los nombres de las aulas grandes.

        :raise IndexError: Si el índice del edificio está fuera de rango.
        '''
        self._edificios[edificio].aulas_dobles.sort(key=lambda aula_doble: aula_doble.aula_grande.nombre)

    def get_carreras(self) -> list[str]:
        '''
        :return: Los nombres de todas las carreras en la base de
        datos, ordenadas alfabéticamente.
        '''
        pass

    def get_carrera(self, índice: int) -> Carrera:
        '''
        :return: La carrera con el índice dado.
        :raise IndexError: Si el índice está fuera de rango.
        '''
        pass
    
    def existe_carrera(self, nombre: str) -> bool:
        '''
        :return: `True` si hay una carrera con ese nombre, `False` si no.
        '''
        pass

    def set_carrera_nombre(self, índice: int, nombre: str) -> int:
        '''
        Renombrar una carrera existente.

        :return: El nuevo índice de la carrera.
        :raise IndexError: Si el índice está fuera de rango.
        :raise ValueError: Si ya existe una carrera con el nombre dado.
        '''
        pass

    def set_carrera_edificio_preferido(self, índice: int, edificio: str|None):
        '''
        Cambiar el edificio preferido de una carrera existente.

        :param índice: El índice de la carrera.
        :param edificio: El nombre del nuevo edificio preferido, o None para que
        no tenga preferencia.

        :raise IndexError: Si el índice está fuera de rango.
        :raise ValueError: Si no existe un edificio con el nombre dado.
        '''
        pass

    def borrar_carrera(self, índice: int):
        '''
        Borrar una carrera de la base de datos.

        :raise IndexError: Si el índice está fuera de rango.
        '''
        pass

    def cantidad_de_materias(self, carrera: int) -> int:
        '''
        :param carrera: El índice de la carrera.
        '''
        pass

    def get_from_materia(self, carrera: int, materia: int, campo: int) -> Any:
        '''
        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param campo: El índice del campo.
        :return: El valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def existe_materia(self, carrera: int, nombre: str) -> bool:
        '''
        :return: `True` si la materia especificada existe en la base de datos,
        `False` si no.

        :param carrera: El índice de la carrera.
        :param nombre: El nombre de la materia a buscar.
        :raise IndexError: Si el índice de la carrera está fuera de rango.
        '''
        pass

    def set_in_materia(self, carrera: int, materia: int, campo: int, valor: Any):
        '''
        Actualizar el valor de un campo de un materia existente.

        El valor dado se asume como válido.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param campo: El índice del campo.
        :param valor: El nuevo valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def add_materia(self, carrera: int):
        '''
        Añadir a una carrera una nueva materia, después del último índice
        existente.

        Se inicializa con valores por defecto, asegurando que tenga un nombre
        único.

        :param carrera: El índice de la carrera.
        :raise IndexError: Si el índice de la carrera está fuera de rango.
        '''
        pass

    def borrar_materia(self, carrera: int, materia: int):
        '''
        Borrar la materia especificada de la base de datos.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def ordenar_materias(self, carrera: int):
        '''
        Ordena alfabéticamente las materias de la carrera especificada.

        :raise IndexError: Si el índice de la carrera está fuera de rango.
        '''
        pass

    def cantidad_de_clases(self, carrera: int, materia: int) -> int:
        '''
        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :return: la cantidad de clases que tiene la materia especificada.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def get_from_clase(self, carrera: int, materia: int, clase: int, campo: int) -> Any:
        '''
        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param clase: El índice de la clase.
        :param campo: El índice del campo.
        :return: El valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def existe_clase(self, carrera: int, materia: int, nombre: str) -> bool:
        '''
        :return: `True` si la clase especificada existe en la base de datos,
        `False` si no.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param nombre: El nombre de la clase a buscar.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def set_in_clase(self, carrera: int, materia: int, clase: int, campo: int, valor: Any):
        '''
        Actualizar el valor de un campo de una clase existente.

        El valor dado se asume como válido.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param clase: El índice de la clase.
        :param campo: El índice del campo.
        :param valor: El nuevo valor del campo especificado.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def add_clase(self, carrera: int, materia: int):
        '''
        Añadir una nueva clase a una carrera, después del último índice
        existente.

        Se inicializa con valores por defecto.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def borrar_clase(self, carrera: int, materia: int, clase: int):
        '''
        Borrar de la base de datos la clase especificada.

        :param carrera: El índice de la carrera.
        :param materia: El índice de la materia.
        :param clase: El índice de la clase.
        :raise IndexError: Si alguno de los índices está fuera de rango.
        '''
        pass

    def validar_datos(self) -> str|None:
        '''
        Verificar que los datos contenidos en la base de datos sean válidos y
        compatibles entre sí.

        La mayoría de los datos se pueden validar en el momento en el que se
        ingresan, pero hay algunas relaciones entre datos que no se pueden
        validar hasta que todos los datos fueron cargados.

        Las validaciones que se hacen en esta función son:
        - Que la lista de aulas dobles no tenga aulas vacías.
        - Que ningún aula aparezca más de una vez en la lista de aulas dobles.
        - (Puede ser que después se agreguen otras)
        
        :return: Un string con la descripción del primer problema, o `None` si
        no hay ningún problema.
        '''
        pass

    def asignar_aulas(self):
        '''
        Asignar aulas a todas las clases que no tengan una asignación forzada.

        :raise AsignaciónImposibleException: Si no se pueden asignar aulas a
        todas las clases. Al manejar esta excepción, tener en cuenta que se
        pueden haber asignado aulas a algunas clases si y otras no (esta
        información estará contenida en la excepción).
        '''
        # Nota: Este método debería llamar a lógica_de_asignación.asignar,
        # y actualizar la base de datos con el resultado.
        pass

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
