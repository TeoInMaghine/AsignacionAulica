# -*- coding: utf-8 -*-
"""
Apartados de configuración, inputs y outputs de datos. Incluye:
    - Edificios de la universidad
    - Aulas de los edificios
    - Carreras de la universidad
    - Actividades/materias de la universidad

@author: Cristian
"""

import flet as ft
#from pandas import DataFrame
from typing import List

from .colores import COLOR
from .datos import *


class UI_BotonConfig():
    """
    Botón para cambiar de apartado. Por ejemplo: Edificios, Aulas, ...
    """
    def __init__(
            self,
            config_ref, # UI_Config
            texto: str, # Nombre del botón
            referencia: str # Referencia al nombre del apartado
            ):
        """
        Crea un botón para cambiar de apartado. Ejemplo de apartado: Edificios,
        Aulas, ...

        Parameters
        ----------
        config_ref : UI_Config
            Apartado o contenedor padre con todos los apartados hijos.
        texto : str
            Texto que llevará el botón. Ejemplo: "Edificios".
        referencia : str
            Referencia al nombre "clave" del apartado en cuestión.

        Returns
        -------
        None.

        """
        self.texto: str = texto
        self.config_ref = config_ref
        self.referencia = referencia
        self.tamanio_letra: int = 18
        self.tamanio_alto: int = 36
        
        self.texto_boton = ft.Text(
            value=self.texto,
            color=COLOR.BLANCO,
            text_align=ft.TextAlign.LEFT,
            size=self.tamanio_letra,
            selectable=False,
            )
        self.container_texto = ft.Container(
            content=self.texto_boton,
            alignment=ft.alignment.center_left,
            padding=ft.padding.symmetric(0, 20),
            )
        self.boton = ft.Container(
            content=self.container_texto,
            bgcolor=COLOR.ROJO,
            ink=True,
            on_click=lambda e: self.config_ref.cambiar_apartado(self.referencia), # llama a la función para cambiar de apartado de UI_Config
            height=self.tamanio_alto,
            border_radius=16,
            )
        
    def dibujar(self) -> ft.Container:
        return self.boton


class APARTADO():
    EDIFICIOS = "edificios"
    AULAS = "aulas"
    CARRERAS = "carreras"
    ACTIVIDADES = "actividades"
    HORARIOS = "horarios"

# APARTADOS:

