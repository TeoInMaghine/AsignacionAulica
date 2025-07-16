# -*- coding: utf-8 -*-
"""
Apartado de configuración para el input y output de datos de los Horarios de
las Actividades/Materias de la Universidad.

@author: Cristian
"""

import traceback
import flet as ft
from pandas import DataFrame

from typing import List

from .datos import limpiar_texto, generar_tabla
from .alertas import VentanaAlerta, VentanaConfirmacion


class TABLA():
    # Luego ver si se necesita alguna más...
    HORARIOS = "horarios"
    EQUIPAMIENTO = "equipamiento"
    

class UI_Config_Horarios():
    """
    Apartado de Horarios de las Actividades/Materias de la universidad.
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
    
    def limpiar_seleccion_horario(self):
        """
        Limpia la selección del horario, quitando las opciones elegidas dentro
        de los dropdowns.

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
    
    def establecer_horario(self, e):
        """
        Función "handler" para el click del botón "Establecer horario".
        
        Establece el horario de un día elegido para una materia. (No tiene en
        cuenta el aula asignada para la misma).
        
        Al hacer click, limpia la selección del horario y día.

        Returns
        -------
        None.

        """
        # TODO
        # Actividad elegida por el usuario.
        #nombre_carrera: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        
        # Horario seleccionado por el usuario.
        dia: str = str(self.lista_dias.value or "")
        hora_apertura: str = str(self.lista_hora_apertura.value or "")
        hora_cierre: str = str(self.lista_hora_cierre.value or "")
        minutos_apertura: str = str(self.lista_minutos_apertura.value or "")
        minutos_cierre: str = str(self.lista_minutos_cierre.value or "")
    
        try:
            # Se establece el horario del día elegido de la actividad en la
            # "base de datos".
            self.ui_config.universidad.modificar_horario(
                nombre_actividad,
                dia,
                int(hora_apertura),
                int(hora_cierre),
                int(minutos_apertura),
                int(minutos_cierre),
            )
        
            # Se limpia la selección del horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_horario(self, e):  # TODO modificar eliminar_horario para discriminar por carrera
        """
        Función "handler" para el click del botón "Eliminar horario".
        
        Elimina el horario de un día elegido para una materia.
        
        Al hacer click, limpia la selección del horario y día, y del aula.

        Returns
        -------
        None.

        """
        # Actividad elegida por el usuario.
        nombre_carrera: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        
        # Horario seleccionado por el usuario.
        dia: str = str(self.lista_dias.value or "")

        try:
            # Se establece el horario del día elegido de la actividad en la
            # "base de datos".
            self.ui_config.universidad.eliminar_horario(nombre_actividad,dia)
        
            # Se limpia la selección del horario.
            self.limpiar_seleccion_horario()
            
            # Se limpia la selección de aula y edificio.
            self.lista_aulas.value = ""
            self.lista_edificios.value = ""
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def asignar_aula(self, e):
        """
        Función "handler" para el click del botón "Asignar aula".
        
        Asigna un aula manualmente para el horario de una actividad.

        Returns
        -------
        None.

        """
        # TODO
        # Actividad elegida por el usuario.
        nombre_carrera: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aulas: str = str(self.lista_aulas.value or "")
        
        # Horario seleccionado por el usuario.
        dia: str = str(self.lista_dias.value or "")
        # Si se necesitan, descomentar, sino eliminar:
        # hora_apertura: str = str(self.lista_hora_apertura.value or "")
        # hora_cierre: str = str(self.lista_hora_cierre.value or "")
        # minutos_apertura: str = str(self.lista_minutos_apertura.value or "")
        # minutos_cierre: str = str(self.lista_minutos_cierre.value or "")
    
        try:
            # Se asigna manualmente el aula para ese horario de la actividad en
            # la "base de datos".
            # self.ui_config.universidad.asignar_manualmente_aula_actividad(
            #     nombre_carrera,
            #     identificador_actividad,
            #     nombre_actividad,
            #     comision_actividad,
            #     nombre_edificio,
            #     nombre_aula,
            #     dia,
            # )
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_asignacion_aula(self, e):
        """
        Función "handler" para el click del botón "Asignar aula".
        
        Asigna un aula manualmente para el horario de una actividad.
        
        Limpia la selección del aula.

        Returns
        -------
        None.

        """
        # TODO
        # Actividad elegida por el usuario.
        nombre_carrera: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        nombre_edificio: str = str(self.lista_edificios.value or "")
        nombre_aulas: str = str(self.lista_aulas.value or "")
        
        # Horario seleccionado por el usuario.
        dia: str = str(self.lista_dias.value or "")
        # Si se necesitan, descomentar, sino eliminar:
        # hora_apertura: str = str(self.lista_hora_apertura.value or "")
        # hora_cierre: str = str(self.lista_hora_cierre.value or "")
        # minutos_apertura: str = str(self.lista_minutos_apertura.value or "")
        # minutos_cierre: str = str(self.lista_minutos_cierre.value or "")
    
        try:
            # Se asigna manualmente el aula para ese horario de la actividad en
            # la "base de datos".
            # self.ui_config.universidad.eliminar_asignacion_aula_actividad(
            #     nombre_carrera,
            #     identificador_actividad,
            #     nombre_actividad,
            #     comision_actividad,
            #     nombre_edificio,
            #     nombre_aula,
            #     dia,
            # )
            
            # Se limpia la selección de aula y edificio.
            self.lista_aulas.value = ""
            self.lista_edificios.value = ""
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def handler_asignar_automaticamente(self, e):
        """
        Función "handler" para el click del botón de asignación automática de
        aulas.
        
        Abre una ventana que le informa al usuario que se utilizarán todas las
        actividades ingresadas para elegir las aulas a las materias,
        dependiendo de las preferencias edificios que tengan las carreras y los
        horarios establecidos para cada actividad.

        Returns
        -------
        None.

        """
        mensaje: str = """
            A continuación, para cada actividad/materia que haya agregado al sistema
            se le asignará automáticamente el aula más conveniente según su edificio
            de preferencia, capacidad, equipamiento y horario establecido.
            Es importante que a cada actividad que haya creado le haya asignado el
            horario correcto en el que se desarrollará la actividad, para que el
            programa pueda elegir qué aula utilizar para la misma.
            ¿Desea proceder con la asignación automática?
            (podrá modificar cada asignación manualmente más tarde).
        """
        VentanaConfirmacion(self.ui_config.page, mensaje, self.asignar_automaticamente)
    
    def asignar_automaticamente(self):
        """
        Función de confirmación para la asignación automática de aulas (parte
        backend).
        
        Realiza la asignación automática o abre una ventana de alerta en caso
        de error.

        Returns
        -------
        None.

        """
        print("Se realizará asignación automatica...")
        
        try:
            print("Boton de asignacion de los chicos activado")
            
            # Se realiza la asignación automática
            self.ui_config.universidad.asignacion_automatica()

            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            print(traceback.format_exc())
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def agregar_equipamiento(self, e):  #TODO
        """
        Función "handler" para el click del botón "Agregar equipamiento".
        
        Agrega el equipamiento del campo de texto a la actividad seleccionada
        dentro de la "base de datos".
        
        Al hacer click, limpia la selección y todos los campos.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.
    
        Returns
        -------
        None.
    
        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        nombre_equipamiento: str = str(self.campo_equipamiento.value or "")
        
        try:
            # Se agrega el equipamiento a la actividad de la "base de datos".
            # self.ui_config.universidad.agregar_equipamiento(
            #     carrera_seleccionada,
            #     identificador_seleccionado,
            #     nombre_actividad_seleccionado,
            #     nombre_comision_seleccionado,
            # )
            
            # Si es que no hay ningún problema:
            # Limpia las selecciones.
            self.lista_equipamiento.value = ""
            
            # Limpia los campos.
            self.campo_equipamiento.value = ""
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_equipamiento(self, e): #TODO
        """
        Función "handler" para el click del botón "Eliminar equipamiento".
        
        Elimina el equipamiento seleccionado de la lista, a la actividad
        seleccionada dentro de la "base de datos".
        
        Al hacer click, limpia la selección y todos los campos.
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.
    
        Returns
        -------
        None.
    
        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        nombre_equipamiento: str = str(self.campo_equipamiento.value or "")
        
        try:
            # Se agrega el equipamiento a la actividad de la "base de datos".
            # self.ui_config.universidad.agregar_equipamiento(
            #     carrera_seleccionada,
            #     identificador_seleccionado,
            #     nombre_actividad_seleccionado,
            #     nombre_comision_seleccionado,
            # )
            
            # Si es que no hay ningún problema:
            # Limpia las selecciones.
            self.lista_equipamiento.value = ""
            
            # Limpia los campos.
            self.campo_equipamiento.value = ""
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_todo()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
        
    def mostrar_horarios(self, e):
        """
        Función "handler" para el click del botón "Mostrar horarios".
        
        Muestra en la tabla todos los horarios de las actividades de la "base
        de datos".
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.
    
        Returns
        -------
        None.
    
        """
        self.tabla_actual = TABLA.HORARIOS
        
        self.actualizar_tabla()
    
    def mostrar_equipamiento(self, e): #TODO
        """
        Función "handler" para el click del botón "Mostrar equipamiento".
        
        Muestra en la tabla todos los equipamientos de la actividad
        seleccionada de la "base de datos".
        
        Nota: limpia el input del usuario de símbolos como '@', '!' y espacios
        innecesarios.
    
        Returns
        -------
        None.
    
        """
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        
        # LA IMPLEMENTACION ES CHARLABLE, LO PODES MODIFICAR COMO TE PAREZCA MEJOR
        # if self.ui_config.universidad.existe_actividad(
        #         carrera_seleccionada,
        #         identificador_seleccionado,
        #         nombre_actividad_seleccionado,
        #         nombre_comision_seleccionado
        #     ):
        #     self.tabla_actual = TABLA.EQUIPAMIENTO
        
        self.actualizar_tabla()
    
    def seleccionar_carrera(self, e):
        """
        Funcion "handler" al seleccionar una carrera.
        
        Filtra, cargando los datos de las actividades/materias, las listas de
        selección.

        Returns
        -------
        None.

        """
        # Carga los datos disponibles para esa carrera seleccionada.
        self.cargar_datos_nombre_actividades()
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def seleccionar_nombre_actividad(self, e):
        """
        Funcion "handler" al seleccionar una carrera.
        
        Filtra, cargando los datos de las actividades/materias, las listas de
        selección.

        Returns
        -------
        None.

        """
        # Se autoselecciona la cantidad de alumnos que había cargado en la
        # "base de datos".
        self.actualizar_cant_alumnos()
    
    def seleccionar_cant_alumnos(self, e):
        """
        Funcion "handler" al seleccionar la cantidad de alumnos de una
        actividad.
        
        Establece la cantidad de alumnos para esa clase.

        Returns
        -------
        None.

        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        actividad_seleccionada: str = str(self.lista_nombre_actividad or "")
        cant_alumnos: str = str(self.lista_cant_alumnos or "")
        
        try:
            # Se establece la cantidad de alumnos para una clase en la "base de
            # datos".
            # self.ui_config.universidad.establecer_cant_alumnos(
            #     carrera_seleccionada,
            #     actividad_seleccionada,
            #     cant_alumnos,
            # )
            
            # Se actualizan los valores cargados en la tabla.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def seleccionar_dia(self, e):
        """
        Funcion "handler" al seleccionar un día de la selección de horario.
        
        Si la actividad posee un horario establecido para un día determinado,
        al seleccionarlo autoselecciona los demás valores cargados. Caso
        contrario, los limpia.

        Returns
        -------
        None.

        """
        # TODO
        # Actividad elegida por el usuario.
        nombre_carrera: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        
        # El metodo retorna los atributos en ese orden:
        # hora_apertura, minutos_apertura, hora_cierre, minutos_cierre = (
        #     self.ui_config.universidad.horario_segmentado_actividad(
        #         nombre_carrera,
        #         identificador_actividad,
        #         nombre_actividad,
        #         comision_actividad,
        #     )
        # )
        
        # "Autoselecciona" o muestra el horario del edificio para el día
        # elegido.
        # self.lista_hora_apertura.value = hora_apertura
        # self.lista_hora_cierre.value = hora_cierre
        # self.lista_minutos_apertura.value = minutos_apertura
        # self.lista_minutos_cierre.value = minutos_cierre
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def seleccionar_hora(self, e):
        """
        Funcion "handler" al seleccionar la hora.
        
        Si el usuario no seleccionó ningún día de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.

        Returns
        -------
        None.

        """
        dia: str = str(self.lista_dias.value or "")
        
        if dia == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de una actividad,
                primero debe seleccionar el día al que se le aplicarán los
                cambios.
                """
             )
            
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
    
    def seleccionar_minutos(self, e):
        """
        Funcion "handler" al seleccionar los minutos de una hora.
        
        Si el usuario no seleccionó ningún día de la lista de selección,
        le alerta con una ventana para que haga la selección correspondiente.

        Returns
        -------
        None.

        """
        dia: str = str(self.lista_dias.value or "")
        
        if dia == "":
            self.alertar(
                """
                Para poder seleccionar y establecer el horario de una actividad,
                primero debe seleccionar el día al que se le aplicarán los
                cambios.
                """
             )
            
            # Limpia las listas de selección de horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_filas()
            self.actualizar_apartado()
    
    def seleccionar_edificios(self, e):
        """
        Funcion "handler" al seleccionar un edificio.

        Returns
        -------
        None.

        """
        self.cargar_datos_aulas()
    
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def __init__(
            self,
            ui_config
            ):
        """
        Crea el apartado de horarios de las actividades/materias de la
        universidad.
        
        Layout (por filas):
        -----------------------------------------------------------------------
        0) Título: "Configuración de Horarios de cada Actividad/Materia de la Universidad"
        1) Dropdown carrera - Drop. nombre materia
        2) ----- (linea divisora) -----
        3) Título: "Cantidad de alumnos para la clase:" - Drop. Cantidad de alumnos
        4) Título: "Horarios de la actividad"
        5) Drop. con día - Hora apertura - Hora cierre - Btn. establecer horario - Btn. eliminar horario
        6) Titulo: "Asignar aula (opcional):" - Drop. Edificio - Drop Aula - Btn. Asignar aula - Btn. Eliminar asignación
        7) Botón asignar aulas automáticamente (backend)
        8) Drop. equipamiento - Campo equipamiento - Btn. Agregar equipamiento - Btn. Eliminar equipamiento
        9) ----- (linea divisora) -----
        10) Tabla con datos de los horarios de la materia seleccionada
        
        Parameters
        ----------
        ui_config : UI_Config
            Referencia al contenedor "padre" de todos los demás apartados.

        Returns
        -------
        None.

        """
        self.ui_config = ui_config
        self.tabla_actual: str = TABLA.HORARIOS
        
        # Fila 0:
        # 0) Título: "Configuración de Horarios de cada Actividad/Materia de la Universidad"
        self.titulo = ft.Text(
            value="Configuración de Horarios de cada Actividad/Materia de la Universidad",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown carrera - Drop. nombre materia
        self.lista_carreras = self.crear_lista_carreras()
        self.lista_nombre_actividad = self.crear_lista_nombre_actividad()
        
        # Fila 2:  
        # 2) ----- (linea divisora) -----
        self.linea_0 = self.crear_linea()
        
        # Fila 2:
        # 3) Título: "Cantidad de alumnos para la clase:" - Drop. Cantidad de alumnos
        self.titulo_alumnos = ft.Text(
            value="Cantidad de alumnos para la clase:",
            size=20,
            selectable=False
        )
        self.lista_cant_alumnos = self.crear_lista_cant_alumnos()
        
        # Fila 4:
        # 4) Título: "Horarios de la actividad"
        self.titulo_horario = ft.Text(
            value="Horarios de la actividad",
            size=20,
            selectable=False
        )
        
        # Fila 5:
        # 5) Drop. con día - Hora apertura - Hora cierre - Btn. establecer horario - Btn. eliminar horario
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
        
        # Fila 6:
        # 6) Titulo: "Asignar aula (opcional):" - Drop. Edificio - Drop Aula - Btn. Asignar aula - Btn. Eliminar asignación
        self.titulo_aula_opcional = ft.Text(
            value="Asignar aula (opcional):",
            size=20,
            selectable=False
        )
        self.lista_edificios = self.crear_lista_edificios()
        self.lista_aulas = self.crear_lista_aulas()
        self.boton_asignar_aula = ft.Button(
            text="Asignar aula",
        )
        self.boton_eliminar_asignacion_aula = ft.Button(
            text="Eliminar asignación",
        )
        
        # Fila 7:
        # 7) Botón asignar aulas automáticamente (backend)
        self.boton_asignar_automaticamente = ft.Button(
            text="Asignar automáticamente aulas para todas las actividades",
        )
        
        # Fila 8:
        # 8) ----- (linea divisora) -----
        self.linea_1 = self.crear_linea()
        
        # Fila 9:
        # 9) Drop. Equipamiento - Campo equipamiento - Btn. Agregar equipamiento - Btn. Eliminar equipamiento
        self.lista_equipamiento = self.crear_lista_equipamiento()
        self.campo_equipamiento = self.crear_campo_equipamiento()
        self.boton_agregar_equipamiento = ft.Button(
            text="Agregar equipamiento",
        )
        self.boton_eliminar_equipamiento = ft.Button(
            text="Eliminar equipamiento",
        )
        
        # Fila 10:
        # 10) Btn. Mostrar actividades - Btn. Mostrar equipamiento
        self.boton_mostrar_actividades = ft.Button(
            text="Mostrar horarios",
        )
        self.boton_mostrar_equipamiento = ft.Button(
            text="Mostrar equipamiento",
        )
        # Fila 11:
        # 11) ----- (linea divisora) -----
        self.linea_2 = self.crear_linea()
        
        # Fila 12:
        # 12) Tabla con datos de los horarios de la materia seleccionada
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
        
        self.lista_carreras.options = opciones_carreras
    
    def cargar_datos_identificador_actividades(self): #TODO when we go back to segmented things, maybe. Por ahora no sirve
        """
        Carga los datos para la lista de selección de identificador de
        actividades.
        
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
        
        
        self.lista_identificador_actividad.options = opciones_identificadores
    
    def cargar_datos_nombre_actividades(self): #TODO discriminar por carrera
        """
        Carga los datos para la lista de selección de nombres de actividades.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        
        opciones_nombres_actividades: List[ft.dropdown.Option] = []
        
        # Carga los nombres de actividades disponibles para la carrera e
        # identificador seleccionados.
        # En caso de no seleccionar una carrera, que se seleccionen aquellas
        # que no tienen una carrera asignada. (PENSAR)
        #for nombre_actividad in self.ui_config.universidad.nombres_materias_concatenados(): # Implementar luego
        
        for nombre_actividad in self.ui_config.universidad.nombres_horarios():
            opciones_nombres_actividades.append(ft.dropdown.Option(str(nombre_actividad)))
        
        
        self.lista_nombre_actividad.options = opciones_nombres_actividades
        
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
        
        self.lista_edificios.options = opciones_edificios
    
    def cargar_datos_aulas(self):  #TODO  # Ver porque el dropdown no agarra esto
        """
        Carga los datos para la lista de selección de aulas.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        edificio_seleccionado: str = str(self.lista_edificios.value or "")
        opciones_aulas: List[ft.dropdown.Option] = []
        
        # Carga los nombres de aulas disponibles para el edificio seleccionado.
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
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividad.value or "")
        dia_seleccionado: str = str(self.lista_dias.value or "")
        
        opciones_equipamiento: List[ft.dropdown.Option] = []
        # for equipamiento in self.ui_config.universidad.funcion():
        #     opciones_equipamiento.append(ft.dropdown.Option(str(equipamiento)))
        
        self.lista_equipamiento.options = opciones_equipamiento
    
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
        self.tabla = generar_tabla(self.ui_config.universidad.mostrar_horarios())
    
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
        self.cargar_datos_nombre_actividades()
        self.cargar_datos_edificios()
        self.cargar_datos_aulas()
        self.cargar_datos_equipamiento()
        self.cargar_datos_tabla()
    
    def crear_lista_carreras(self) -> ft.Dropdown:
        """
        Crea una lista para la selección de la carrera.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de carreras.

        """
        dropdown = ft.Dropdown(
            label="Carrera",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=500,
        )
        return dropdown
    
    def crear_lista_nombre_actividad(self) -> ft.Dropdown:
        """
        Crea una lista para la selección del identificador de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de carreras.

        """
        dropdown = ft.Dropdown(
            label="Nombre de la actividad",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=500
        )
        return dropdown
    
    def crear_lista_cant_alumnos(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso de la cantidad de alumnos de la
        actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de la cantidad de alumnos de la actividad.

        """
        dropdown = ft.Dropdown(
            label="Cantidad de alumnos",
            options=[
                ft.dropdown.Option(f"{i}") for i in range(10, 130, 10)
            ],
            enable_filter=True,
            editable=True,
            menu_height=300,
        )
        return dropdown
    
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
            editable=True
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
            editable=True,
            menu_height=300,
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
            editable=True,
            menu_height=300,
        )
        return dropdown
    
    def crear_lista_equipamiento(self) -> ft.Dropdown:
        """
        Crea una lista para el ingreso de el equipamiento de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección del equipamiento de la actividad.

        """
        dropdown = ft.Dropdown(
            label="Equipamiento",
            options=[],
            enable_filter=True,
            editable=True,
            menu_height=200
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
    
    def crear_campo_equipamiento(self) -> ft.TextField:
        """
        Crea el elemento de campo de texto para ingreso del equipamiento de la
        actividad a crear/agregar.

        Returns
        -------
        textfield : ft.TextField
            Campo de texto para el input del equipamiento de la actividad.

        """
        textfield = ft.TextField(
            label="Equipamiento",
        )
        return textfield
    
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
            case TABLA.HORARIOS:
                data = {
                    "Aula": [],
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
                    "Aula": [],
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
        # Define el comportamiento "on_click" de cada elemento.
        self.boton_establecer_horario.on_click = self.establecer_horario
        self.boton_eliminar_horario.on_click = self.eliminar_horario
        self.boton_asignar_aula.on_click = self.asignar_aula
        self.boton_eliminar_asignacion_aula.on_click = self.eliminar_asignacion_aula
        self.boton_asignar_automaticamente.on_click = self.handler_asignar_automaticamente
        self.boton_agregar_equipamiento.on_click = self.agregar_equipamiento
        self.boton_eliminar_equipamiento.on_click = self.eliminar_equipamiento
        
        # Define el comportamiento "on_change" de cada elemento (listas).
        self.lista_carreras.on_change = self.seleccionar_carrera
        self.lista_cant_alumnos.on_change = self.seleccionar_cant_alumnos
        self.lista_dias.on_change = self.seleccionar_dia
        self.lista_hora_apertura.on_change = self.seleccionar_hora
        self.lista_minutos_apertura.on_change = self.seleccionar_minutos
        self.lista_hora_cierre.on_change = self.seleccionar_hora
        self.lista_minutos_cierre.on_change = self.seleccionar_minutos
        self.lista_edificios.on_change = self.seleccionar_edificios
    
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
        self.fila.append(ft.Row([self.lista_carreras, self.lista_nombre_actividad]))
        self.fila.append(ft.Row([self.linea_0]))
        self.fila.append(ft.Row([self.titulo_alumnos, self.lista_cant_alumnos]))
        self.fila.append(ft.Row([self.titulo_horario]))
        self.fila.append(ft.Row([
            self.lista_dias,
            self.lista_hora_apertura, self.separador_0,self.lista_minutos_apertura,
            self.separador_1,
            self.lista_hora_cierre, self.separador_2, self.lista_minutos_cierre,
            self.boton_establecer_horario,self.boton_eliminar_horario
        ]))
        self.fila.append(ft.Row([self.titulo_aula_opcional, self.lista_edificios, self.lista_aulas, self.boton_asignar_aula, self.boton_eliminar_asignacion_aula]))
        self.fila.append(ft.Row([self.boton_asignar_automaticamente]))
        self.fila.append(ft.Row([self.linea_1]))
        self.fila.append(ft.Row([self.lista_equipamiento, self.campo_equipamiento, self.boton_agregar_equipamiento, self.boton_eliminar_equipamiento]))
        self.fila.append(ft.Row([self.linea_2]))
        self.fila.append(ft.Row([self.boton_mostrar_actividades, self.boton_mostrar_equipamiento]))
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
    
    def actualizar_cant_alumnos(self):
        """
        Actualiza la lista de cantidad de alumnos en la interfaz.

        Returns
        -------
        None.

        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        actividad_seleccionada: str = str(self.lista_nombre_actividad or "")
        
        # Se carga la cantidad de alumnos que se había ingresado en la "base de
        # datos" y se autoselecciona en la lista de cantidad de alumnos.
        # NOTA: Se espera que retorne un string con la cantidad de alumnos
        # (número entero) o sino un string vacío ("").
        cant_alumnos: str = str(self.ui_config.universidad.cargar_cant_alumnos(
                carrera_seleccionada,
                actividad_seleccionada,
            )
        )
        
        # Se autoselecciona el valor en el dropdown.
        self.lista_cant_alumnos.value = cant_alumnos
    
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
        
    
    def actualizar_lista_aulas(self):
        """
        Actualiza la lista de edificios en la interfaz.

        Returns
        -------
        None.

        """
        # Se cargan todos los nombres de los edificios.
        self.cargar_datos_aulas()
        
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
