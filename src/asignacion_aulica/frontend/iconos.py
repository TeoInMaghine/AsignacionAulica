# -*- coding: utf-8 -*-
"""
Created on Wed May 28 12:50:21 2025

@author: Cristian
"""

import flet as ft


class UI_Icono():
    def __init__(self):
        self.TAMAÑO: int = 40 # 40 px
        
        # Las rutas están escritas relativas al directorio src/assets/
        
        self.MENU = ft.Image(src="iconos/menu.png",
                             height=self.TAMAÑO,
                             width=self.TAMAÑO,
                             fit=ft.ImageFit.CONTAIN)
        self.NUEVO = ft.Image(src="iconos/nuevo.png",
                              height=self.TAMAÑO,
                              width=self.TAMAÑO,
                              fit=ft.ImageFit.CONTAIN)
        self.IMPORTAR = ft.Image(src="iconos/importar.png",
                                 height=self.TAMAÑO,
                                 width=self.TAMAÑO,
                                 fit=ft.ImageFit.CONTAIN)
        self.ABRIR = ft.Image(src="iconos/abrir.png",
                              height=self.TAMAÑO,
                              width=self.TAMAÑO,
                              fit=ft.ImageFit.CONTAIN)
        self.GUARDAR = ft.Image(src="iconos/guardar.png",
                                height=self.TAMAÑO,
                                width=self.TAMAÑO,
                                fit=ft.ImageFit.CONTAIN)
        self.EXPORTAR = ft.Image(src="iconos/exportar.png",
                                 height=self.TAMAÑO,
                                 width=self.TAMAÑO,
                                 fit=ft.ImageFit.CONTAIN)
        self.FLECHA_CLARA = ft.Image(src="iconos/flecha_clara.png",
                                     height=self.TAMAÑO,
                                     width=self.TAMAÑO,
                                     fit=ft.ImageFit.CONTAIN)
        self.FLECHA_OSCURA = ft.Image(src="iconos/flecha_oscura.png",
                                      height=self.TAMAÑO,
                                      width=self.TAMAÑO,
                                      fit=ft.ImageFit.CONTAIN)