class UI_Config_Edificios():
    """
    Apartado de Edificios de la universidad.
    """
    
    def actualizar_tabla(self):
        pass
    
    def agregar_edificio(self, e):
        nombre_edificio: str = limpiar_texto(self.campo_nombre_edificio.value)
        print(f"Agregar edificio: {nombre_edificio}")

        ### WARNING: ACA NO ESTA INSTANCIADO UNIVERSIDAD. Siempre va a entrar al Exception.
        ### Por ahora puse el Exception porque no tengo separado el archivo con excepciones del universidad.py
        ### Pero esta es la estructura que deberia tener esto.
        # try:
        #   self.ui_config.universidad.TU_FUNCION(...)
        # except excepcion:
        #   mostrar cartelito de alerta
        # finally:
        #   self.actualizar_tabla()
        #
        
    def modificar_edificio(self, e):
        nombre_edificio: str = self.lista_edificios.value or "" # Si es None toma valor ""
        nuevo_nombre_edificio: str = limpiar_texto(self.campo_nombre_edificio.value)
        print(f"Modificar edificio: {nombre_edificio} -> {nuevo_nombre_edificio}")
        
        # try:
        #   self.ui_config.universidad.TU_FUNCION(...)
        # except excepcion:
        #   mostrar cartelito de alerta
        # finally:
        #   self.actualizar_tabla()
        
    def eliminar_edificio(self, e):
        nombre_edificio: str = self.lista_edificios.value or "" # Si es None toma valor ""
        print(f"Eliminar edificio: {nombre_edificio}")
       
        # try:
        #   self.ui_config.universidad.TU_FUNCION(...)
        # except excepcion:
        #   mostrar cartelito de alerta
        # finally:
        #   self.actualizar_tabla()
        
    def establecer_horario(self, e):
        nombre_edificio: str = self.lista_edificios.value or "" # Si es None toma valor ""
        dia: str = self.lista_dias.value or "" # "Miércoles"
        hora_apertura: str = self.lista_hora_apertura.value or "" # "09"
        hora_cierre: str = self.lista_hora_cierre.value or "" # "00"
        minutos_apertura: str = self.lista_minutos_apertura.value or "" # "21"
        minutos_cierre: str = self.lista_minutos_cierre.value or "" # "00"
        
        # "09:00-21:00"
        horario: str = f"{hora_apertura}:{minutos_apertura}-{hora_cierre}:{minutos_cierre}"
        
        print(f"Establecer horario: {dia}, {horario} -> Edificio: {nombre_edificio}")
        
        # try:
        #   self.ui_config.universidad.TU_FUNCION(...)
        # except excepcion:
        #   mostrar cartelito de alerta
        # finally:
        #   self.actualizar_tabla()
    
    def eliminar_horario(self, e):
        nombre_edificio: str = self.lista_edificios.value or "" # Si es None toma valor ""
        dia: str = self.lista_dias.value or "" # Si es None toma valor ""
        print(f"Eliminar horario: {dia} -> Edificio: {nombre_edificio}")
        
        # try:
        #   self.ui_config.universidad.TU_FUNCION(...)
        # except excepcion:
        #   mostrar cartelito de alerta
        # finally:
        #   self.actualizar_tabla()
    
    def seleccionar_edificio(self, e):
        pass
    
    def seleccionar_dia(self, e):
        pass
    
    def seleccionar_hora_apertura(self, e):
        pass
    
    def seleccionar_minutos_apertura(self, e):
        pass
    
    def seleccionar_hora_cierre(self, e):
        pass
    
    def seleccionar_minutos_cierre(self, e):
        pass
    
    def __init__(
            self,
            ui_config
            ):
        """
        Crea el apartado de edificios de la universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Edificios de la Universidad"
        1) Dropdown de edificios - Botón eliminar edificio
        2) Campo nombre edificio - Btn agregar edificio - Btn. modificar edificio
        3) ----- (linea divisora) -----
        4) Título: "Horarios de apertura y cierre"
        5) Drop. con día - Hora apertura - Hora cierre - Btn. agregar horario - Btn. eliminar horario
        6) ----- (linea divisora) -----
        7) Tabla con datos de los edificios cargados

        Returns
        -------
        None.

        """
        
        self.ui_config = ui_config
        
        self.fila: List[ft.Row] = []
        
        # Fila 0:
        # 0) Título: "Configuración de Edificios de la Universidad"
        self.titulo = ft.Text(
            value="Configuración de Edificios de la Universidad",
            text_align=ft.TextAlign.LEFT,
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown de edificios - Botón eliminar edificio
        self.lista_edificios = ft.Dropdown(
            label="Edificios",
            options=[
                ft.dropdown.Option("Anasagasti"),
                ft.dropdown.Option("Mitre"),
            ],
            enable_filter=True,
            enable_search=True
            
        )
        self.boton_eliminar_edificio = ft.Button(
            text="Eliminar edificio",
        )
        
        # Fila 2:
        # 2) Campo nombre edificio - Btn agregar edificio - Btn. modificar edificio
        self.campo_nombre_edificio = ft.TextField(
            label="Nombre del edificio",
        )
        self.boton_agregar_edificio = ft.Button(
            text="Agregar edificio",
        )
        self.boton_modificar_edificio = ft.Button(
            text="Modificar edificio",
        )
        
        # Fila 3: (línea divisora)
        # 3) ----- (linea divisora) -----
        self.linea_0 = ft.Divider(
            thickness=1
        )
        
        # Fila 4:
        # 4) Título: "Horarios de apertura y cierre"
        self.titulo_horarios = ft.Text(
            value="Horarios del Edificio",
            text_align=ft.TextAlign.LEFT,
            size=20,
            selectable=False
        )
        
        # Fila 5:
        # 5) Drop. con día - Hora apertura - Hora cierre - Btn. agregar horario - Btn. eliminar horario
        self.lista_dias = ft.Dropdown(
            label="Día",
            options=[
                ft.dropdown.Option("Lunes"),
                ft.dropdown.Option("Martes"),
                ft.dropdown.Option("Miércoles"),
                ft.dropdown.Option("Jueves"),
                ft.dropdown.Option("Viernes"),
                ft.dropdown.Option("Sábado"),
                ft.dropdown.Option("Domingo")
            ],
            enable_filter=True,
        )
        self.lista_hora_apertura = ft.Dropdown(
            label="Hora",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(24)
            ],
            enable_filter=True,
        )
        self.separador_0 = ft.Text(":")
        self.lista_minutos_apertura = ft.Dropdown(
            label="Minutos",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(0, 60, 5)
            ],
            enable_filter=True,
        )
        self.separador_1 = ft.Text("-")
        self.lista_hora_cierre = ft.Dropdown(
            label="Hora",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(24)
            ],
            enable_filter=True,
        )
        self.separador_2 = ft.Text(":")
        self.lista_minutos_cierre = ft.Dropdown(
            label="Minutos",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(0, 60, 5)
            ],
            enable_filter=True,
        )
        self.boton_establecer_horario = ft.Button(
            text="Establecer horario",
        )
        self.boton_eliminar_horario = ft.Button(
            text="Eliminar horario",
        )
        
        # Fila 6
        # 6) ----- (linea divisora) -----
        self.linea_1 = ft.Divider(
            thickness=1
        )
        
        # Fila 7:
        # 7) Tabla con datos de los edificios cargados
        data = {
            "Nombre del Edificio": ["Mitre", "Anasagasti"],
            "Lunes": ["9:00-18:00", "9:00-18:00"],
            "Martes": ["12:00-21:00", "12:00-21:00"],
            "Miércoles": ["9:00-18:00", "9:00-18:00"],
            "Jueves": ["12:00-21:00", "12:00-21:00"],
            "Viernes": ["9:00-18:00", "9:00-18:00"],
            "Sábado": ["12:00-21:00", "12:00-21:00"],
            "Domingo": ["CERRADO", "CERRADO"],
        }
        # data = {
        #     "Nombre del Edificio": [],
        #     "Lunes": [],
        #     "Martes": [],
        #     "Miércoles": [],
        #     "Jueves": [],
        #     "Viernes": [],
        #     "Sábado": [],
        #     "Domingo": [],
        # }
        df = DataFrame(data)
        self.tabla = crear_tabla(df)
        
        # Define el comportamiento "on_click" de cada elemento.
        self.boton_agregar_edificio.on_click = self.agregar_edificio
        self.boton_eliminar_edificio.on_click = self.eliminar_edificio
        self.boton_modificar_edificio.on_click = self.modificar_edificio
        self.boton_establecer_horario.on_click = self.establecer_horario
        # self.boton_eliminar_horario.on_click = self.eliminar_horario
        # self.lista_edificios.on_change = self.seleccionar_edificio
        # self.lista_dias.on_change = self.seleccionar_dia
        # self.lista_hora_apertura = self.seleccionar_hora_apertura
        # self.lista_minutos_apertura = self.seleccionar_minutos_apertura
        # self.lista_hora_cierre = self.seleccionar_hora_cierre
        # self.lista_minutos_cierre = self.seleccionar_minutos_cierre
        
        # Agrega todas las filas a la columna resultado.
        self.fila.append(ft.Row([self.titulo]))
        self.fila.append(ft.Row([self.lista_edificios, self.boton_eliminar_edificio]))
        self.fila.append(ft.Row([self.campo_nombre_edificio, self.boton_agregar_edificio, self.boton_modificar_edificio]))
        self.fila.append(ft.Row([self.linea_0]))
        self.fila.append(ft.Row([self.titulo_horarios]))
        self.fila.append(ft.Row([
            self.lista_dias,
            self.lista_hora_apertura, self.separador_0,self.lista_minutos_apertura,
            self.separador_1,
            self.lista_hora_cierre, self.separador_2, self.lista_minutos_cierre,
            self.boton_establecer_horario,self.boton_eliminar_horario
        ]))
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
    
    def dibujar(self) -> ft.Container:
        return self.container


