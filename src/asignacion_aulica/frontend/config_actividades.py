# -*- coding: utf-8 -*-
"""
Apartado de configuración para el input y output de datos de las Actividades/
Materias de la Universidad.

@author: Cristian
"""

import flet as ft
from pandas import DataFrame

from typing import List

from .datos import limpiar_texto, generar_tabla
from .alertas import VentanaAlerta


class UI_Config_Actividades():
    """
    Apartado de Actividades/Materias de la universidad.
    """
    def alertar(self, mensaje: str):
        """
        Crea y muestra una ventana con un mensaje de alerta para el usuario y
        un botón de "Aceptar".

        Parameters
        ----------
        mensaje : str
            Mensaje a alertar al usuario. Por ejemplo: "Error al agregar edificio."

        Returns
        -------
        None.

        """
        VentanaAlerta(self.ui_config.page, mensaje)
    
    def agregar_actividad(self, e):
        """
        Función "handler" para el click del botón "Agregar actividad".
        
        Agrega todos los datos completados para crear una nueva actividad en la
        "base de datos".
        
        Al hacer click, limpia la selección y todos los campos.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.
    
        Returns
        -------
        None.
    
        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_actividad: str = limpiar_texto(str(self.campo_identificador_actividad))
        nombre_actividad: str = limpiar_texto(str(self.campo_nombre_actividad))
        comision_actividad: str = limpiar_texto(str(self.campo_comision_actividad))
        año_seleccionado: str = str(self.lista_año or "")
        
        try:
            # Se agrega la actividad a la "base de datos".
            # self.ui_config.universidad.agregar_actividad(
            #     carrera_seleccionada,
            #     identificador_actividad,
            #     nombre_actividad,
            #     comision_actividad,
            #     año_seleccionado,
            #     cant_alumnos,
            # )
            
            # Si es que no hay ningún problema:
            # Limpia las selecciones.
            self.lista_identificador_actividad.value = ""
            self.lista_nombre_actividad.value = ""
            self.lista_comision_actividad.value = ""
            self.lista_año.value = ""
            
            # Limpia los campos.
            self.campo_identificador_actividad.value = ""
            self.campo_nombre_actividad.value = ""
            self.campo_comision_actividad.value = ""
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def modificar_actividad(self, e):
        """
        Función "handler" para el click del botón "Modificar actividad".
        
        Modifica todos los datos completados de la actividad seleccionada en
        la "base de datos".
        
        Al hacer click, limpia la selección y todos los campos.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.
    
        Returns
        -------
        None.
    
        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_seleccionado: str = str(self.lista_identificador_actividad.value or "")
        nombre_actividad_seleccionado: str = str(self.lista_nombre_actividad.value or "")
        nombre_comision_seleccionado: str = str(self.lista_comision_actividad.value or "")
        
        identificador_actividad: str = limpiar_texto(str(self.campo_identificador_actividad))
        nombre_actividad: str = limpiar_texto(str(self.campo_nombre_actividad))
        comision_actividad: str = limpiar_texto(str(self.campo_comision_actividad))
        año_seleccionado: str = str(self.lista_año or "")
        
        try:
            # Se modifica la actividad en la "base de datos".
            # self.ui_config.universidad.modificar_actividad(
            #     carrera_seleccionada,
            #     identificador_seleccionado,
            #     nombre_actividad_seleccionado,
            #     nombre_comision_seleccionado,
            #     identificador_actividad,
            #     nombre_actividad,
            #     comision_actividad,
            #     año_seleccionado,
            #     cant_alumnos,
            # )
            
            # Si es que no hay ningún problema:
            # Limpia las selecciones.
            self.lista_identificador_actividad.value = ""
            self.lista_nombre_actividad.value = ""
            self.lista_comision_actividad.value = ""
            self.lista_año.value = ""
            
            # Limpia los campos.
            self.campo_identificador_actividad.value = ""
            self.campo_nombre_actividad.value = ""
            self.campo_comision_actividad.value = ""
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_actividad(self, e):
        """
        Función "handler" para el click del botón "Eliminar actividad".
        
        Elimina una actividad de la "base de datos".
        
        Al hacer click, limpia la selección y todos los campos.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.
    
        Returns
        -------
        None.
    
        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_seleccionado: str = str(self.lista_identificador_actividad.value or "")
        nombre_actividad_seleccionado: str = str(self.lista_nombre_actividad.value or "")
        nombre_comision_seleccionado: str = str(self.lista_comision_actividad.value or "")
        
        try:
            # Se elimina la actividad en la "base de datos".
            # self.ui_config.universidad.agregar_actividad(
            #     carrera_seleccionada,
            #     identificador_seleccionado,
            #     nombre_actividad_seleccionado,
            #     nombre_comision_seleccionado,
            # )
            
            # Si es que no hay ningún problema:
            # Limpia las selecciones.
            self.lista_identificador_actividad.value = ""
            self.lista_nombre_actividad.value = ""
            self.lista_comision_actividad.value = ""
            self.lista_año.value = ""
            
            # Limpia los campos.
            self.campo_identificador_actividad.value = ""
            self.campo_nombre_actividad.value = ""
            self.campo_comision_actividad.value = ""
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    
    def seleccionar_lista(self, e):
        """
        Función "handler" al cambiar de item en una lista o dropdown.
        
        Recarga todos los datos para que se muestren correctamente.

        Returns
        -------
        None.

        """
        self.actualizar_todo()
    
    def __init__(
            self,
            ui_config
            ):
        """
        Crea el apartado de actividades/materias de la universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Actividades/Materias de la Universidad"
        1) Dropdown carrera
        2) Drop. identificador - Drop. nombre actividad - Drop. comisión
        3) Campo identificador - Campo nombre - Campo comisión
        4) Drop. año
        5) Botón agregar actividad - Btn. modificar actividad - Btn. eliminar actividad
        9) ----- (linea divisora) -----
        10) Btn. Mostrar actividades - Btn. Mostrar equipamiento
        11) Tabla con datos de las actividades

        Returns
        -------
        None.

        """
        self.ui_config = ui_config
        
        # Fila 0:
        # 0) Título: "Configuración de Actividades/Materias de la Universidad"
        self.titulo = ft.Text(
            "Configuración de Actividades/Materias de la Universidad",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown carrera
        self.lista_carreras = self.crear_lista_carreras()
        
        # Fila 2:
        # 2) Drop. identificador - Drop. nombre actividad - Drop. comisión - Botón eliminar actividad
        self.lista_identificador_actividad = self.crear_lista_identificador_actividad()
        self.lista_nombre_actividad = self.crear_lista_nombre_actividad()
        self.lista_comision_actividad = self.crear_lista_comision_actividad()
        
        # Fila 3:
        # 3) Campo identificador - Campo nombre - Campo comisión
        self.campo_identificador_actividad = self.crear_campo_identificador_actividad()
        self.campo_nombre_actividad = self.crear_campo_nombre_actividad()
        self.campo_comision_actividad = self.crear_campo_comision_actividad()
        
        # Fila 4:
        # 4) Drop. año - Drop. Cantidad de alumnos
        self.lista_año = self.crear_lista_año()
        
        # Fila 5:
        # 5) Botón agregar actividad - Btn. modificar actividad - Btn.
        self.boton_agregar_actividad = ft.Button(
            text="Agregar actividad",
        )
        self.boton_modificar_actividad = ft.Button(
            text="Modificar actividad",
        )
        self.boton_eliminar_actividad = ft.Button(
            text="Eliminar actividad",
        )
        
        # Fila 6:
        # 6) ----- (linea divisora) -----
        self.linea = self.crear_linea()
        
        # Fila 7:
        # 7) Tabla con datos de las actividades
        self.tabla = self.crear_tabla()
        
        # Carga inicial de todos los datos:
        self.cargar_datos_inicio()
        
        # Se actualizan los handlers para los botones y se agregan las filas
        # para la interfaz.
        self.actualizar_handlers()
        self.actualizar_filas()
    
    def cargar_datos_carreras(self):
        """
        Carga los datos para la lista de selección de carreras.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        opciones_carreras: List[ft.dropdown.Option] = []
        
        # for carrera in self.ui_config.universidad.nombres_carreras():
        #     opciones_carreras.append(ft.dropdown.Option(str(carrera)))
        self.lista_carreras = self.crear_lista_carreras()
        self.lista_carreras.options = opciones_carreras
        
    def cargar_datos_identificador_actividad(self):
        """
        Carga los datos para la lista de selección de identificador de
        actividad.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        
        opciones_identificadores: List[ft.dropdown.Option] = []
        
        # Carga los identificadores disponibles para la carrera seleccionada.
        # En caso de no seleccionar una carrera, que se seleccionen aquellas
        # que no tienen una carrera asignada. (PENSAR)
        # for identificador in self.ui_config.universidad.obtener_identificadores_actividades(carrera_seleccionada):
        #     opciones_identificadores.append(ft.dropdown.Option(str(identificador)))
        
        self.lista_identificador_actividad = self.crear_lista_identificador_actividad()
        self.lista_identificador_actividad.options = opciones_identificadores
    
    def cargar_datos_nombre_actividad(self):
        """
        Carga los datos para la lista de selección de nombres de actividad.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_seleccionado: str = str(self.lista_identificador_actividad.value or "")
        
        opciones_nombres_actividades: List[ft.dropdown.Option] = []
        
        # Carga los nombres de actividades disponibles para la carrera e
        # identificador seleccionados.
        # En caso de no seleccionar una carrera, que se seleccionen aquellas
        # que no tienen una carrera asignada. (PENSAR)
        # for nombre_actividad in self.ui_config.universidad.obtener_nombre_actividad(carrera_seleccionada, identificador_seleccionado):
        #     opciones_nombres_actividades.append(ft.dropdown.Option(str(nombre_actividad)))
        
        self.lista_nombre_actividad = self.crear_lista_nombre_actividad()
        self.lista_nombre_actividad.options = opciones_nombres_actividades
    
    def cargar_datos_comision_actividad(self):
        """
        Carga los datos para la lista de selección de nombres de actividad.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_seleccionado: str = str(self.lista_identificador_actividad.value or "")
        nombre_actividad_seleccionado: str = str(self.lista_nombre_actividad.value or "")
        
        opciones_comisiones_actividades: List[ft.dropdown.Option] = []
        
        # Carga las comisiones de actividades disponibles para la carrera,
        # identificador y nombre seleccionados.
        # for comision in self.ui_config.universidad.obtener_comision_actividad(
        #         carrera_seleccionada, identificador_seleccionado, nombre_actividad_seleccionado
        #         ):
        #     opciones_comisiones_actividades.append(ft.dropdown.Option(str(comision)))
        
        self.lista_comision_actividad = self.crear_lista_comision_actividad()
        self.lista_comision_actividad.options = opciones_comisiones_actividades
    
    def cargar_datos_tabla(self):
        """
        Carga los datos para la tabla, dependiendo de que tabla actual esté
        seleccionada
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO juan
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_seleccionado: str = str(self.lista_identificador_actividad.value or "")
        nombre_seleccionado: str = str(self.lista_nombre_actividad.value or "")
        comision_seleccionado: str = str(self.lista_comision_actividad.value or "")
        
        # match self.tabla_actual:
        #     case TABLA.ACTIVIDADES:
        #         self.tabla = generar_tabla(self.ui_config.universidad.mostrar_actividades())
        #     case TABLA.EQUIPAMIENTO:
        #         self.tabla = generar_tabla(self.ui_config.universidad.mostrar_equipamiento_actividad(
        #                 carrera_seleccionada,
        #                 identificador_seleccionado,
        #                 nombre_seleccionado,
        #                 comision_seleccionado
        #             )
        #         )
        #     case _:
        #         self.tabla = generar_tabla(self.ui_config.universidad.mostrar_actividades())
        self.tabla = generar_tabla(self.ui_config.universidad.mostrar_materias())
    
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
        self.cargar_datos_carreras()
        self.cargar_datos_identificador_actividad()
        self.cargar_datos_nombre_actividad()
        self.cargar_datos_comision_actividad()
        self.cargar_datos_tabla()
    
    def crear_lista_carreras(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso de la carrera.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de carrera.

        """
        dropdown = ft.Dropdown(
            label="Carrera",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=300,
        )
        return dropdown
    
    def crear_lista_identificador_actividad(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso del identificador de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de identificador de actividad.

        """
        dropdown = ft.Dropdown(
            label="Identificador",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=300,
        )
        return dropdown
    
    def crear_lista_nombre_actividad(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso del nombre de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de nombre de actividad.

        """
        dropdown = ft.Dropdown(
            label="Nombre",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=300,
        )
        return dropdown
    
    def crear_lista_comision_actividad(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso de la comisión de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de la comisión de la actividad.

        """
        dropdown = ft.Dropdown(
            label="Comisión",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=200,
        )
        return dropdown
    
    def crear_lista_año(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso del año de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección del año de la actividad.

        """
        dropdown = ft.Dropdown(
            label="Año",
            options=[
                ft.dropdown.Option(f"{i}") for i in range(1, 7, 1)
            ],
            enable_filter=True,
            editable=True,
        )
        return dropdown
    
    def crear_campo_identificador_actividad(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso del identificador de la
        actividad a crear/agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input del identificador de la actividad.

        """
        textfield = ft.TextField(
            label="Identificador de actividad",
        )
        return textfield
    
    def crear_campo_nombre_actividad(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso del nombre de la
        actividad a crear/agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input del nombre de la actividad.

        """
        textfield = ft.TextField(
            label="Nombre de actividad",
        )
        return textfield
    
    def crear_campo_comision_actividad(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso de la comisión de la
        actividad a crear/agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input de la comisión de la actividad.

        """
        textfield = ft.TextField(
            label="Comisión",
        )
        return textfield
    
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
    
    def crear_tabla(self) -> ft.DataTable:
        """
        Crea el elemento tabla para la interfaz.
        Nota: esta función no carga los datos que debe tener, simplemente crea
        el elemento para luego añadirle sus datos.

        Returns
        -------
        ft.DataTable
            Tabla del apartado actual.

        """
        data = {
            "Carrera": [],
            "Identificador": [],
            "Nombre": [],
            "Comisión": [],
            "Año": [],
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
        # Define el comportamiento "on_click" de cada elemento (botones).
        # self.boton_agregar_actividad.on_click = self.agregar_actividad
        # self.boton_modificar_actividad.on_click = self.modificar_actividad
        # self.boton_eliminar_actividad.on_click = self.eliminar_actividad
        # self.boton_mostrar_actividades.on_click = self.mostrar_actividades
        # self.boton_mostrar_equipamiento.on_click = self.mostrar_equipamiento
        
        # Define el comportamiento "on_change" de cada elemento (listas).
        # self.lista_carreras.on_change = self.seleccionar_lista
        # self.lista_identificador_actividad.on_change = self.seleccionar_lista
        # self.lista_nombre_actividad.on_change = self.seleccionar_lista
        # self.lista_comision_actividad.on_change = self.seleccionar_lista
    
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
        self.fila.append(ft.Row([self.lista_carreras]))
        self.fila.append(ft.Row([self.lista_identificador_actividad, self.lista_nombre_actividad, self.lista_comision_actividad]))
        self.fila.append(ft.Row([self.campo_identificador_actividad, self.campo_nombre_actividad, self.campo_comision_actividad]))
        self.fila.append(ft.Row([self.lista_año]))
        self.fila.append(ft.Row([self.boton_agregar_actividad, self.boton_modificar_actividad, self.boton_eliminar_actividad]))
        self.fila.append(ft.Row([self.linea]))
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
        self.actualizar_filas()
        self.actualizar_apartado()
    
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
