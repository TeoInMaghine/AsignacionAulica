# -*- coding: utf-8 -*-
"""
Apartado de configuración para el input y output de datos de las Aulas Dobles
de la Universidad.

@author: Cristian
"""

import flet as ft
from pandas import DataFrame

from typing import List

from .datos import limpiar_texto, generar_tabla, limpiar_espacios_texto
from .alertas import VentanaAlerta


class UI_Config_Aulas_Dobles():
    """
    Apartado de Aulas Dobles o extensibles de la universidad.
    """
    def alertar(self, mensaje: str):
        """
        Crea y muestra una ventana con un mensaje de alerta para el usuario y
        un botón de "Aceptar".

        Parameters
        ----------
        mensaje : str
            Mensaje a alertar al usuario. Por ejemplo: "Error al agregar carrera."

        Returns
        -------
        None.

        """
        VentanaAlerta(self.ui_config.page, mensaje)
        
    def desvincular_primero(self, e):
        """
        Funcion "handler" para el click del botón "Desvincular aula".
        
        Destruye la vinculación entre dos aulas (rompe el aula doble).
        
        Actualiza el estado del aula seleccionada y los elementos ligados.

        Returns
        -------
        None.

        """
        # TODO
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aula: str = str(self.lista_aulas_primero.value or "")
        
        print(f"Desvincular: Aula {nombre_aula} de Edificio {nombre_edificio}")
    
        try:
            # Se desvincula el aula de su otra aula ligada de la "base de
            # datos". (termina desvinculando ambas aulas en resultado)
            # self.ui_config.universidad.desvincular_aula_doble(nombre_edificio, nombre_aula)
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def desvincular_segundo(self, e):
        """
        Funcion "handler" para el click del botón "Desvincular aula".
        
        Destruye la vinculación entre dos aulas (rompe el aula doble).
        
        Actualiza el estado del aula seleccionada y los elementos ligados.

        Returns
        -------
        None.

        """
        # TODO
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aula: str = str(self.lista_aulas_segundo.value or "")
        
        print(f"Desvincular: Aula {nombre_aula} de Edificio {nombre_edificio}")
    
        try:
            # Se desvincula el aula de su otra aula ligada de la "base de
            # datos". (termina desvinculando ambas aulas en resultado)
            # self.ui_config.universidad.desvincular_aula_doble(nombre_edificio, nombre_aula)
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def crear_vinculacion(self, e):
        
        """
        Funcion "handler" para el click del botón "Crear vinculación entre las
        aulas seleccionadas".
        
        Crea un Aula "Doble", haciendo la vinculación entre las dos aulas
        seleccionadas.
        
        Actualiza el estado del aula seleccionada y los elementos ligados.

        Returns
        -------
        None.

        """
        # TODO
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aula_primero: str = str(self.lista_aulas_primero.value or "")
        nombre_aula_segundo: str = str(self.lista_aulas_segundo.value or "")
        
        print(f"Vinculacion: Edificio {nombre_edificio}, {nombre_aula_primero} -> {nombre_aula_segundo}")
    
        try:
            # Se vinculan las dos aulas para un Aula Doble en la "base de
            # datos".
            # self.ui_config.universidad.crear_aula_doble(
            #     nombre_edificio,
            #     nombre_aula_primero, nombre_aula_segundo
            # )
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def seleccionar_edificio(self, e):
        """
        Funcion "handler" al seleccionar un edificio.
        
        Carga en las listas de selección de aulas, las aulas disponibles para
        el edificio seleccionado.

        Returns
        -------
        None.

        """
        # Carga los datos de las aulas.
        self.cargar_datos_aulas()
        
        # Limpia las listas de aulas.
        self.lista_aulas_primero.value = ""
        self.lista_aulas_segundo.value = ""
    
        # Se actualizan los elementos de la interfaz.
        self.actualizar_todo()
    
    def seleccionar_aulas(self, e):
        """
        Funcion "handler" al seleccionar un aula.
        
        Verifica si el aula es doble y actualiza los elementos
        correspondientes.

        Returns
        -------
        None.

        """
        # Se actualizan los elementos de la interfaz.
        self.actualizar_verificaciones_aulas()
    
    def __init__(
            self,
            ui_config
            ):
        """
        Crea el apartado de aulas de los aulas dobles o "extensibles" de la
        universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Aulas "Dobles" de la Universidad"
        1) Dropdown de edificios
        2) 1: Drop. Aulas - Btn. Desvincular aula - Titulo (Es o no aula doble)
        3) 2: Drop. Aulas - Btn. Desvincular aula - Titulo (Es o no aula doble)
        4) Btn. Crear vinculación entre aulas seleccionadas
        5) ----- (linea divisora) -----
        6) Tabla con datos de las aulas que son dobles
        
        Parameters
        ----------
        ui_config : UI_Config
            Referencia al contenedor "padre" de todos los demás apartados.

        Returns
        -------
        None.

        """
        self.ui_config = ui_config
        
        self.aula_primero_vinculada = False
        self.aula_segundo_vinculada = False
        
        # Fila 0:
        # 0) Título: "Configuración de Aulas "Dobles" de la Universidad"
        self.titulo = ft.Text(
            value="Configuración de Aulas \"Dobles\" de la Universidad",
            size=20,
            selectable=False
        )
        # Fila 0+:
        # 0+) Descripción de aula doble
        texto_descripcion = "Un Aula \"Doble\" es una composición de dos aulas, unidas por una\n"
        texto_descripcion+= "pared que puede ser retraída para unirlas y obtener un espacio más\n"
        texto_descripcion+= "amplio para los alumnos. En la Sede ANDINA, dentro del edificio\n"
        texto_descripcion+= "Anasagasti, se encuentra el ejemplo para este caso."
        self.descripcion = ft.Text(
            value=texto_descripcion,
            size=16,
            selectable=False
        )
        # Fila 1:
        # 1) Dropdown de edificios
        self.lista_edificios = self.crear_lista_edificios()
        
        # Fila 2:
        # 2) 1: Drop. Aulas - Btn. Desvincular aula - Titulo (Es o no aula doble)
        self.titulo_1 = ft.Text(
            value="1:",
            size=20,
            selectable=False
        )
        self.lista_aulas_primero = self.crear_lista_aulas()
        self.boton_desvincular_primero = ft.Button(
            text="Desvincular aula"
        )
        self.titulo_aula_primero = self.crear_titulo_aula_primero()
        
        # Fila 3:
        # 3) 2: Drop. Aulas - Btn. Desvincular aula - Titulo (Es o no aula doble)
        self.titulo_2 = ft.Text(
            value="2:",
            size=20,
            selectable=False
        )
        self.lista_aulas_segundo = self.crear_lista_aulas()
        self.boton_desvincular_segundo = ft.Button(
            text="Desvincular aula"
        )
        self.titulo_aula_segundo = self.crear_titulo_aula_segundo()
        
        # Fila 4:
        # 4) Btn. Crear vinculación entre aulas seleccionadas
        self.boton_crear_vinculacion = ft.Button(
            text="Crear vinculación entre las aulas seleccionadas"
        )
        
        # Fila 5:
        # 5) ----- (linea divisora) -----
        self.linea = self.crear_linea()
        
        # Fila 6:
        # 6) Tabla con datos de las aulas que son dobles
        self.tabla = self.crear_tabla()
        
        # Carga inicial de los datos:
        self.cargar_datos_inicio()
        
        self.actualizar_handlers()
        self.actualizar_filas()
        
    def cargar_datos_edificios(self):
        """
        Carga los datos para la lista de selección de edificios.
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # Se cargan todos los nombres de los edificios.
        opciones_edificios: List[ft.dropdown.Option] = []
        for edificio in self.ui_config.universidad.nombres_edificios():
            opciones_edificios.append(ft.dropdown.Option(str(edificio)))
        self.lista_edificios = self.crear_lista_edificios()
        self.lista_edificios.options = opciones_edificios
        
    def cargar_datos_aulas(self):
        """
        Carga los datos para las listas de selección de aulas.
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO juan
        # Se toma el valor seleccionado para el edificio, y mostrar solamente
        # aquellas que estén disponibles en ese edificio.
        edificio_seleccionado: str = str(self.lista_edificios.value or "")
        
        opciones_aulas: List[ft.dropdown.Option] = []
        # for aula in self.ui_config.universidad.funcion(edificio_seleccionado):
        #     opciones_aulas.append(ft.dropdown.Option(str(aula)))
        self.lista_aulas_primero.options = opciones_aulas
        self.lista_aulas_segundo.options = opciones_aulas
    
    def cargar_datos_tabla(self):
        """
        Carga los datos para la tabla.
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        # self.tabla = generar_tabla(self.ui_config.universidad.mostrar_aulas_dobles())
        pass
    
    def cargar_datos_inicio(self):
        """
        Carga TODOS los datos de TODOS los elementos disponibles en el
        apartado.
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        self.cargar_datos_edificios()
        self.cargar_datos_aulas()
        self.cargar_datos_tabla()
    
    def crear_lista_edificios(self) -> ft.Dropdown:
        """
        Crea una lista para la selección de edificio.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de edificio.

        """
        dropdown = ft.Dropdown(
            label="Edificio",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=400,
        )
        return dropdown
    
    def crear_lista_aulas(self) -> ft.Dropdown:
        """
        Crea una lista para la selección de aula.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de aula.

        """
        dropdown = ft.Dropdown(
            label="Aula",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=400,
        )
        return dropdown
    
    def crear_titulo_aula_primero(self) -> ft.Text:
        """
        Crea un titulo que le muestra al usuario si el aula está vinculada a
        otra aula.

        Returns
        -------
        text : ft.Text
            Texto que dice si está vinculada y a qué aula.

        """
        # TODO
        aula_seleccionada: str = str(self.lista_aulas_primero.value or "")
        
        text = ft.Text(
            value="Esta aula no está vinculada a ningúna otra",
            size=20,
            selectable=False
        )
        
        # if self.aula_primero_vinculada:
        #     aula_vinculada: str = self.ui_config.universidad.buscar_vinculacion_de_aula(aula_seleccionada)
            
        #     text = ft.Text(
        #         value=f"Esta aula está vinculada a: {aula_vinculada}",
        #         size=20,
        #         selectable=False
        #     )
        
        return text
    
    def crear_titulo_aula_segundo(self) -> ft.Text:
        """
        Crea un titulo que le muestra al usuario si el aula está vinculada a
        otra aula.

        Returns
        -------
        text : ft.Text
            Texto que dice si está vinculada y a qué aula.

        """
        # TODO
        aula_seleccionada: str = str(self.lista_aulas_segundo.value or "")
        
        text = ft.Text(
            value="Esta aula no está vinculada a ningúna otra",
            size=20,
            selectable=False
        )
        
        # if self.aula_segundo_vinculada:
        #     aula_vinculada: str = self.ui_config.universidad.buscar_vinculacion_de_aula(aula_seleccionada)
            
        #     text = ft.Text(
        #         value=f"Esta aula está vinculada a: {aula_vinculada}",
        #         size=20,
        #         selectable=False
        #     )
        
        return text
    
    def crear_linea(self) -> ft.Divider:
        """
        Crea un elemento línea separadora para la interfaz.

        Returns
        -------
        divider : ft.Divider
            Línea separadora.

        """
        divider = ft.Divider(
            thickness=1
        )
        return divider
    
    def crear_tabla(self):
        """
        Crea el elemento tabla para la interfaz.
        Nota: esta función no carga los datos que debe tener, simplemente crea
        el elemento para luego añadirle sus datos.

        Returns
        -------
        ft.DataTable
            Tabla del apartado actual.

        """
        # TODO FIJARSE COMO ES MEJOR MOSTRAR LA TABLA
        data = {
            "Aula original": [],
            "Aula extendible a": [],
        }
        df = DataFrame(data)
        return generar_tabla(df)
    
    def actualizar_handlers(self):
        """
        Actualiza, define o establece las funciones "handlers" encargadas del
        comportamiento de cada botón.

        Returns
        -------
        None.

        """
        # TODO (descomentar)
        # Define el comportamiento "on_click" de cada elemento.
        self.boton_desvincular_primero.on_click = self.desvincular_primero
        self.boton_desvincular_segundo.on_click = self.desvincular_segundo
        self.boton_crear_vinculacion.on_click = self.crear_vinculacion
        
        # Define el comportamiento "on_change" de cada elemento (listas).
        self.lista_edificios.on_change = self.seleccionar_edificio
        self.lista_aulas_primero.on_change = self.seleccionar_aulas
        self.lista_aulas_segundo.on_change = self.seleccionar_aulas
    
    def actualizar_verificaciones_aulas(self):
        """
        Actualiza los elementos de verificación de vinculación de cada aula
        seleccionada.

        Returns
        -------
        None.

        """
        # TODO
        self.titulo_aula_primero = self.crear_titulo_aula_primero()
        self.titulo_aula_segundo = self.crear_titulo_aula_segundo()
        
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def actualizar_filas(self):
        """
        Agrega o actualiza todas las filas del layout del apartado actual.

        Returns
        -------
        None.

        """
        self.fila: List[ft.Row] = []
        
        # Agrega todas las filas a la columna resultado.
        self.fila.append(ft.Row([self.titulo]))
        self.fila.append(ft.Row([self.descripcion]))
        self.fila.append(ft.Row([self.lista_edificios]))
        
        if self.aula_primero_vinculada:
            self.fila.append(ft.Row([self.titulo_1, self.lista_aulas_primero, self.boton_desvincular_primero, self.titulo_aula_primero]))
        else:
            self.fila.append(ft.Row([self.titulo_1, self.lista_aulas_primero, self.titulo_aula_primero]))
        
        if self.aula_segundo_vinculada:
            self.fila.append(ft.Row([self.titulo_2, self.lista_aulas_segundo, self.boton_desvincular_segundo, self.titulo_aula_segundo]))
        else:
            self.fila.append(ft.Row([self.titulo_2, self.lista_aulas_segundo, self.titulo_aula_segundo]))
        
        self.fila.append(ft.Row([self.boton_crear_vinculacion]))
        self.fila.append(ft.Row([self.tabla]))
        
        # Columna final con todas las filas creadas.
        self.columna = ft.Column(
            controls=self.fila,
            alignment=ft.alignment.top_left,
        )
        self.container = ft.Container(
            content=self.columna,
            alignment=ft.alignment.top_left,
        )
        
    
    def actualizar_lista_aulas(self):
        """
        Actualiza la lista de edificios en la interfaz.

        Returns
        -------
        None.

        """
        # Se cargan todos los nombres de las aulas para el edificio
        # seleccionado.
        self.cargar_datos_aulas()
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def actualizar_lista_edificios(self):
        """
        Actualiza la lista de edificios en la interfaz.

        Returns
        -------
        None.

        """
        # Se cargan todos los nombres de los edificios.
        self.cargar_datos_edificios()
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def actualizar_tabla(self):
        """
        Actualiza la tabla con los datos cargados.

        Returns
        -------
        None.

        """
        # Se cargan todos los datos del apartado para la tabla.
        self.cargar_datos_tabla()
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def actualizar_todo(self):
        """
        Actualiza todos los elementos del apartado, INCLUYENDO los datos que
        contienen.

        Returns
        -------
        None.

        """
        # Actualiza los datos de todos los elementos.
        self.cargar_datos_inicio()
        
        # Actualiza los elementos de la interfaz.
        # self.actualizar_filas()
        # self.actualizar_apartado()
        self.actualizar_verificaciones_aulas()
    
    def actualizar_apartado(self):
        """
        Actualiza los elementos de la interfaz.

        Returns
        -------
        None.

        """
        self.ui_config.actualizar_apartado()
    
    def dibujar(self) -> ft.Container:
        return self.container
