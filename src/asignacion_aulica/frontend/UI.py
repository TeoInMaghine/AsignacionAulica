# -*- coding: utf-8 -*-
"""
Proyecto de Ingeniería de Software
Grupo Asignación Áulica
Parte "FrontEnd" - Interfaz Gráfica de Usuario (GUI)
@author: Cristian Mogensen
"""

import flet as ft

from .colores import COLOR
from .menu import UI_Menu
from .config import UI_Config
from .universidad import Universidad


def main(page: ft.Page):
    """
    Función main de entrada o de ejecución al programa. Se ejecuta con flet
    utilizando:
        ft.app(main)
        
    Título: "UNRN Andina - Asignación de Aulas"
    Dimensiones de ventana: 1280x720 px (mínimo)

    Parameters
    ----------
    page : ft.Page
        Page principal de la app. (no hace falta incluirlo al ejecutarlo con
        ft.app)

    Returns
    -------
    None.

    """
    
    # Página/ft.Page principal
    page.title = "UNRN Andina - Asignación de Aulas" # Título de la ventana
    page.theme_mode = ft.ThemeMode.LIGHT # Tema claro
    page.padding = 0 # Quita el padding entre elementos
    page.spacing = 0 # Quita espaciado
    page.alignment = ft.alignment.top_left # Alineamiento
    page.vertical_alignment = ft.MainAxisAlignment.START # Alineamiento vertical
    page.horizontal_alignment = ft.CrossAxisAlignment.START # Alineamiento horizontal
    page.window_width = 1280 # Ancho de la ventana
    page.window_height = 720 # Alto de la ventana
    page._set_attr("windowMinWidth", 1280) # Ancho mínimo de la ventana
    page._set_attr("windowMinHeight", 720) # Alto mínimo de la ventana
    page.window.maximized = True # Maximiza la ventana
    
    # Fuente de la app
    page.fonts = {
        "Karla": "fonts/Karla-Regular.ttf",
        "Open Sans": "fonts/OpenSans-Regular.ttf",
        "Open Sans Condensed": "fonts/OpenSans_Condensed-Regular.ttf"
    }
    page.theme = ft.Theme(font_family="Karla")  # Font de la App por default
    
    universidad = Universidad()
    menu = UI_Menu(universidad, page) # Menú de archivo...
    config = UI_Config(universidad, page) # Menú de configuración (edificios, aulas, ...)
    
    UI_interfaz = ft.Row(
        controls=[
            menu.dibujar(),
            config.dibujar()
        ],
        spacing=0,
        expand=True
    )
    
    page.add(UI_interfaz) # Se agrega el contenido a la ventana
    
    page.update()

