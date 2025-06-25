# -*- coding: utf-8 -*-
"""
Apartado de configuración para el input y output de datos de Edificios de la
Universidad.

@author: Cristian
"""

import flet as ft
from pandas import DataFrame

from typing import List

from .datos import limpiar_texto, generar_tabla
from .alertas import VentanaAlerta


class UI_Config_Edificios():
    """
    Apartado de Edificios de la universidad.
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
        
    def limpiar_seleccion_horario(self):
        """
        Limpia la selección del horario, quitando las opciones elegidas dentro
        de los dropdowns. (tristemente solamente se puede lograr esto volviendo
        a crear los objetos correspondientes y actualizando el apartado).

        Returns
        -------
        None.

        """
        # Se vuelven a crear los elementos para que estén vacíos en selección.
        self.lista_dias.value = ""
        self.lista_hora_apertura.value = ""
        self.lista_hora_cierre.value = ""
        self.lista_minutos_apertura.value = ""
        self.lista_minutos_cierre.value = ""
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def agregar_edificio(self, e):
        """
        Función "handler" para el click del botón "Agregar edificio".
        
        Agrega el nombre del edificio nuevo, con un horario predeterminado a
        la "base de datos" del programa.
        
        Al hacer click, limpia la selección del edificio, del campo de texto y
        del horario, para prevenir posibles errores futuros.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # Toma el input del usuario.
        nombre_edificio: str = limpiar_texto(str(self.campo_nombre_edificio.value)) # datos.py
        
        print(f"Agregar edificio: {nombre_edificio}")
        
        try:
            # Se agrega el edificio a la "base de datos".
            self.ui_config.universidad.agregar_edificio(nombre_edificio)
            
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
            
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def modificar_edificio(self, e):
        """
        Función "handler" para el click del botón "Modificar edificio".
        
        Modifica el nombre de un edificio ya agregado a la "base de datos" del
        programa. (No modifica horarios).
        
        Al hacer click, limpia la selección del edificio y del campo de texto.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # Toma el input del usuario.
        nombre_edificio: str = str(self.lista_edificios.value or "") # Si es None toma valor ""
        nuevo_nombre_edificio: str = limpiar_texto(str(self.campo_nombre_edificio.value))
        
        print(f"Modificar edificio: {nombre_edificio} -> {nuevo_nombre_edificio}")
        
        try:
            # Se modifica el edificio en la "base de datos".
            print(self.ui_config.universidad.columnas_edificios())
            self.ui_config.universidad.modificar_edificio(
                nombre_edificio,
                self.ui_config.universidad.columnas_edificios()[0], 
                nuevo_nombre_edificio
            )
        
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
        
    def eliminar_edificio(self, e): #Nota: Si no se puede eliminar porque hay aulas que lo usa, lo resuelvo en universidad.py
        """
        Función "handler" para el click del botón "Eliminar edificio".
        
        Elimina un edificio ya agregado a la "base de datos" del programa.
        
        Al hacer click, limpia la selección del edificio y del campo de texto.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        nombre_edificio: str = str(self.lista_edificios.value or "") # Si es None toma valor ""
        print(f"Eliminar edificio: {nombre_edificio}")
        
        try:
            # Se elimina el edificio en la "base de datos".
            self.ui_config.universidad.eliminar_edificio(nombre_edificio)
        
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
        
    def establecer_horario(self, e):
        """
        Función "handler" para el click del botón "Establecer horario".
        
        Establece el horario de un día elegido de un edificio ya agregado a la
        "base de datos" del programa.
        
        Al hacer click, limpia la selección del horario y día.

        Returns
        -------
        None.

        """
        nombre_edificio: str = str(self.lista_edificios.value or "") # Si es None toma valor ""
        dia: str = str(self.lista_dias.value or "") # "Miércoles"
        hora_apertura: str = str(self.lista_hora_apertura.value or "") # "09"
        hora_cierre: str = str(self.lista_hora_cierre.value or "") # "00"
        minutos_apertura: str = str(self.lista_minutos_apertura.value or "") # "21"
        minutos_cierre: str = str(self.lista_minutos_cierre.value or "") # "00"
        
        horario: str = f"{hora_apertura}:{minutos_apertura}-{hora_cierre}:{minutos_cierre}"
        
        print(f"Establecer horario: {dia}, {horario} -> Edificio: {nombre_edificio}")
        
    
        try:
            # Se establece el horario del día elegido del edificio en la
            # "base de datos".
            self.ui_config.universidad.modificar_horario_edificio(
                nombre_edificio,
                dia,
                int(hora_apertura),
                int(hora_cierre),
                int(minutos_apertura),
                int(minutos_cierre)
            )
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_horario(self, e):
        """
        Función "handler" para el click del botón "Eliminar horario".
        
        Elimina un horario de un día elegido de un edificio ya agregado a la
        "base de datos" del programa.
        
        Al hacer click, limpia la selección del horario y día.

        Returns
        -------
        None.

        """
        nombre_edificio: str = str(self.lista_edificios.value or "") # Si es None toma valor ""
        dia: str = str(self.lista_dias.value or "") # Si es None toma valor ""
        
        print(f"Eliminar horario: {dia} -> Edificio: {nombre_edificio}")
        
        try:
            # Se "elimina" (se marca como cerrado) el horario del día elegido
            # del edificio en la "base de datos".
            self.ui_config.universidad.modificar_edificio(
                nombre_edificio,
                dia,
                "CERRADO"
            )
        
            # Si es que no hay ningún problema:
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
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
        # Limpia el campo de texto del edificio.
        self.campo_nombre_edificio.value = ""
    
        # Limpia las listas de selección de horario.
        self.limpiar_seleccion_horario()
    
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def seleccionar_dia(self, e):
        """
        Funcion "handler" al seleccionar un día de la selección de horario.
        
        Si el usuario no seleccionó ningún edificio de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.
        
        De lo contrario, si al seleccionar un día determinado tiene un horario
        definido (no está cerrado), se seleccionan los valores de horas y
        minutos para las listas de selección de ese horario (para ahorrarle el
        trabajo de tener que hacer toda la selección de cero, si lo que quiere
        es hacer un pequeño cambio, por ejemplo en los minutos de cierre).

        Returns
        -------
        None.

        """
        nombre_edificio: str = str(self.lista_edificios.value or "")
        print(f"Edificio: {nombre_edificio}")
        dia: str = str(self.lista_dias.value or "")
        print(f"Dia: {dia}")
        
        if nombre_edificio == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un edificio,
                primero debe seleccionar el edificio al que se le aplicarán los
                cambios.
                """
            )
        
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
        elif dia in self.ui_config.universidad.columnas_edificios()[1:]:
                try:
                    # Si explota aca por falta de argumentos de retorno, no hace el update.
                    # El metodo retorna los atributos en ese orden:
                    hora_apertura, minutos_apertura, hora_cierre, minutos_cierre = (
                        self.ui_config.universidad.horario_segmentado_edificio(nombre_edificio, dia)
                    )
                    
                    # "Autoselecciona" o muestra el horario del edificio para el día
                    # elegido.
                    self.lista_hora_apertura.value = hora_apertura
                    self.lista_hora_cierre.value = hora_cierre
                    self.lista_minutos_apertura.value = minutos_apertura
                    self.lista_minutos_cierre.value = minutos_cierre
                    
                    # Se actualizan los elementos de la interfaz.
                    self.actualizar_filas()
                    self.actualizar_apartado()
                except Exception as exc:
                    print("Intente actualizar una lista de horarios de un dia cerrado. Loggeo en print para saber nomas.")
                    pass
    
    def seleccionar_hora(self, e):
        """
        Funcion "handler" al seleccionar una hora.
        
        Si el usuario no seleccionó ningún edificio de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.
        
        De lo contrario, si selecciona una hora y no ha seleccionado un día
        determinado, le alerta con una ventana para que haga la selección
        correspondiente.

        Returns
        -------
        None.

        """
        nombre_edificio: str = str(self.lista_edificios.value or "")
        dia: str = str(self.lista_dias.value or "")
        
        if nombre_edificio == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un edificio,
                primero debe seleccionar el edificio al que se le aplicarán los
                cambios.
                """
            )
        
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
        elif dia == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un edificio,
                primero debe seleccionar el día al que se le aplicarán los
                cambios.
                """
            )
        
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
    
    def seleccionar_minutos(self, e):
        """
        Funcion "handler" al seleccionar los minutos de una hora.
        
        Si el usuario no seleccionó ningún edificio de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.
        
        De lo contrario, si selecciona los minutos y no ha seleccionado un día
        determinado, le alerta con una ventana para que haga la selección
        correspondiente.

        Returns
        -------
        None.

        """
        nombre_edificio: str = str(self.lista_edificios.value or "")
        dia: str = str(self.lista_dias.value or "")
        
        if nombre_edificio == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un edificio,
                primero debe seleccionar el edificio al que se le aplicarán los
                cambios.
                """
             )
        
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
        elif dia == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un edificio,
                primero debe seleccionar el día al que se le aplicarán los
                cambios.
                """
            )
        
            # Limpia el campo de texto del edificio.
            self.campo_nombre_edificio.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
    
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
        # 0) Título: "Configuración de Edificios de la Universidad"
        self.titulo = ft.Text(
            value="Configuración de Edificios de la Universidad",
            text_align=ft.TextAlign.LEFT,
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown de edificios - Botón eliminar edificio
        self.lista_edificios = self.crear_lista_edificios()
        self.boton_eliminar_edificio = ft.Button(
            text="Eliminar edificio",
        )
        
        # Fila 2:
        # 2) Campo nombre edificio - Btn agregar edificio - Btn. modificar edificio
        self.campo_nombre_edificio = self.crear_campo_nombre_edificio()
        self.boton_agregar_edificio = ft.Button(
            text="Agregar edificio",
        )
        self.boton_modificar_edificio = ft.Button(
            text="Modificar edificio",
        )
        
        # Fila 3: (línea divisora)
        # 3) ----- (linea divisora) -----
        self.linea_0 = self.crear_linea()
        
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
        self.lista_dias = self.crear_lista_dias()
        self.lista_hora_apertura = self.crear_lista_horas()
        self.separador_0 = ft.Text(":")
        self.lista_minutos_apertura = self.crear_lista_minutos()
        self.separador_1 = ft.Text("-")
        self.lista_hora_cierre = self.crear_lista_horas()
        self.separador_2 = ft.Text(":")
        self.lista_minutos_cierre = self.crear_lista_minutos()
        self.boton_establecer_horario = ft.Button(
            text="Establecer horario",
        )
        self.boton_eliminar_horario = ft.Button(
            text="Eliminar horario",
        )
        
        # Fila 6
        # 6) ----- (linea divisora) -----
        self.linea_1 = self.crear_linea()
        
        # Fila 7:
        # 7) Tabla con datos de los edificios cargados
        self.tabla = self.crear_tabla()
        
        # Carga inicial de todos los datos:
        self.cargar_datos_inicio()
        
        # Se actualizan los handlers para los botones y se agregan las filas
        # para la interfaz.
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
        opciones_edificios: List[ft.dropdown.Option] = []
        for edificio in self.ui_config.universidad.nombres_edificios():
            opciones_edificios.append(ft.dropdown.Option(str(edificio)))
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
        self.tabla = generar_tabla(self.ui_config.universidad.mostrar_edificios())
    
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
        self.cargar_datos_tabla()
    
    def crear_lista_edificios(self) -> ft.Dropdown:
        """
        Crea el elemento de lista para la selección de edificios ya cargados.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de edificios.

        """
        dropdown = ft.Dropdown(
            label="Edificios",
            options=[
                # ft.dropdown.Option("Anasagasti"),
                # ft.dropdown.Option("Mitre"),
            ],
            enable_filter=True,
        )
        return dropdown
    
    def crear_campo_nombre_edificio(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso del nombre del edificio
        a crear/agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input del nombre de edificio.

        """
        textfield = ft.TextField(
            label="Nombre del edificio",
        )
        return textfield
    
    def crear_lista_dias(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso del día en el horario.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de días (Lun-Dom).

        """
        dropdown = ft.Dropdown(
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
        return dropdown
    
    def crear_lista_horas(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso de horas en el horario.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de horas (00-23 hs).

        """
        dropdown = ft.Dropdown(
            label="Hora",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(24)
            ],
            enable_filter=True,
        )
        return dropdown
    
    def crear_lista_minutos(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso de minutos en el horario.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de minutos (00-45 mins).

        """
        dropdown = ft.Dropdown(
            label="Minutos",
            options=[
                ft.dropdown.Option(f"{i:02}") for i in range(0, 60, 15)
            ],
            enable_filter=True,
        )
        return dropdown
    
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
            "Nombre del Edificio": [],
            "Lunes": [],
            "Martes": [],
            "Miércoles": [],
            "Jueves": [],
            "Viernes": [],
            "Sábado": [],
            "Domingo": [],
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
        self.boton_agregar_edificio.on_click = self.agregar_edificio
        self.boton_eliminar_edificio.on_click = self.eliminar_edificio
        self.boton_modificar_edificio.on_click = self.modificar_edificio
        self.boton_establecer_horario.on_click = self.establecer_horario
        self.boton_eliminar_horario.on_click = self.eliminar_horario
        
        # Define el comportamiento "on_change" de cada elemento (listas).
        self.lista_edificios.on_change = self.seleccionar_edificio
        self.lista_dias.on_change = self.seleccionar_dia
        self.lista_hora_apertura.on_change = self.seleccionar_hora
        self.lista_minutos_apertura.on_change = self.seleccionar_minutos
        self.lista_hora_cierre.on_change = self.seleccionar_hora
        self.lista_minutos_cierre.on_change = self.seleccionar_minutos
    
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