class UI_Config_Aulas():
    """
    Apartado de Aulas de los Edificios de la universidad.
    """
    def __init__(
            self
            ):
        """
        Crea el apartado de aulas de los edificios la universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Aulas de los Edificios"
        1) Dropdown de edificios - Drop. de aulas - Botón eliminar aula
        2) Campo identificador aula - Campo capacidad aula - Btn. agregar aula - Btn. modificar aula
        3) ----- (linea divisora) -----
        4) Título: "Equipamiento del Aula"
        5) Drop. de equipamiento - Campo de nombre equipamiento - Btn. agregar equipamiento - Btn. eliminar eq.
        6) ----- (linea divisora) -----
        7) Título: "Horario del Aula"
        8) Drop. con día - Hora apertura - Hora cierre - Btn. establecer horario - Btn. eliminar horario
        9) ----- (linea divisora) -----
        10) Btn. mostrar aulas - Btn. mostrar eq. de aula
        11) Tabla con datos de los aulas

        Returns
        -------
        None.

        """
        
        self.fila: List[ft.Row] = []
        
        # Fila 0:
        # 0) Título: "Configuración de Aulas de los Edificios"
        self.titulo = ft.Text(
            "Configuración de Aulas de los Edificios",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown de edificios - Drop. de aulas - Botón eliminar aula
        self.lista_edificios = ft.Dropdown(
            label="Edificios"
        )
        self.lista_aulas = ft.Dropdown(
            label="Aulas"
        )
        self.boton_eliminar_aula = ft.Button(
            "Eliminar aula"
        )
        
        # Fila 2:
        # 2) Campo identificador aula - Campo capacidad aula - Btn. agregar aula - Btn. modificar aula
        self.campo_identificador_aula = ft.TextField(
            label="Identificador del aula"
        )
        self.campo_capacidad_aula = ft.TextField(
            label="Capacidad del aula"
        )
        self.boton_agregar_aula = ft.Button(
            "Agregar aula"
        )
        self.boton_modificar_aula = ft.Button(
            "Modificar aula"
        )
        
        # Fila 3:
        # 3) ----- (linea divisora) -----
        self.linea_0 = ft.Divider(
            thickness=1
        )
        
        # Fila 4:
        # 4) Título: "Equipamiento del Aula"
        self.titulo_equipamiento = ft.Text(
            "Equipamiento del Aula",
            size=20,
            selectable=False
        )
        
        
        # Fila 5:
        # 5) Drop. de equipamiento - Campo de nombre equipamiento - Btn. agregar equipamiento - Btn. eliminar eq.
        self.lista_equipamiento = ft.Dropdown(
            label="Equipamiento"
        )
        self.campo_equipamiento_aula = ft.TextField(
            label="Equipamiento del aula"
        )
        self.boton_agregar_equipamiento = ft.Button(
            "Agregar equipamiento"
        )
        self.boton_eliminar_equipamiento = ft.Button(
            "Eliminar equipamiento"
        )
        
        # Fila 6:
        # 6) ----- (linea divisora) -----
        self.linea_1 = ft.Divider(
            thickness=1
        )
        
        # Fila 7:
        # 7) Título: "Horario del Aula"
        self.titulo_horario = ft.Text(
            "Horario del Aula",
            size=20,
            selectable=False
        )
        
        # Fila 8:
        # 8) Drop. con día - Hora apertura - Hora cierre - Btn. establecer horario - Btn. eliminar horario
        self.lista_dias = ft.Dropdown(
            label="Día",
            options=[
                ft.dropdown.Option("Lunes"),
                ft.dropdown.Option("Martes"),
                ft.dropdown.Option("Miércoles"),
                ft.dropdown.Option("Jueves"),
                ft.dropdown.Option("Viernes"),
                ft.dropdown.Option("Sábado"),
                ft.dropdown.Option("Domingo")
            ],
            enable_filter=True,
        )
        self.lista_hora_apertura = ft.Dropdown(
            label="Hora",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(24)
            ],
            enable_filter=True,
        )
        self.separador_0 = ft.Text(":")
        self.lista_minutos_apertura = ft.Dropdown(
            label="Minutos",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(0, 60, 5)
            ],
            enable_filter=True,
        )
        self.separador_1 = ft.Text("-")
        self.lista_hora_cierre = ft.Dropdown(
            label="Hora",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(24)
            ],
            enable_filter=True,
        )
        self.separador_2 = ft.Text(":")
        self.lista_minutos_cierre = ft.Dropdown(
            label="Minutos",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(0, 60, 5)
            ],
            enable_filter=True,
        )
        self.boton_establecer_horario = ft.Button(
            text="Establecer horario",
        )
        self.boton_eliminar_horario = ft.Button(
            text="Eliminar horario",
        )
        
        # Fila 9:
        # 9) ----- (linea divisora) -----
        self.linea_2 = ft.Divider(
            thickness=1
        )
        
        # Fila 10:
        # 10) Btn. mostrar aulas - Btn. mostrar eq. de aula
        self.boton_mostrar_aulas = ft.Button(
            "Mostrar Aulas"
        )
        self.boton_mostrar_equipamiento_aulas = ft.Button(
            "Mostrar Equipamiento de Aula"
        )
        
        # Fila 11:
        # 11) Tabla con datos de los aulas
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Edificio")),
                ft.DataColumn(ft.Text("Identificador de Aula")),
                ft.DataColumn(ft.Text("Capacidad")),
                ft.DataColumn(ft.Text("Lunes")),
                ft.DataColumn(ft.Text("Martes")),
                ft.DataColumn(ft.Text("Miércoles")),
                ft.DataColumn(ft.Text("Jueves")),
                ft.DataColumn(ft.Text("Viernes")),
                ft.DataColumn(ft.Text("Sábado")),
                ft.DataColumn(ft.Text("Domingo"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Anasagasti")),
                        ft.DataCell(ft.Text("B-101")),
                        ft.DataCell(ft.Text("50")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("CERRADO")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Anasagasti")),
                        ft.DataCell(ft.Text("B-201")),
                        ft.DataCell(ft.Text("50")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("9:00-21:00")),
                        ft.DataCell(ft.Text("CERRADO")),
                    ]
                )
            ],
        )
        
        self.fila.append(ft.Row([self.titulo]))
        self.fila.append(ft.Row([self.lista_edificios, self.lista_aulas, self.boton_eliminar_aula]))
        self.fila.append(ft.Row([self.campo_identificador_aula, self.campo_capacidad_aula, self.boton_agregar_aula, self.boton_modificar_aula]))
        self.fila.append(ft.Row([self.linea_0]))
        self.fila.append(ft.Row([self.titulo_equipamiento]))
        self.fila.append(ft.Row([self.lista_equipamiento, self.campo_equipamiento_aula, self.boton_agregar_equipamiento, self.boton_eliminar_equipamiento]))
        self.fila.append(ft.Row([self.linea_1]))
        self.fila.append(ft.Row([self.titulo_horario]))
        self.fila.append(ft.Row([self.lista_dias,
                                 self.lista_hora_apertura, self.separador_0, self.lista_minutos_apertura,
                                 self.separador_1,
                                 self.lista_hora_cierre, self.separador_2, self.lista_minutos_cierre,
                                 self.boton_establecer_horario,
                                 self.boton_eliminar_horario]))
        self.fila.append(ft.Row([self.linea_2]))
        self.fila.append(ft.Row([self.boton_mostrar_aulas, self.boton_mostrar_equipamiento_aulas]))
        self.fila.append(ft.Row([self.tabla]))
        
        # Columna final con todas las filas creadas.
        self.columna = ft.Column(
            controls=self.fila
        )
        self.container = ft.Container(
            content=self.columna
        )
    
    def dibujar(self) -> ft.Container:
        return self.container


