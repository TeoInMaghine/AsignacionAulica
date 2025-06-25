# -*- coding: utf-8 -*-
"""
Menú encargado de la creación y apertura de archivos. Incluye:
    - Menu
    - Nuevo archivo
    - Abrir archivo
    - Guardar archivo
    - Importar archivo (excel, csv, ...)
    - Exportar archivo (a excel, csv, ...)

@author: Cristian
"""

import flet as ft

from .colores import COLOR
from .archivos import nuevo_archivo, abrir_archivo, guardar_archivo, importar_archivo, exportar_archivo 
from .universidad import Universidad


class UI_UNRN:
    """
    Ícono de la UNRN. (va en el panel izquierdo de la UI)
    """
    def __init__(self, ruta_imagen: str):
        # Directorio donde se encuentra la imágen del icono.
        self.ruta_imagen: str = ruta_imagen
        self.tamanio_imagen: int = 225
        self.tamanio_container: int = 250
        self.padding: int = self.tamanio_container - self.tamanio_imagen
        
        self.icono = ft.Image(
            src=self.ruta_imagen,
            width=self.tamanio_imagen,
            height=self.tamanio_imagen,
            fit=ft.ImageFit.CONTAIN
        )
        self.container = ft.Container(
            content=self.icono,
            alignment=ft.alignment.top_center,
            width=self.tamanio_container,
            height=self.tamanio_imagen,
            padding=ft.Padding(
                left=self.padding,
                top=0,
                right=self.padding,
                bottom=0
            )
        )

    def dibujar(self) -> ft.Container:
        return self.container


class UI_MenuBoton:
    """
    Botón de archivo del panel izquierdo de la UI. Sirve para archivo nuevo,
    abrir, exportar, ...
    """
    def __init__(
            self,
            ruta_imagen: str,
            texto: str,
            onclick
            ):
        # Directorio donde se encuentra la imágen del icono del boton.
        self.ruta_imagen: str = ruta_imagen
        # Texto que dirá el botón. Por ejemplo: "Menú"
        self.texto: str = texto
        # Función que ejecutará el botón.
        self.onclick = onclick
        
        self.padding_imagen: int = 14
        self.tamanio_letra: int = 24
        self.tamanio_imagen: int = 40
        self.tamanio_container_izq = (68, 68)
        self.tamanio_container_der = (182, 68)
        
        self.icono = ft.Image(
            src=self.ruta_imagen,
            height=self.tamanio_imagen, width=self.tamanio_imagen,
            fit=ft.ImageFit.CONTAIN
        )
        self.container_icono = ft.Container(
            content=self.icono,
            width=self.tamanio_container_izq[0],
            height=self.tamanio_container_izq[1],
            alignment=ft.alignment.center,
        )
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
            width=self.tamanio_container_der[0],
            height=self.tamanio_container_der[1],
        )
        
        self.boton = ft.Container(
            content=ft.Row([self.container_icono, self.container_texto]),
            alignment=ft.alignment.top_left,
            bgcolor=COLOR.ROJO,
            ink=True,
            on_click=self.onclick,
            width=(self.tamanio_container_izq[0] + self.tamanio_container_der[0]),
        )
    
    def dibujar(self) -> ft.Container:
        return self.boton


class UI_Menu:
    """
    Panel (de navegación?) izquierdo o menú, con todos los botones necesarios
    para la creación de archivos.
    """

    def archivo_nuevo(self, e):
        nuevo_archivo(self.page, self.file_picker)
    
    def archivo_abrir(self, e):
        abrir_archivo(self.page, self.file_picker)
    
    def archivo_guardar(self, e):
        guardar_archivo(self.page, self.file_picker)
        
    def archivo_importar(self, e):
        importar_archivo(self.page, self.file_picker)
    
    def archivo_exportar(self, e):
        exportar_archivo(self.page, self.file_picker)
    
    def __init__(self, universidad: Universidad, page: ft.Page):
        self.page = page
        self.universidad = universidad
        
        # Para manejar ventanas de archivos.
        self.file_picker = ft.FilePicker()
        self.page.overlay.append(self.file_picker)
        
        self.icono_UNRN = UI_UNRN("logo_UNRN_Andina.png")
        self.boton_menu = UI_MenuBoton("iconos/menu.png", "Menú", None)
        self.boton_nuevo = UI_MenuBoton("iconos/nuevo.png", "Nuevo", self.archivo_nuevo)
        self.boton_abrir = UI_MenuBoton("iconos/abrir.png", "Abrir", self.archivo_abrir)
        self.boton_guardar = UI_MenuBoton("iconos/guardar.png", "Guardar", self.archivo_guardar)
        self.boton_importar = UI_MenuBoton("iconos/importar.png", "Importar", self.archivo_importar)
        self.boton_exportar = UI_MenuBoton("iconos/exportar.png", "Exportar", self.archivo_exportar)
        
        self.subcolumna = ft.Column(
            controls=[
                self.boton_menu.dibujar(),
                self.boton_nuevo.dibujar(),
                self.boton_abrir.dibujar(),
                self.boton_guardar.dibujar(),
                self.boton_importar.dibujar(),
                self.boton_exportar.dibujar()
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS,
            tight=True
        )
        
        self.columna = ft.Column(
            controls=[
                self.icono_UNRN.dibujar(),
                self.subcolumna
            ],
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
            width=250,
            tight=False,
            expand=True
        )
        
        self.container = ft.Container(
            content=self.columna,
            padding=0,
            bgcolor=COLOR.ROJO,
            alignment=ft.alignment.top_left,
            expand=False
        )
    
    def dibujar(self) -> ft.Container:
        return self.container

