from collections.abc import Iterable

from asignacion_aulica.gestor_de_datos.entidades import Aula, Edificio, Carrera, Materia, Clase
from asignacion_aulica.lógica_de_asignación import AsignaciónImposibleException

class GestorDeDatos:
    '''
    Objeto encargado de administrar todos los datos de edificios, aulas, y
    clases.

    Internamente usa una base de datos para almacenar los datos de manera
    persistente.
    '''

    def __init__(self, path_base_de_datos: str):
        '''
        :param path_base_de_datos: El path absoluto del archivo de la base de
        datos. Si el archivo no existe, es creado.
        '''
        pass

    def get_edificios(self) -> Iterable[Edificio]:
        '''
        :return: Un iterable de todos los edificios en la base de datos.
        '''
        pass

    def get_edificio(self, nombre: str) -> Edificio:
        '''
        :return: El edificio con el nombre dado.
        :raise KeyError: Si no existe un edificio con el nombre dado.
        '''
        pass

    def existe_edificio(self, nombre: str) -> bool:
        '''
        :return: `True` si hay un edificio con ese nombre en la base de datos,
        `False` si no.
        '''
        pass

    def set_edificio(self, edificio: Edificio):
        '''
        Actualizar la base de datos con el edificio dado.

        Si ya existe un edificio con el mismo nombre, se sobreescriben sus
        valores. Si no existe un edificio con el mismo nombre, se agrega.

        :raise ValueError: Si el horario de cierre de algún día es más temprano
        que el horario de apertura.
        '''
        pass

    def borrar_edificio(self, nombre: str):
        '''
        Borrar de la base de datos el edificio dado y todas sus aulas.

        :raise KeyError: Si no existe un edificio con el nombre dado.
        '''
        pass

    def get_aulas(self, edificio: str) -> Iterable[Aula]:
        '''
        :return: Un iterable de todas las aulas pertenecientes al edificio dado.
        :raise KeyError: Si no existe un edificio con el nombre dado.
        '''
        pass

    def get_aula(self, edificio: str, nombre: str) -> Aula:
        '''
        :return: El aula con el nombre dado.
        :raise KeyError: Si no existe un aula con el nombre dado en ese
        edificio, o si no existe un edificio con ese nombre.
        '''
        pass

    def existe_aula(self, edificio: str, nombre: str) -> bool:
        '''
        :return: `True` si hay un aula con ese nombre en ese edificio , `False`
        si no.
        :raise KeyError: Si no existe un edificio con ese nombre.
        '''
        pass

    def set_aula(self, aula: Aula):
        '''
        Actualizar la base de datos con el aula dada.

        Si ya existe un aula con el mismo nombre en ese edificio, se
        sobreescriben sus valores. Si no existe un aula con el mismo nombre en
        ese edificio, se agrega.

        :raise KeyError: Si no existe el edificio al que pertenece el aula.
        :raise ValueError: Si la capacidad es negativa, si el horario de cierre
        de algún día es más temprano que el horario de apertura.
        '''
        pass
    
    def borrar_aula(self, edificio: str, nombre: str):
        '''
        Borrar un aula de la base de datos.

        :raise KeyError: Si no existe un aula con el nombre dado en ese
        edificio, o si no existe un edificio con ese nombre.
        '''
        pass

    def get_carreras(self) -> Iterable[Carrera]:
        '''
        :return: Un iterable de todas las carreras en la base de datos.
        '''
        pass

    def get_carrera(self, nombre: str) -> Carrera:
        '''
        :return: La carrera con el nombre dado.
        :raise KeyError: Si no existe una carrera con ese nombre.
        '''
        pass
    
    def existe_carrera(self, nombre: str) -> bool:
        '''
        :return: `True` si hay una carrera con ese nombre, `False` si no.
        '''
        pass

    def set_carrera(self, carrera: Carrera):
        '''
        Actualizar la base de datos con la carrera dada.

        Si ya existe una carrera con el mismo nombre, se sobreescriben sus
        valores. Si no existe una carrera con el mismo nombre, se agrega.

        :raise ValueError: Si `carrera.edificio_preferido` no es `None` y no es
        el nombre de un edificio que existe.
        '''
        pass

    def borrar_carrera(self, nombre: str):
        '''
        Borrar de la base de datos la carrera dada, junto con todas sus materias
        y clases.

        :raise KeyError: Si no existe una carrera con el nombre dado.
        '''
        pass

    def get_materias(self, carrera: str) -> Iterable[Materia]:
        '''
        :return: Un iterable de todas las materias de la carrera dada.
        :raise KeyError: Si no existe una carrera con el nombre dado.
        '''
        pass

    def get_materia(self, carrera: str, nombre: str) -> Materia:
        '''
        :return: La materia con el nombre dado.
        :raise KeyError: Si no existe una materia con el nombre dado en esa
        carrera, o si no existe una carrera con ese nombre.
        '''
        pass

    def existe_materia(self, carrera: str, nombre: str) -> bool:
        '''
        :return: `True` si hay una materia con ese nombre en esa carrera,
        `False` si no.
        :raise KeyError: Si no existe una carrera con ese nombre.
        '''
        pass

    def set_materia(self, materia: Materia):
        '''
        Actualizar la base de datos con la materia.

        Si ya existe una materia con el mismo nombre en la misma carrera, se
        sobreescriben sus valores. Si no existe una materia con el mismo nombre
        en esa carrera, se agrega.

        :raise KeyError: Si `materia.carrera` no es el nombre de una carrera que
        existe.
        :raise ValueError: Si `carrera.año` no es mayor a cero.
        '''
        pass
    
    def borrar_materia(self, carrera: str, nombre: str) -> Materia:
        '''
        Borrar de la base de datos una materia y todas sus clases.

        :raise KeyError: Si no existe una materia con el nombre dado en esa
        carrera, o si no existe una carrera con ese nombre.
        '''
        pass

    def get_clases(self, carrera: str, materia: str) -> Iterable[Clase]:
        '''
        :return: Un iterable de todas las clases de la materia dada.
        :raise KeyError: Si no existe una materia con el nombre dado en la
        carrera dada, o si no existe una carrera con ese nombre.
        '''
        pass

    def get_clase(self, carrera: str, materia: str, id: int) -> Clase:
        '''
        :return: La clase con el id dado.
        :raise KeyError: Si no existe una clase con el id dado en esa materia y
        carrera, o si no existe una carrera o materia con ese nombre.
        '''
        pass

    def nuevo_id_para_clase(self, carrera: str, materia: str) -> int:
        '''
        :return: Un id que actualmente no existe, para una nueva clase en la
        materia dada.
        :raise KeyError: Si no existe una materia con el nombre dado en la
        carrera dada, o si no existe una carrera con ese nombre.
        '''
        pass

    def set_clase(self, clase: Clase):
        '''
        Actualizar la base de datos con la clase dada.

        Si ya existe una clase con el mismo id en la misma materia de la misma
        carrera, se sobreescriben sus valores. Si no, se agrega.
        
        :raise KeyError: Si `clase.carrera` no es el nombre de una carrera que
        existe, o si `clase.materia` no es el nombre de una materia de esa
        carrera.
        :raise ValueError: En los siguientes casos:
        - `clase.horario_fin` es más temprano que `clase.horario_inicio`
        - `clase.cantidad_de_alumnos` es negativo
        - uno de `clase.aula` y `clase.edificio` es `None` y el otro no
        - `clase.edificio` no es `None` y no es el nombre de un edificio que
          existe
        - `clase.aula` no es `None` y no es el nombre de un aula que pertenece a
          ese edificio
        '''
        pass
    
    def borrar_clase(self, carrera: str, materia: str, id: int) -> Clase:
        '''
        Borrar una clase de la base de datos.

        :raise KeyError: Si no existe una clase con el id dado en esa materia y
        carrera, o si no existe una carrera o materia con ese nombre.
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
        - Que el diccionario de aulas dobles de cada edificio contenga aulas que
          existen en ese edificio.
        - (Puede ser que después se agreguen otras)
        
        :return: `None` si está todo bien, un string con la descripción del
        problema si hay algún problema.
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

    def importar_clases_de_excel(self, path: str):
        '''
        Leer datos de carreras, materias y clases de un archivo excel e
        incorporarlos a la base de datos.

        TODO: Decidir si esta acción debería sobreescribir cosas que ya existen
        o tirar una excepción o qué hacer.

        :param path: El path absoluto del archivo.

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