class UI_Config_Carreras():
    """
    Apartado de Carreras de la universidad.
    """
    def __init__(
            self
            ):
        """
        Crea el apartado de aulas de los edificios la universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Carreras de la Universidad"
        1) Dropdown carreras - Botón eliminar carrera    
        2) Campo nombre de carrera - Btn. agregar carrera - Btn. modificar carrera
        3) Drop. edificio preferido para la carrera - Btn. eliminar preferencia
        4) ----- (linea divisora) -----
        5) Tabla con datos de las carreras

        Returns
        -------
        None.

        """
        
        self.fila: List[ft.Row] = []
        
        # Fila 0:
        # 0) Título: "Configuración de Carreras de la Universidad"
        self.titulo = ft.Text(
            "Configuración de Carreras de la Universidad",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown carreras - Botón eliminar carrera
        self.lista_carreras = ft.Dropdown(
            label="Carrera"
        )
        self.boton_eliminar_carrera = ft.Button(
            "Eliminar carrera"
        )
        
        # Fila 2:
        # 2) Campo nombre de carrera - Btn. agregar carrera - Btn. modificar carrera
        self.campo_nombre_carrera = ft.TextField(
            label="Nombre de la carrera"
        )
        self.boton_agregar_carrera = ft.Button(
            "Agregar carrera"
        )
        self.boton_modificar_carrera = ft.Button(
            "Modificar carrera"
        )
        
        # Fila 3:
        # 3) Drop. edificio preferido para la carrera - Btn. eliminar preferencia
        self.lista_edificios = ft.Dropdown(
            label="Edificio"
        )
        self.boton_eliminar_preferencia = ft.Button(
            "Eliminar preferencia de edificio"
        )
        
        # Fila 4:
        # 4) ----- (linea divisora) -----
        self.linea = ft.Divider(
            thickness=1
        )
        
        # Fila 5:
        # 5) Tabla con datos de las carreras
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Carrera")),
                ft.DataColumn(ft.Text("Preferencia de Edificio"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Ingeniería en Computación")),
                        ft.DataCell(ft.Text("Anasagasti")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Ingeniería Electrónica")),
                        ft.DataCell(ft.Text("Anasagasti")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Antropología")),
                        ft.DataCell(ft.Text("Mitre")),
                    ]
                ),
            ],
        )
        
        self.fila.append(ft.Row([self.titulo]))
        self.fila.append(ft.Row([self.lista_carreras, self.boton_eliminar_carrera]))
        self.fila.append(ft.Row([self.campo_nombre_carrera, self.boton_agregar_carrera, self.boton_modificar_carrera]))
        self.fila.append(ft.Row([self.lista_edificios, self.boton_eliminar_preferencia]))
        self.fila.append(ft.Row([self.linea]))
        self.fila.append(ft.Row([self.tabla]))
        
        # Columna final con todas las filas creadas.
        self.columna = ft.Column(
            controls=self.fila
        )
        self.container = ft.Container(
            content=self.columna
        )
    
    def dibujar(self) -> ft.Container:
        return self.container


class UI_Config_Actividades():
    """
    Apartado de Actividades/Materias de la universidad.
    """
    def __init__(
            self
            ):
        """
        Crea el apartado de aulas de los edificios la universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Actividades/Materias de la Universidad"
        1) Dropdown identificador - Drop. nombre actividad - Drop. comisión - Botón eliminar actividad
        2) Campo nombre de carrera - Btn. agregar carrera - Btn. modificar carrera
        3) Drop. edificio preferido para la carrera - Btn. eliminar preferencia
        4) ----- (linea divisora) -----
        5) Tabla con datos de las carreras

        Returns
        -------
        None.

        """
        
        self.fila: List[ft.Row] = []
        
        # Fila 0:
        # 0) Título: "Configuración de Actividades/Materias de la Universidad"
        self.titulo = ft.Text(
            "Configuración de Actividades/Materias de la Universidad",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown identificador - Drop. nombre actividad - Drop. comisión - Botón eliminar actividad
        self.lista_identificador_actividades = ft.Dropdown(
            label="Identificador"
        )
        self.lista_nombre_actividades = ft.Dropdown(
            label="Nombre de actividad"
        )
        
        # Fila 2:
        # 2) Campo nombre de carrera - Btn. agregar carrera - Btn. modificar carrera
        self.lista_comision_actividades = ft.Dropdown(
            label="Comisión"
        )
        self.boton_eliminar_actividad = ft.Button(
            "Eliminar actividad"
        )
        
        # Fila 3:
        # 3) Drop. edificio preferido para la carrera - Btn. eliminar preferencia
        self.campo_identificador_actividad = ft.TextField(
            label="Identificador"
        )
        self.campo_nombre_actividad = ft.TextField(
            label="Nombre de actividad"
        )
        
        # Fila 4:
        # 4) ----- (linea divisora) -----
        self.campo_comision_actividad = ft.TextField(
            label="Comisión"
        )
        self.boton_agregar_actividad = ft.Button(
            "Agregar actividad"
        )
        self.boton_modificar_actividad = ft.Button(
            "Modificar actividad"
        )
        
        # Fila 5:
        # 5) Tabla con datos de las carreras
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Identificador")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Comisión")),
                ft.DataColumn(ft.Text("Carrera")),
                ft.DataColumn(ft.Text("Año")),
                ft.DataColumn(ft.Text("Cant. de Alumnos")),
                ft.DataColumn(ft.Text("Preferencia Edificio"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("PI")),
                        ft.DataCell(ft.Text("Programación I")),
                        ft.DataCell(ft.Text("A")),
                        ft.DataCell(ft.Text("Ingeniería en Computación")),
                        ft.DataCell(ft.Text("1")),
                        ft.DataCell(ft.Text("100")),
                        ft.DataCell(ft.Text("Anasagasti")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("PI")),
                        ft.DataCell(ft.Text("Programación I")),
                        ft.DataCell(ft.Text("B")),
                        ft.DataCell(ft.Text("Ingeniería en Computación")),
                        ft.DataCell(ft.Text("1")),
                        ft.DataCell(ft.Text("100")),
                        ft.DataCell(ft.Text("Anasagasti")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("PII")),
                        ft.DataCell(ft.Text("Programación II")),
                        ft.DataCell(ft.Text("N/A")),
                        ft.DataCell(ft.Text("Ingeniería en Computación")),
                        ft.DataCell(ft.Text("2")),
                        ft.DataCell(ft.Text("100")),
                        ft.DataCell(ft.Text("Anasagasti")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Matemática I")),
                        ft.DataCell(ft.Text("MI")),
                        ft.DataCell(ft.Text("N/A")),
                        ft.DataCell(ft.Text("Ingeniería en Computación")),
                        ft.DataCell(ft.Text("1")),
                        ft.DataCell(ft.Text("50")),
                        ft.DataCell(ft.Text("Mitre")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Ingeniería de Software")),
                        ft.DataCell(ft.Text("IS")),
                        ft.DataCell(ft.Text("N/A")),
                        ft.DataCell(ft.Text("Ingeniería en Computación")),
                        ft.DataCell(ft.Text("4")),
                        ft.DataCell(ft.Text("50")),
                        ft.DataCell(ft.Text("Anasagasti")),
                    ]
                ),
            ],
        )
        
        self.fila.append(ft.Row([self.titulo]))
        self.fila.append(ft.Row([self.lista_identificador_actividades, self.lista_nombre_actividades]))
        self.fila.append(ft.Row([self.lista_comision_actividades, self.boton_eliminar_actividad]))
        self.fila.append(ft.Row([self.campo_identificador_actividad, self.campo_nombre_actividad]))
        self.fila.append(ft.Row([self.campo_comision_actividad, self.boton_agregar_actividad, self.boton_modificar_actividad]))
        self.fila.append(ft.Row([self.tabla]))
        
        # Columna final con todas las filas creadas.
        self.columna = ft.Column(
            controls=self.fila
        )
        self.container = ft.Container(
            content=self.columna
        )
    
    def dibujar(self) -> ft.Container:
        return self.container

