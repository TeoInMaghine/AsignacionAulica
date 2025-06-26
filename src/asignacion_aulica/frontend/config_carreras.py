# -*- coding: utf-8 -*-
"""
Apartado de configuración para el input y output de datos de las Carreras de
la Universidad.

@author: Cristian
"""

import flet as ft
from pandas import DataFrame

from typing import List

from .datos import limpiar_texto, generar_tabla
from .alertas import VentanaAlerta


class UI_Config_Carreras():
    """
    Apartado de Carreras de la universidad.
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
        
    def limpiar_seleccion_carrera(self):
        """
        Limpia la selección de la carrera, quitando la opcion elegida dentro
        del dropdown. (tristemente solamente se puede lograr esto volviendo a
        crear los objetos correspondientes y actualizando el apartado).

        Returns
        -------
        None.

        """
        # Se vuelven a crear los elementos para que estén vacíos en selección.
        self.lista_carreras.value = ""
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
        
    def limpiar_seleccion_edificio(self):
        """
        Limpia la selección del edificio, quitando la opcion elegida dentro del
        dropdown. (tristemente solamente se puede lograr esto volviendo a crear
        los objetos correspondientes y actualizando el apartado).

        Returns
        -------
        None.

        """
        # Se vuelven a crear los elementos para que estén vacíos en selección.
        self.lista_edificios.value = ""
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def agregar_carrera(self, e):
        """
        Función "handler" para el click del botón "Agregar carrera".
        
        Agrega el nombre de la carrera nueva, con un ningún edificio de
        preferencia (valor predeterminado) si no se lo especifica.
        
        Al hacer click, limpia la selección del edificio y del campo de texto,
        para prevenir posibles errores futuros. También selecciona la carrera
        agregada en la lista de carreras.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # Toma el input del usuario.
        nombre_carrera: str = limpiar_texto(str(self.campo_nombre_edificio.value))
        nombre_edificio: str = str(self.lista_edificios.value or "")
        
        print(f"Agregar carrera: {nombre_carrera} con edificio de preferencia: {nombre_edificio}")
        
        try:
            # TODO
            # Se agrega la carrera a la "base de datos".
            # self.ui_config.universidad.agregar_carrera(nombre_carrera, nombre_edificio)
            
            # Si es que no hay ningún problema:
            # Limpia el campo de texto de la carrera.
            self.campo_nombre_carrera = self.crear_campo_nombre_carrera()
            
            # Limpia la lista de selección de carrera y edificio.
            self.limpiar_seleccion_carrera()
            self.limpiar_seleccion_edificio()
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def modificar_carrera(self, e):
        """
        Función "handler" para el click del botón "Modificar carrera".
        
        Modifica el nombre de una carrera ya agregada a "base de datos" del
        programa.
        
        Al hacer click, limpia la selección de la carrera y el campo de texto.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # Toma el input del usuario.
        nombre_carrera: str = str(self.lista_carreras.value or "")
        nuevo_nombre_carrera: str = limpiar_texto(str(self.campo_nombre_carrera.value))
        
        print(f"Modificar carrera: {nombre_carrera} -> {nuevo_nombre_carrera}")
        
        try:
            # TODO
            # Se modifica la carrera en la "base de datos".
            # self.ui_config.universidad.modificar_carrera(
            #     nombre_edificio,
            #     nuevo_nombre_edificio
            # )
        
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del edificio.
            self.campo_nombre_carrera = self.crear_campo_nombre_carrera()
        
            # Limpia la lista de selección de carrera y edificio.
            self.limpiar_seleccion_carrera()
            self.limpiar_seleccion_edificio()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
        
    def eliminar_carrera(self, e):
        """
        Función "handler" para el click del botón "Eliminar carrera".
        
        Elimina una carrera ya agregada a la "base de datos" del programa.
        
        Al hacer click, limpia la selección de la carrera, del edificio y el
        campo de texto.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        nombre_carrera: str = str(self.lista_carreras.value or "")
        
        print(f"Eliminar carrera: {nombre_carrera}")
        
        try:
            # TODO
            # Se elimina la carrera en la "base de datos".
            # self.ui_config.universidad.eliminar_carrera(nombre_carrera)
        
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio = self.crear_campo_nombre_edificio()
        
            # Limpia la lista de selección de carrera y edificio.
            self.limpiar_seleccion_carrera()
            self.limpiar_seleccion_edificio()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
        
    def eliminar_preferencia_edificio(self, e):
        """
        Función "handler" para el click del botón "Eliminar preferencia de
        edificio".
        
        Elimina un edificio asignado a la preferencia para una carrera ya
        agregada a la "base de datos" del programa.
        
        Al hacer click, limpia la selección del edificio.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        nombre_carrera: str = str(self.lista_carreras.value or "")
        
        print(f"Eliminar preferencia de edificio de carrera: {nombre_carrera}")
        
        try:
            # TODO
            # Se elimina la preferencia de edificio de la carrera en la "base
            # de datos".
            # self.ui_config.universidad.eliminar_preferencia_edificio_carrera(nombre_carrera)
        
            # Si es que no hay ningún problema:
            # Limpia la lista de selección de carrera y edificio.
            self.limpiar_seleccion_edificio()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def seleccionar_carrera(self, e):
        """
        Funcion "handler" al seleccionar una carrera.
        
        Limpia el campo de texto del nombre de la carrera al hacer una
        selección de una carrera ya existente (evita que el usuario lo modifique
        accidentalmente). También selecciona automáticamente el edificio de
        preferencia de la carrera seleccionada (si es que tiene uno).

        Returns
        -------
        None.

        """
        # TODO
        # nombre_carrera: str = str(self.lista_carreras.value or "")
        # nombre_edificio: str = self.ui_config.universidad.edificio_preferencia_de_carrera(nombre_carrera)
        
        # if nombre_edificio == "":
        #     # Limpia la lista de selección de edificio.
        #     self.limpiar_seleccion_edificio()
        # else:
        #     # Selecciona automáticamente el edificio que tenía de preferencia.
        #     self.lista_edificios.value = nombre_edificio
    
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()

    def seleccionar_edificio(self, e):
        """
        Funcion "handler" al seleccionar un edificio.
        
        Limpia el campo de texto del nombre del edificio al hacer una selección
        de un edificio ya existente (evita que el usuario lo modifique
        accidentalmente).
    
        Returns
        -------
        None.
    
        """
        # TODO
        # nombre_carrera: str = str(self.lista_carreras.value or "")
        # nombre_edificio: str = self.ui_config.universidad.edificio_preferencia_de_carrera(nombre_carrera)
        
        # if nombre_carrera == "":
        #     self.alertar(
        #         """
        #         Para poder seleccionar y establecer el edificio de preferencia
        #         de una carrera, primero debe seleccionar la carrera al que se
        #         le aplicarán los cambios.
        #         """
        #     )
            
        #     # Limpia la lista de selección de edificio.
        #     self.limpiar_seleccion_edificio()
    
        #     # Se actualizan los elementos de la interfaz.
        #     self.actualizar_filas()
        #     self.actualizar_apartado()
    
    def __init__(
            self,
            ui_config
            ):
        """
        Crea el apartado de aulas de los edificios la universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Carreras de la Universidad"
        1) Dropdown carreras - Botón eliminar carrera    
        2) Campo nombre de carrera - Btn. agregar carrera - Btn. modificar carrera
        3) ----- (linea divisora) -----
        4) Título: "Preferencia de edificio para la carrera"
        5) Drop. edificio preferido para la carrera - Btn. eliminar preferencia
        6) ----- (linea divisora) -----
        7) Tabla con datos de las carreras
        
        Parameters
        ----------
        ui_config : UI_Config
            Referencia al contenedor "padre" de todos los demás apartados.

        Returns
        -------
        None.

        """
        self.ui_config = ui_config
        
        # Fila 0:
        # 0) Título: "Configuración de Carreras de la Universidad"
        self.titulo = ft.Text(
            value="Configuración de Carreras de la Universidad",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown carreras - Botón eliminar carrera
        self.lista_carreras = self.crear_lista_carreras()
        self.boton_eliminar_carrera = ft.Button(
            text="Eliminar carrera"
        )
        
        # Fila 2:
        # 2) Campo nombre de carrera - Btn. agregar carrera - Btn. modificar carrera
        self.campo_nombre_carrera = self.crear_campo_nombre_carrera()
        self.boton_agregar_carrera = ft.Button(
            text="Agregar carrera"
        )
        self.boton_modificar_carrera = ft.Button(
            text="Modificar carrera"
        )
        
        # Fila 3:
        # 3) ----- (linea divisora) -----
        self.linea_0 = self.crear_linea()
        
        # Fila 4:
        # 4) Título: "Preferencia de edificio para la carrera"
        self.titulo_preferencia_edificio = ft.Text(
            value="Preferencia de edificio para la carrera",
            size=20,
            selectable=False
        )
        
        # Fila 5:
        # 5) Drop. edificio preferido para la carrera - Btn. eliminar preferencia
        self.lista_edificios = self.crear_lista_edificios()
        self.boton_eliminar_preferencia = ft.Button(
            text="Eliminar preferencia de edificio"
        )
        
        # Fila 6:
        # 6) ----- (linea divisora) -----
        self.linea_1 = self.crear_linea()
        
        # Fila 7:
        # 7) Tabla con datos de las carreras
        self.tabla = self.crear_tabla()
        
        # Carga inicial de los datos:
        self.cargar_datos_inicio()
        
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
        
        opciones_carreras: List[ft.dropdown.Option] = []
        for carrera in self.ui_config.universidad.nombres_carreras():
            opciones_carreras.append(ft.dropdown.Option(str(carrera)))
        self.lista_carreras = self.crear_lista_carreras()
        self.lista_carreras.options = opciones_carreras
        
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
        # self.tabla = generar_tabla(self.ui_config.universidad.mostrar_carreras())
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
        self.cargar_datos_carreras()
        self.cargar_datos_edificios()
        self.cargar_datos_tabla()
    
    def crear_lista_carreras(self) -> ft.Dropdown:
        """
        Crea una lista para la selección de carreras ya existentes.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de carreras.

        """
        dropdown = ft.Dropdown(
            label="Carrera",
            options=[
                # ft.dropdown.Option("Ingeniería en Computación"),
            ],
            enable_filter=True,
            editable=True,
            menu_height=400,
        )
        return dropdown
    
    def crear_lista_edificios(self) -> ft.Dropdown:
        """
        Crea una lista para la selección de preferencia de edificio.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de preferencia de edificio.

        """
        dropdown = ft.Dropdown(
            label="Edificio",
            options=[
                # ft.dropdown.Option("Anasagasti 2"),
            ],
            enable_filter=True,
            editable=True,
            menu_height=400,
        )
        return dropdown
    
    def crear_campo_nombre_carrera(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso del nombre la carrera
        a crear/agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input del nombre de la carrera.

        """
        textfield = ft.TextField(
            label="Nombre de la carrera",
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
        data = {
            "Carrera": [],
            "Preferencia de Edificio": [],
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
        self.boton_agregar_carrera.on_click = self.agregar_carrera
        self.boton_modificar_carrera.on_click = self.modificar_carrera
        self.boton_eliminar_carrera.on_click = self.eliminar_carrera
        self.boton_eliminar_preferencia.on_click=self.eliminar_preferencia_edificio
        
        # Define el comportamiento "on_change" de cada elemento (listas).
        self.lista_carreras.on_change = self.seleccionar_carrera
        self.lista_edificios.on_change = self.seleccionar_edificio
    
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
        self.fila.append(ft.Row([self.lista_carreras, self.boton_eliminar_carrera]))
        self.fila.append(ft.Row([self.campo_nombre_carrera, self.boton_agregar_carrera, self.boton_modificar_carrera]))
        self.fila.append(ft.Row([self.linea_0]))
        self.fila.append(ft.Row([self.titulo_preferencia_edificio]))
        self.fila.append(ft.Row([self.lista_edificios, self.boton_eliminar_preferencia]))
        self.fila.append(ft.Row([self.linea_1]))
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
    
    def actualizar_lista_carreras(self):
        """
        Actualiza la lista de carreras en la interfaz.

        Returns
        -------
        None.

        """
        # Se cargan todos los nombres de las carreras.
        self.cargar_datos_carreras()
        
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
