# -*- coding: utf-8 -*-
"""
Apartado de configuración para el input y output de datos de Aulas de los
Edificios de la Universidad.

@author: Cristian
"""

import flet as ft
from pandas import DataFrame

from typing import List

from .datos import limpiar_texto, generar_tabla
from .alertas import VentanaAlerta


class TABLA():
    TODAS_LAS_AULAS = "todas"
    AULAS_POR_EDIFICIO = "edificio"
    EQUIPAMIENTO = "equipamiento"


class UI_Config_Aulas():
    """
    Apartado de Aulas de los Edificios de la universidad.
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
    
    def agregar_aula(self, e):
        """
        Función "handler" para el click del botón "Agregar aula".
        
        Agrega el nombre del aula nueva, con un horario predeterminado a
        la "base de datos" del programa.
        
        Al hacer click, limpia la selección del aula, del campo de texto y
        del horario, para prevenir posibles errores futuros.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # TODO juan
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aula_nueva: str = limpiar_texto(str(self.campo_identificador_aula.value))
        capacidad_aula_nueva: str = limpiar_texto(str(self.campo_capacidad_aula.value))
        
        print(f"Agregar aula: {nombre_aula_nueva} (capacidad -> {capacidad_aula_nueva}), en Edificio: {nombre_edificio}")
        
        try:
            # Se agrega el aula a la "base de datos", con el horario
            # predeterminado por el horario del edificio.
            self.ui_config.universidad.agregar_aula(nombre_aula_nueva, capacidad_aula_nueva, nombre_edificio)
            
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
            
            # Limpia la capacidad del aula.
            self.campo_capacidad_aula.value = ""
            
            # Limpia la selección del aula.
            self.lista_aulas.value = ""
            
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def modificar_aula(self, e):
        """
        Función "handler" para el click del botón "Modificar aula".
        
        Modifica el nombre y/o la capacidad de un aula ya agregada a la "base
        de datos" del programa. (No modifica horarios).
        
        Al hacer click, limpia la selección del aula y de los campo de texto.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # TODO
        # Toma el input del usuario.
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aula: str = str(self.lista_aulas.value or "")
        nuevo_nombre_aula: str = limpiar_texto(str(self.campo_identificador_aula.value))
        capacidad_nueva: str = limpiar_texto(str(self.campo_capacidad_aula.value))
        
        print(f"Modificar aula: Edificio {nombre_edificio}, {nombre_aula} -> {nuevo_nombre_aula}, capacidad: {capacidad_nueva}")
        
        try:
            if (nuevo_nombre_aula != nombre_aula and nuevo_nombre_aula in self.ui_config.universidad.nombres_aulas()):
                raise(Exception("El nombre nuevo no puede apuntar a otro edificio en el sistema"))
            # Se modifica el aula en la "base de datos".
            # print(self.ui_config.universidad.columnas_edificios())
            
            self.ui_config.universidad.modificar_aula(nombre_aula, "Aula", nuevo_nombre_aula)   #Rename
            self.ui_config.universidad.modificar_aula(nuevo_nombre_aula, "Capacidad", capacidad_nueva)
        
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
            
            # Limpia el campo de texto de la capacidad.
            self.campo_capacidad_aula.value = ""
            
            # Limpia la selección de la lista de aulas.
            self.lista_aulas.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_aula(self, e):
        """
        Función "handler" para el click del botón "Eliminar aula".
        
        Elimina un aula ya agregada a la "base de datos" del programa.
        
        Al hacer click, limpia la selección del aula y del campo de texto.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # TODO
        nombre_edificio: str = str(self.lista_edificios.value or "")
        identificador_aula: str = str(self.lista_aulas.value or "")
        
        print(f"Eliminar aula: Edificio: {nombre_edificio}, Aula: {identificador_aula}")
        
        try:
            # Se elimina el aula en la "base de datos".
            # self.ui_config.universidad.eliminar_aula(nombre_edificio, identificador_aula)
        
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
            
            # Limpia el campo de seleccción del aula.
            self.lista_aulas.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def agregar_equipamiento(self, e):
        """
        Función "handler" para el click del botón "Agregar equipamiento".
        
        Agrega el nombre del equipamiento nuevo para el aula seleccionada.
        
        Al hacer click, limpia la selección del equipamiento y del campo de
        texto, para prevenir posibles errores futuros.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # TODO juan
        nombre_edificio: str = str(self.lista_edificios.value or "")
        identificador_aula: str = limpiar_texto(str(self.campo_identificador_aula.value))
        nombre_equipamiento: str = limpiar_texto(str(self.campo_equipamiento_aula.value))
        
        print(f"Agregar equipamiento:")
        print(f"\t- Edificio: {nombre_edificio}")
        print(f"\t- Aula: {identificador_aula}")
        print(f"\t- Equipamiento: {nombre_equipamiento}")
        
        try:
            # Se agrega el aula a la "base de datos", con el horario
            # predeterminado por el horario del edificio.
            # self.ui_config.universidad.agregar_aula(nombre_edificio, identificador_aula_nueva, capacidad_aula_nueva)
            
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del edificio.
            self.campo_identificador_aula.value = ""
            
            # Limpia el campo de texto de la capacidad.
            self.campo_capacidad_aula.value = ""
            
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_equipamiento(self, e):
        """
        Función "handler" para el click del botón "Eliminar equipamiento".
        
        Elimina un equipamiento ya agregado a un aula de la "base de datos" del
        programa.
        
        Al hacer click, limpia el campo de texto y la lista de equipamiento.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.

        Returns
        -------
        None.

        """
        # TODO
        nombre_edificio: str = str(self.lista_edificios.value or "")
        identificador_aula: str = str(self.lista_aulas.value or "")
        nombre_equipamiento: str = limpiar_texto(str(self.campo_equipamiento_aula.value))
        
        print(f"Eliminar equipamiento:")
        print(f"\t- Edificio: {nombre_edificio}")
        print(f"\t- Aula: {identificador_aula}")
        print(f"\t- Equipamiento: {nombre_equipamiento}")
        
        try:
            # Se elimina el aula en la "base de datos".
            # self.ui_config.universidad.eliminar_equipamiento(
            #     nombre_edificio,
            #     identificador_aula,
            #     nombre_equipamiento
            # )
        
            # Si es que no hay ningún problema:
            # Limpia el campo de texto del equipamiento del aula.
            self.campo_equipamiento_aula.value = ""
        
            # Limpia la lista del equipamiento del aula.
            self.lista_equipamiento.value = ""
        
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
        # TODO
        nombre_edificio: str = str(self.lista_edificios.value or "")
        identificador_aula: str = str(self.lista_aulas.value or "")
        dia: str = str(self.lista_dias.value or "")
        hora_apertura: str = str(self.lista_hora_apertura.value or "")
        hora_cierre: str = str(self.lista_hora_cierre.value or "")
        minutos_apertura: str = str(self.lista_minutos_apertura.value or "")
        minutos_cierre: str = str(self.lista_minutos_cierre.value or "")
        
        horario: str = f"{hora_apertura}:{minutos_apertura}-{hora_cierre}:{minutos_cierre}"
        
        print(f"Establecer horario: {dia}, {horario} -> Edificio: {nombre_edificio}, Aula: {identificador_aula}")
        
    
        try:
            # Se establece el horario del día elegido del edificio en la
            # "base de datos".
            # self.ui_config.universidad.modificar_horario_aula(
            #     nombre_edificio,
            #     identificador_aula,
            #     dia,
            #     int(hora_apertura),
            #     int(hora_cierre),
            #     int(minutos_apertura),
            #     int(minutos_cierre)
            # )
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_horario(self, e):
        """
        Función "handler" para el click del botón "Eliminar horario".
        
        Elimina un horario de un día elegido de un aula ya agregada a la
        "base de datos" del programa.
        
        Al hacer click, limpia la selección del horario y día.

        Returns
        -------
        None.

        """
        # TODO
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aula: str = str(self.lista_aulas.value or "")
        dia: str = str(self.lista_dias.value or "")
        
        print(f"Eliminar horario: {dia} -> Edificio: {nombre_edificio}, Aula: {nombre_aula}")
        
        try:
            # Se "elimina" (se marca como cerrado) el horario del día elegido
            # del aula en la "base de datos".
            self.ui_config.universidad.modificar_aula(nombre_aula, dia, "CERRADO")
        
            # Si es que no hay ningún problema:
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def mostrar_aulas_todas(self, e):
        """
        Función "handler" para el click del botón "Mostrar todas las Aulas".
        
        Muestra todas las aulas de todos los edificios, junto a sus capacidades
        de alumnos y horarios.

        Returns
        -------
        None.

        """
        # Define la tabla a mostrar.
        self.tabla_actual = TABLA.TODAS_LAS_AULAS
        
        # Actualiza los elementos.
        self.actualizar_tabla()
    
    def mostrar_aulas_edificio(self, e):
        """
        Función "handler" para el click del botón "Mostrar Aulas del Edificio
        seleccionado".
        
        Muestra todas las aulas de un edificio, junto a sus capacidades de
        alumnos y horarios.

        Returns
        -------
        None.

        """
        # Define la tabla a mostrar.
        self.tabla_actual = TABLA.AULAS_POR_EDIFICIO
        
        # Actualiza los elementos.
        self.actualizar_tabla()
    
    def mostrar_equipamiento_aulas(self, e):
        """
        Función "handler" para el click del botón "Mostrar Equipamiento de
        Aula".
        
        Muestra todos los equipamientos agregados a un aula de un edificio.

        Returns
        -------
        None.

        """
        # Define la tabla a mostrar.
        self.tabla_actual = TABLA.EQUIPAMIENTO
        
        # Actualiza los elementos.
        self.actualizar_tabla()
    
    def seleccionar_edificio(self, e):
        """
        Función "handler" al seleccionar un edificio.
        
        Carga todas las aulas disponibles en ese edificio para la lista de
        aulas.

        Returns
        -------
        None.

        """
        self.cargar_datos_aulas()
        
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def seleccionar_aula(self, e):
        """
        Funcion "handler" al seleccionar un aula de la lista de selección.
        
        Si el usuario no seleccionó ningún edificio de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.
        
        De lo contrario, si ya seleccionó el edificio, se cargan los datos de
        del equipamiento que ya tenga cargado y los horarios del mismo.

        Returns
        -------
        None.

        """
        nombre_edificio: str = str(self.lista_edificios.value or "")
        
        if nombre_edificio == "":
            self.alertar("Para seleccionar un aula, primero debe seleccionar un edificio.")
        else:
            self.cargar_datos_equipamiento()
        
            self.actualizar_filas()
            self.actualizar_apartado()
    
    def seleccionar_equipamiento(self, e):
        """
        Funcion "handler" al seleccionar un equipamiento de la lista de
        selección.
        
        Si el usuario no seleccionó ningún aula de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.

        Returns
        -------
        None.

        """
        identificador_aula: str = str(self.lista_aulas.value or "")
        
        if identificador_aula == "":
            self.alertar("Para seleccionar un equipamiento, primero debe seleccionar un aula.")
    
    def seleccionar_dia(self, e):
        """
        Funcion "handler" al seleccionar un día de la selección de horario.
        
        Si el usuario no seleccionó ningún aula de la lista de selección,
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
        # TODO
        identificador_aula: str = str(self.lista_aulas.value or "")
        
        dia: str = str(self.lista_dias.value or "")
        print(f"Dia: {dia}")
        
        if identificador_aula == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un aula,
                primero debe seleccionar el aula al que se le aplicarán los
                cambios.
                """
            )
        
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
        # elif dia in dias:
        #     try:
        #         # Si explota aca por falta de argumentos de retorno, no hace el update.
        #         # El metodo retorna los atributos en ese orden:
        #         hora_apertura, minutos_apertura, hora_cierre, minutos_cierre = (
        #             self.ui_config.universidad.horario_segmentado_edificio(nombre_edificio, dia)
        #         )
                
        #         # "Autoselecciona" o muestra el horario del edificio para el día
        #         # elegido.
        #         self.lista_hora_apertura.value = hora_apertura
        #         self.lista_hora_cierre.value = hora_cierre
        #         self.lista_minutos_apertura.value = minutos_apertura
        #         self.lista_minutos_cierre.value = minutos_cierre
                
        #         # Se actualizan los elementos de la interfaz.
        #         self.actualizar_filas()
        #         self.actualizar_apartado()
        #     except Exception as exc:
        #         print("Intente actualizar una lista de horarios de un dia cerrado. Loggeo en print para saber nomas.")
        #         pass
    
    def seleccionar_hora(self, e):
        """
        Funcion "handler" al seleccionar una hora.
        
        Si el usuario no seleccionó ningún aula de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.
        
        De lo contrario, si selecciona una hora y no ha seleccionado un día
        determinado, le alerta con una ventana para que haga la selección
        correspondiente.

        Returns
        -------
        None.

        """
        identificador_aula: str = str(self.lista_aulas.value or "")
        dia: str = str(self.lista_dias.value or "")
        
        if identificador_aula == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un aula,
                primero debe seleccionar el aula al que se le aplicarán los
                cambios.
                """
            )
        
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
        elif dia == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un aula,
                primero debe seleccionar el día al que se le aplicarán los
                cambios.
                """
            )
        
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
        
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
    
    def seleccionar_minutos(self, e):
        """
        Funcion "handler" al seleccionar los minutos de una hora.
        
        Si el usuario no seleccionó ningún aula de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.
        
        De lo contrario, si selecciona unos minutos y no ha seleccionado un día
        determinado, le alerta con una ventana para que haga la selección
        correspondiente.

        Returns
        -------
        None.

        """
        identificador_aula: str = str(self.lista_aulas.value or "")
        dia: str = str(self.lista_dias.value or "")
        
        if identificador_aula == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de un aula,
                primero debe seleccionar el aula al que se le aplicarán los
                cambios.
                """
             )
        
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
        
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
        
            # Limpia el campo de texto del aula.
            self.campo_identificador_aula.value = ""
        
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
        10) Btn. mostrar todas las aulas - Btn. mostrar aulas del edificio - Btn. mostrar eq. de aula
        11) Tabla con datos de los aulas

        Returns
        -------
        None.

        """
        self.ui_config = ui_config
        
        self.tabla_actual = TABLA.TODAS_LAS_AULAS
        
        # Fila 0:
        # 0) Título: "Configuración de Aulas de los Edificios"
        self.titulo = ft.Text(
            "Configuración de Aulas de los Edificios",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown de edificios - Drop. de aulas - Botón eliminar aula
        self.lista_edificios = self.crear_lista_edificios()
        self.lista_aulas = self.crear_lista_aulas()
        self.boton_eliminar_aula = ft.Button(
            "Eliminar aula"
        )
        
        # Fila 2:
        # 2) Campo identificador aula - Campo capacidad aula - Btn. agregar aula - Btn. modificar aula
        self.campo_identificador_aula = self.crear_campo_identificador_aula()
        self.campo_capacidad_aula = self.crear_campo_capacidad_aula()
        self.boton_agregar_aula = ft.Button(
            "Agregar aula"
        )
        self.boton_modificar_aula = ft.Button(
            "Modificar aula"
        )
        
        # Fila 3:
        # 3) ----- (linea divisora) -----
        self.linea_0 = self.crear_linea()
        
        # Fila 4:
        # 4) Título: "Equipamiento del Aula"
        self.titulo_equipamiento = ft.Text(
            "Equipamiento del Aula",
            size=20,
            selectable=False
        )
        
        
        # Fila 5:
        # 5) Drop. de equipamiento - Campo de nombre equipamiento - Btn. agregar equipamiento - Btn. eliminar eq.
        self.lista_equipamiento = self.crear_lista_equipamiento()
        self.campo_equipamiento_aula = self.crear_campo_equipamiento_aula()
        self.boton_agregar_equipamiento = ft.Button(
            "Agregar equipamiento"
        )
        self.boton_eliminar_equipamiento = ft.Button(
            "Eliminar equipamiento"
        )
        
        # Fila 6:
        # 6) ----- (linea divisora) -----
        self.linea_1 = self.crear_linea()
        
        # Fila 7:
        # 7) Título: "Horario del Aula"
        self.titulo_horario = ft.Text(
            "Horario del Aula",
            size=20,
            selectable=False
        )
        
        # Fila 8:
        # 8) Drop. con día - Hora apertura - Hora cierre - Btn. establecer horario - Btn. eliminar horario
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
        
        # Fila 9:
        # 9) ----- (linea divisora) -----
        self.linea_2 = self.crear_linea()
        
        # Fila 10:
        # 10) Btn. mostrar todas las aulas - Btn. mostrar aulas del edificio - Btn. mostrar eq. de aula
        self.boton_mostrar_aulas_todas = ft.Button(
            "Mostrar todas las Aulas"
        )
        self.boton_mostrar_aulas_edificio = ft.Button(
            "Mostrar Aulas del Edificio seleccionado"
        )
        self.boton_mostrar_equipamiento_aulas = ft.Button(
            "Mostrar Equipamiento de Aula"
        )
        
        # Fila 11:
        # 11) Tabla con datos de los aulas
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
    
    def cargar_datos_aulas(self): #TODO VERIFICAR porque no lo agarra la lista dropdown
        """
        Carga los datos para la lista de selección de aulas.
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
        for aula in self.ui_config.universidad.aulas_de_edificio(edificio_seleccionado):
            opciones_aulas.append(ft.dropdown.Option(str(aula)))
        self.lista_aulas.options = opciones_aulas
    
    def cargar_datos_equipamiento(self):
        """
        Carga los datos para la lista de selección de equipamiento para un
        aula ya seleccionada.
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO juan
        # Se toman los valores seleccionados por el usuario para cargar la
        # lista de equipamiento disponible en esa aula.
        edificio_seleccionado: str = str(self.lista_edificios.value or "")
        aula_seleccionada: str = str(self.lista_aulas.value or "")
        
        opciones_equipamiento: List[ft.dropdown.Option] = []
        # for equipamiento in self.ui_config.universidad.funcion():
        #     opciones_equipamiento.append(ft.dropdown.Option(str(equipamiento)))
        self.lista_equipamiento.options = opciones_equipamiento
    
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
        edificio_seleccionado: str = str(self.lista_edificios.value or "")
        aula_seleccionada: str = str(self.lista_aulas.value or "")
        
        match self.tabla_actual:
            case TABLA.TODAS_LAS_AULAS:
                self.tabla = generar_tabla(self.ui_config.universidad.mostrar_aulas())
        #    case TABLA.AULAS_POR_EDIFICIO:
        #        self.tabla = generar_tabla(self.ui_config.universidad.mostrar_edificios(
        #            edificio_seleccionado
        #            )
        #        )
        #    case TABLA.EQUIPAMIENTO:
        #        self.tabla = generar_tabla(self.ui_config.universidad.mostrar_equipamiento(
        #            edificio_seleccionado, aula_seleccionada
        #            )
        #        )
            case _:
                self.tabla = generar_tabla(self.ui_config.universidad.mostrar_aulas())
    
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
        edificio_seleccionado: str = str(self.lista_edificios.value or "")
        aula_seleccionada: str = str(self.lista_aulas.value or "")
        
        self.cargar_datos_edificios()
        
        if edificio_seleccionado != "":
            self.cargar_datos_aulas()
        
        if aula_seleccionada != "":
            self.cargar_datos_equipamiento()
        
        self.cargar_datos_tabla()
        
    def crear_lista_edificios(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso de un edificio.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección edificios.

        """
        dropdown = ft.Dropdown(
            label="Edificio",
            options=[],
            enable_filter=True,
        )
        return dropdown
        
    def crear_lista_aulas(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso del aula.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección aulas.

        """
        dropdown = ft.Dropdown(
            label="Aula",
            options=[],
            enable_filter=True,
        )
        return dropdown
        
    def crear_campo_identificador_aula(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso del identificador de un
        aula a crear/agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input del identificador del aula.

        """
        textfield = ft.TextField(
            label="Identificador del aula",
        )
        return textfield
        
    def crear_campo_capacidad_aula(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso de la capacidad de
        un aula a agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input de la capacidad del aula.

        """
        textfield = ft.TextField(
            label="Capacidad",
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
        
    def crear_lista_equipamiento(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso del equipamiento de un aula.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de equipamiento.

        """
        dropdown = ft.Dropdown(
            label="Equipamiento",
            options=[],
            enable_filter=True,
        )
        return dropdown
        
    def crear_campo_equipamiento_aula(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso del nombre de un
        equipamiento a crear/agregar de un aula.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input del nombre del equipamiento.

        """
        textfield = ft.TextField(
            label="Equipamiento del aula",
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
        data = {}
        match self.tabla_actual:
            case TABLA.TODAS_LAS_AULAS:
                data = {
                    "Edificio": [],
                    "Identificador del Aula": [],
                    "Capacidad": [],
                    "Lunes": [],
                    "Martes": [],
                    "Miércoles": [],
                    "Jueves": [],
                    "Viernes": [],
                    "Sábado": [],
                    "Domingo": [],
                }
            case TABLA.AULAS_POR_EDIFICIO:
                data = {
                    "Identificador del Aula": [],
                    "Capacidad": [],
                    "Lunes": [],
                    "Martes": [],
                    "Miércoles": [],
                    "Jueves": [],
                    "Viernes": [],
                    "Sábado": [],
                    "Domingo": [],
                }
            case TABLA.EQUIPAMIENTO:
                data = {
                    "Equipamiento": [],
                }
            case _:
                data = {
                    "Edificio": [],
                    "Identificador del Aula": [],
                    "Capacidad": [],
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
        # TODO (implementar y descomentar)
        # Define el comportamiento "on_click" de cada elemento.
        self.boton_agregar_aula.on_click = self.agregar_aula
        self.boton_modificar_aula.on_click = self.modificar_aula
        self.boton_eliminar_aula.on_click = self.eliminar_aula
        self.boton_agregar_equipamiento.on_click = self.agregar_equipamiento
        self.boton_eliminar_equipamiento.on_click = self.eliminar_equipamiento
        self.boton_establecer_horario.on_click = self.establecer_horario
        # self.boton_eliminar_horario.on_click = self.eliminar_horario
        # self.boton_mostrar_aulas_todas.on_click = self.mostrar_aulas_todas
        # self.boton_mostrar_aulas_edificio.on_click = self.mostrar_aulas_edificio
        # self.boton_mostrar_equipamiento_aulas.on_click = self.mostrar_equipamiento_aulas
        
        # Define el comportamiento "on_change" de cada elemento (listas).
        # self.lista_edificios.on_change = self.seleccionar_edificio
        # self.lista_aulas.on_change = self.seleccionar_aula
        # self.lista_equipamiento.on_change = self.seleccionar_equipamiento
        # self.lista_dias.on_change = self.seleccionar_dia
        # self.lista_hora_apertura.on_change = self.seleccionar_hora
        # self.lista_minutos_apertura.on_change = self.seleccionar_minutos
        # self.lista_hora_apertura.on_change = self.seleccionar_hora
        # self.lista_minutos_cierre.on_change = self.seleccionar_minutos
    
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
        self.fila.append(ft.Row([self.boton_mostrar_aulas_todas, self.boton_mostrar_aulas_edificio, self.boton_mostrar_equipamiento_aulas]))
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