# MENU DE APARTADOS

class UI_Config():
    """
    Apartado 'Padre', con todos los apartados de la configuración.
    """
    def __init__(
            self,
            universidad
            ):
        self.universidad = universidad
        
        # Botones para configurar cada apartado.
        self.btn_edificios = UI_BotonConfig(self, "Edificios", APARTADO.EDIFICIOS)
        self.btn_aulas = UI_BotonConfig(self, "Aulas", APARTADO.AULAS)
        self.btn_carreras = UI_BotonConfig(self, "Carreras", APARTADO.CARRERAS)
        self.btn_actividades = UI_BotonConfig(self, "Actividades/materias", APARTADO.ACTIVIDADES)
        
        self.fila_botones = ft.Row(
            [
                self.btn_edificios.dibujar(),
                self.btn_aulas.dibujar(),
                self.btn_carreras.dibujar(),
                self.btn_actividades.dibujar()
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing = 10,
            scroll=ft.ScrollMode.AUTO,
            )
        
        self.apartado_edificios = UI_Config_Edificios(self)
        self.apartado_aulas = UI_Config_Aulas()
        self.apartado_carreras = UI_Config_Carreras()
        self.apartado_actividades = UI_Config_Actividades()
        
        self.apartado = self.apartado_edificios
        
        self.menu_config = ft.Column(
            [
                self.fila_botones,
                self.apartado.dibujar()
            ],
            alignment=ft.MainAxisAlignment.START,
            #expand=True
            )
        
        self.container = ft.Container(
            content=self.menu_config,
            alignment=ft.alignment.top_left,
            padding=20,
            expand=False,
            border=ft.border.all(1, "black")
        )
    
    def dibujar(self) -> ft.Container:
        return self.container
    
    def cambiar_apartado(self, apartado: str) -> None:
        """
        Cambia el apartado que se está mostrando actualmente.

        Parameters
        ----------
        apartado : str
            Palabra clave del nombre del apartado. Ejemplo: "edificios".

        Returns
        -------
        None.

        """
        match apartado:
            case APARTADO.EDIFICIOS:
                self.apartado = self.apartado_edificios
            case APARTADO.AULAS:
                self.apartado = self.apartado_aulas
            case APARTADO.CARRERAS:
                self.apartado = self.apartado_carreras
            case APARTADO.ACTIVIDADES:
                self.apartado = self.apartado_actividades
            case _:
                self.apartado = self.apartado_edificios
        self.menu_config.controls.clear()
        self.menu_config.controls.append(self.fila_botones)
        self.menu_config.controls.append(self.apartado.dibujar())
        self.menu_config.update()
