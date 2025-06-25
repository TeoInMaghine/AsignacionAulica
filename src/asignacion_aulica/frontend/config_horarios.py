# -*- coding: utf-8 -*-
"""
Apartado de configuración para el input y output de datos de los Horarios de
las Actividades/Materias de la Universidad.

@author: Cristian
"""

import flet as ft
from pandas import DataFrame

from typing import List

from .datos import limpiar_texto, generar_tabla
from .alertas import VentanaAlerta, VentanaConfirmacion


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
        nombre_carrera: str = str(self.lista_carreras.value or "")
        identificador_actividad: str = str(self.lista_identificador_actividades.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividades.value or "")
        comision_actividad: str = str(self.lista_comision_actividades.value or "")
        
        # Horario seleccionado por el usuario.
        dia: str = str(self.lista_dias.value or "")
        hora_apertura: str = str(self.lista_hora_apertura.value or "")
        hora_cierre: str = str(self.lista_hora_cierre.value or "")
        minutos_apertura: str = str(self.lista_minutos_apertura.value or "")
        minutos_cierre: str = str(self.lista_minutos_cierre.value or "")
    
        try:
            # Se establece el horario del día elegido de la actividad en la
            # "base de datos".
            # self.ui_config.universidad.modificar_horario_actividad(
            #     nombre_carrera,
            #     identificador_actividad,
            #     nombre_actividad,
            #     comision_actividad,
            #     dia,
            #     int(hora_apertura),
            #     int(hora_cierre),
            #     int(minutos_apertura),
            #     int(minutos_cierre)
            # )
        
            # Se limpia la selección del horario.
            self.limpiar_seleccion_horario()
        
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
    def eliminar_horario(self, e):
        """
        Función "handler" para el click del botón "Eliminar horario".
        
        Elimina el horario de un día elegido para una materia.
        
        Al hacer click, limpia la selección del horario y día, y del aula.

        Returns
        -------
        None.

        """
        # TODO
        # Actividad elegida por el usuario.
        nombre_carrera: str = str(self.lista_carreras.value or "")
        identificador_actividad: str = str(self.lista_identificador_actividades.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividades.value or "")
        comision_actividad: str = str(self.lista_comision_actividades.value or "")
        
        # Horario seleccionado por el usuario.
        dia: str = str(self.lista_dias.value or "")
        hora_apertura: str = str(self.lista_hora_apertura.value or "")
        hora_cierre: str = str(self.lista_hora_cierre.value or "")
        minutos_apertura: str = str(self.lista_minutos_apertura.value or "")
        minutos_cierre: str = str(self.lista_minutos_cierre.value or "")
    
        try:
            # Se establece el horario del día elegido de la actividad en la
            # "base de datos".
            # self.ui_config.universidad.eliminar_horario_actividad(
            #     nombre_carrera,
            #     identificador_actividad,
            #     nombre_actividad,
            #     comision_actividad,
            #     dia,
            #     int(hora_apertura),
            #     int(hora_cierre),
            #     int(minutos_apertura),
            #     int(minutos_cierre)
            # )
        
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
        identificador_actividad: str = str(self.lista_identificador_actividades.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividades.value or "")
        comision_actividad: str = str(self.lista_comision_actividades.value or "")
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
        identificador_actividad: str = str(self.lista_identificador_actividades.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividades.value or "")
        comision_actividad: str = str(self.lista_comision_actividades.value or "")
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
            # TODO
            # Se realiza la asignación automática
            # self.ui_config.universidad.asignacion_automatica()
            
            # Se actualizan los elementos de la interfaz.
            self.actualizar_tabla()
        except Exception as exc:
            mensaje_error: str = str(exc)
            self.alertar(mensaje_error)
    
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
        self.cargar_datos_identificador_actividades()
        self.cargar_datos_nombre_actividades()
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def seleccionar_identificador_actividades(self, e):
        """
        Funcion "handler" al seleccionar un identificador de actividad.
        
        Filtra, cargando los datos de las actividades/materias, las listas de
        selección.

        Returns
        -------
        None.

        """
        # Carga los datos disponibles para esa carrera seleccionada.
        self.cargar_datos_nombre_actividades()
        
        # Si solamente hay una actividad, la selecciona:
        if len(self.lista_nombre_actividades.options) == 1:
            self.lista_nombre_actividades.value = str(self.lista_nombre_actividades.options[0].key)
        
        # Se cargan los datos de comisión disponibles para el nombre,
        # autoseleccionado (si es que lo fue)
        self.cargar_datos_comision_actividades()
        
        # Si solamente hay una comisión, la selecciona:
        if len(self.lista_comision_actividades.options) == 1:
            self.lista_comision_actividades.value = str(self.lista_comision_actividades.options[0].key)
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
    def seleccionar_nombre_actividades(self, e):
        """
        Funcion "handler" al seleccionar un nombre de actividad.
        
        Filtra, cargando los datos de las actividades/materias, las listas de
        selección.

        Returns
        -------
        None.

        """
        # Se cargan los datos de comisión disponibles para el nombre de la
        # actividad seleccionada.
        self.cargar_datos_comision_actividades()
        
        # Si solamente hay una comisión, la selecciona:
        if len(self.lista_comision_actividades.options) == 1:
            self.lista_comision_actividades.value = str(self.lista_comision_actividades.options[0].key)
        
        # Se actualizan los elementos de la interfaz.
        self.actualizar_filas()
        self.actualizar_apartado()
    
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
        identificador_actividad: str = str(self.lista_identificador_actividades.value or "")
        nombre_actividad: str = str(self.lista_nombre_actividades.value or "")
        comision_actividad: str = str(self.lista_comision_actividades.value or "")
        
        # El metodo retorna los atributos en ese orden:
        hora_apertura, minutos_apertura, hora_cierre, minutos_cierre = (
            self.ui_config.universidad.horario_segmentado_actividad(
                nombre_carrera,
                identificador_actividad,
                nombre_actividad,
                comision_actividad,
            )
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
        1) Dropdown carrera
        2) Drop. identificador materia - Drop. Nombre Materia - Drop. Comision Materia
        3) ----- (linea divisora) -----
        4) Título: "Horarios de la actividad"
        3) Drop. con día - Hora apertura - Hora cierre - Btn. establecer horario - Btn. eliminar horario
        4) Titulo: "Asignar aula (opcional):" - Drop. Edificio - Drop Aula - Btn. Asignar aula - Btn. Eliminar asignación
        5) Botón asignar aulas automáticamente (backend)
        6) ----- (linea divisora) -----
        7) Tabla con datos de los horarios de la materia seleccionada
        
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
        # 0) Título: "Configuración de Horarios de cada Actividad/Materia de la Universidad"
        self.titulo = ft.Text(
            value="Configuración de Horarios de cada Actividad/Materia de la Universidad",
            size=20,
            selectable=False
        )
        
        # Fila 1:
        # 1) Dropdown carrera
        self.lista_carreras = self.crear_lista_carreras()
        
        # Fila 2:
        # 2) Drop. identificador materia - Drop. Nombre Materia - Drop. Comision Materia
        self.lista_identificador_actividades = self.crear_lista_identificador_actividades()
        self.lista_nombre_actividades = self.crear_lista_nombre_actividades()
        self.lista_comision_actividades = self.crear_lista_comision_actividades()
        
        # Fila 3:
        self.linea_0 = self.crear_linea()
        
        # Fila 4:
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
        # 9) Tabla con datos de los horarios de la materia seleccionada
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
        # TODO
        opciones_carreras: List[ft.dropdown.Option] = []
        # for carrera in self.ui_config.universidad.nombres_carreras():
        #     opciones_carreras.append(ft.dropdown.Option(str(carrera)))
        self.lista_carreras = self.crear_lista_carreras()
        self.lista_carreras.options = opciones_carreras
    
    def cargar_datos_identificador_actividades(self):
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
        
        self.lista_identificador_actividades = self.crear_lista_identificador_actividades()
        self.lista_identificador_actividades.options = opciones_identificadores
    
    def cargar_datos_nombre_actividades(self):
        """
        Carga los datos para la lista de selección de nombres de actividades.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_seleccionado: str = str(self.lista_identificador_actividades.value or "")
        
        opciones_nombres_actividades: List[ft.dropdown.Option] = []
        
        # Carga los nombres de actividades disponibles para la carrera e
        # identificador seleccionados.
        # En caso de no seleccionar una carrera, que se seleccionen aquellas
        # que no tienen una carrera asignada. (PENSAR)
        # for nombre_actividad in self.ui_config.universidad.obtener_nombre_actividad(carrera_seleccionada, identificador_seleccionado):
        #     opciones_nombres_actividades.append(ft.dropdown.Option(str(nombre_actividad)))
        
        self.lista_nombre_actividades = self.crear_lista_nombre_actividades()
        self.lista_nombre_actividades.options = opciones_nombres_actividades
    
    def cargar_datos_comision_actividades(self):
        """
        Carga los datos para la lista de selección de nombres de actividades.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        carrera_seleccionada: str = str(self.lista_carreras.value or "")
        identificador_seleccionado: str = str(self.lista_identificador_actividades.value or "")
        nombre_actividad_seleccionado: str = str(self.lista_nombre_actividades.value or "")
        
        opciones_comisiones_actividades: List[ft.dropdown.Option] = []
        
        # Carga las comisiones de actividades disponibles para la carrera,
        # identificador y nombre seleccionados.
        # for comision in self.ui_config.universidad.obtener_comision_actividad(
        #         carrera_seleccionada, identificador_seleccionado, nombre_actividad_seleccionado
        #         ):
        #     opciones_comisiones_actividades.append(ft.dropdown.Option(str(comision)))
        
        self.lista_comision_actividades = self.crear_lista_comision_actividades()
        self.lista_comision_actividades.options = opciones_comisiones_actividades
        
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
        Carga los datos para la lista de selección de aulas.
        
        NOTA: NO actualiza los elementos. Simplemente carga los datos. Para
        eso, existen las funciones actualizar_*.

        Returns
        -------
        None.

        """
        # TODO
        edificio_seleccionado: str = str(self.lista_edificios.value or "")
        
        opciones_aulas: List[ft.dropdown.Option] = []
        
        # Carga los nombres de aulas disponibles para el edificio seleccionado.
        for aula in self.ui_config.universidad.obtener_aulas(edificio_seleccionado):
            opciones_aulas.append(ft.dropdown.Option(str(aula)))
        
        self.lista_aulas = self.crear_lista_aulas()
        self.lista_aulas.options = opciones_aulas
    
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
    
    def crear_lista_identificador_actividades(self) -> ft.Dropdown:
        """
        Crea una lista para la selección del identificador de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de carreras.

        """
        dropdown = ft.Dropdown(
            label="Identificador de actividad",
            options=[],
            enable_filter=True,
        )
        return dropdown
    
    def crear_lista_nombre_actividades(self) -> ft.Dropdown:
        """
        Crea una lista para la selección del nombre de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de nombre de actividad.

        """
        dropdown = ft.Dropdown(
            label="Nombre de la actividad",
            options=[],
            enable_filter=True,
        )
        return dropdown
    
    def crear_lista_comision_actividades(self) -> ft.Dropdown:
        """
        Crea una lista para la selección de la comisión de la actividad.

        Returns
        -------
        dropdown : ft.Dropdown
            Lista de selección de comisión de actividad.

        """
        dropdown = ft.Dropdown(
            label="Comisión de la actividad",
            options=[],
            enable_filter=True,
        )
        return dropdown
    
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
        # TODO (descomentar)
        # Define el comportamiento "on_click" de cada elemento.
        self.boton_establecer_horario.on_click = self.establecer_horario
        self.boton_eliminar_horario.on_click = self.eliminar_horario
        self.boton_asignar_aula.on_click = self.asignar_aula
        self.boton_eliminar_asignacion_aula.on_click = self.eliminar_asignacion_aula
        self.boton_asignar_automaticamente.on_click = self.handler_asignar_automaticamente
        
        # Define el comportamiento "on_change" de cada elemento (listas).
        self.lista_carreras.on_change = self.seleccionar_carrera
        self.lista_identificador_actividades.on_change = self.seleccionar_identificador_actividades
        self.lista_nombre_actividades.on_change = self.seleccionar_nombre_actividades
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
        self.fila.append(ft.Row([self.lista_carreras]))
        self.fila.append(ft.Row([self.lista_identificador_actividades, self.lista_nombre_actividades, self.lista_comision_actividades]))
        self.fila.append(ft.Row([self.linea_0]))
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
