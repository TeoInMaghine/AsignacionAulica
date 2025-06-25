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

# Apartados:
from .config_edificios import UI_Config_Edificios
from .config_aulas import UI_Config_Aulas
from .config_aulas_dobles import UI_Config_Aulas_Dobles
from .config_carreras import UI_Config_Carreras
from .config_actividades import UI_Config_Actividades
from .config_horarios import UI_Config_Horarios

from .colores import COLOR


class UI_BotonConfig():
    """
    Botón para cambiar de apartado. Por ejemplo: Edificios, Aulas, ...
    """
    def cambiar_apartado(self, e):
        """
        Le indica al contenedor "padre" de los apartados, que debe cambiar
        de apartado.

        Returns
        -------
        None.

        """
        self.ui_config.cambiar_apartado(self.referencia)
    
    def __init__(
            self,
            ui_config, # UI_Config
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
        self.ui_config = ui_config
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
            on_click=self.cambiar_apartado,
            height=self.tamanio_alto,
            border_radius=16,
        )
        
    def dibujar(self) -> ft.Container:
        return self.boton


class APARTADO():
    EDIFICIOS = "edificios"
    AULAS = "aulas"
    AULAS_DOBLES = "aulas_dobles"
    CARRERAS = "carreras"
    ACTIVIDADES = "actividades"
    HORARIOS = "horarios"


class UI_Config():
    """
    Apartado 'Padre', con todos los apartados de la configuración.
    """
    def __init__(
            self,
            universidad,
            page: ft.Page
            ):
        self.universidad = universidad
        self.page = page
        
        # Botones para configurar cada apartado.
        self.btn_edificios = UI_BotonConfig(self, "Edificios", APARTADO.EDIFICIOS)
        self.btn_aulas = UI_BotonConfig(self, "Aulas", APARTADO.AULAS)
        self.btn_aulas_dobles = UI_BotonConfig(self, "Aulas \"Dobles\"", APARTADO.AULAS_DOBLES)
        self.btn_carreras = UI_BotonConfig(self, "Carreras", APARTADO.CARRERAS)
        self.btn_actividades = UI_BotonConfig(self, "Actividades/materias", APARTADO.ACTIVIDADES)
        self.btn_horarios = UI_BotonConfig(self, "Horarios", APARTADO.HORARIOS)
        
        self.fila_botones = ft.Row(
            [
                self.btn_edificios.dibujar(),
                self.btn_aulas.dibujar(),
                self.btn_aulas_dobles.dibujar(),
                self.btn_carreras.dibujar(),
                self.btn_actividades.dibujar(),
                self.btn_horarios.dibujar()
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing = 10,
            scroll=ft.ScrollMode.AUTO,
        )
        
        self.apartado_edificios = UI_Config_Edificios(self)
        self.apartado_aulas = UI_Config_Aulas(self)
        self.apartado_aulas_dobles = UI_Config_Aulas_Dobles(self)
        self.apartado_carreras = UI_Config_Carreras(self)
        self.apartado_actividades = UI_Config_Actividades(self)
        self.apartado_horarios = UI_Config_Horarios(self)
        
        self.apartado = self.apartado_edificios
        
        self.menu_config = ft.Column(
            [
                self.fila_botones,
                self.apartado.dibujar()
            ],
            alignment=ft.MainAxisAlignment.START,
        )
        
        self.container = ft.Container(
            content=self.menu_config,
            alignment=ft.alignment.top_left,
            padding=20,
            expand=False,
            #border=ft.border.all(1, "black") # esto es para hacer un borde negro y ver bien como se distribuyen los elementos, hay que borrarlo cuando ya esté una versión "estable"
        )
    
    def actualizar_apartado(self):
        """
        Actualiza el cambio de apartado.
        
        Recarga los datos para evitar inconsistencias y actualiza los elementos
        de la interfaz.

        Returns
        -------
        None.

        """
        # Se actualizan los datos que deben cargar inicialmente los apartados,
        # para no generar inconsistencias al agregar, eliminar o modificar
        # datos relacionados en diferentes apartados.
        self.apartado.cargar_datos_inicio()
        self.apartado.actualizar_filas()
        
        # Se actualizan los elementos de la vista actual.
        self.menu_config.controls.clear()
        self.menu_config.controls.append(self.fila_botones)
        self.menu_config.controls.append(self.apartado.dibujar())
        self.menu_config.update()
        self.page.update()
    
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
            case APARTADO.AULAS_DOBLES:
                self.apartado = self.apartado_aulas_dobles
            case APARTADO.CARRERAS:
                self.apartado = self.apartado_carreras
            case APARTADO.ACTIVIDADES:
                self.apartado = self.apartado_actividades
            case APARTADO.HORARIOS:
                self.apartado = self.apartado_horarios
            case _:
                self.apartado = self.apartado_edificios
        self.actualizar_apartado()
    
    def dibujar(self) -> ft.Container:
        return self.container
