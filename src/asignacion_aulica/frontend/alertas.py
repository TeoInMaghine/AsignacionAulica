# -*- coding: utf-8 -*-
"""
Elementos de Alerta para el usuario (Interfaz de Usuario).

@author: Cristian
"""

import flet as ft

from .datos import limpiar_espacios_texto


class VentanaAlerta():
    """
    Ventana de Alerta al Usuario, con mensaje y 1 botón para cerrar.
    """
    def __init__(
            self,
            page: ft.Page,
            mensaje_de_alerta: str
            ):
        """
        Al instanciarla abre automáticamente una ventana de alerta con un
        mensaje para el usuario. Posee un título con el contenido "Atención" y
        en el cuerpo de la ventana se encuentra el mensaje al usuario. Tiene un
        (1) botón para cerrarla.

        Parameters
        ----------
        page : ft.Page
            Page de la app para poder abrir la ventana de alerta.
        mensaje_de_alerta : str
            Mensaje a alertar al usuario. Por ejemplo: "Error con tipo de dato..."

        Returns
        -------
        None.

        """
        # Limpia el texto de espacios innecesarios.
        mensaje: str = limpiar_espacios_texto(mensaje_de_alerta)
        
        # Crea la ventana de alerta al usuario con el mensaje brindado.
        self.alerta = ft.AlertDialog(
            modal=True,
            title=ft.Text("Atención"),
            content=ft.Text(mensaje, selectable=True),
            actions=[
                ft.TextButton(
                    text="Aceptar",
                    on_click=lambda e: page.close(self.alerta)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print(f"Alertado al usuario: {mensaje}"),
        )
        
        # Abre la alerta. (se cierra clickeando el botón del mensaje).
        page.open(self.alerta)
        
class VentanaConfirmacion():
    """
    Ventana de Alerta al Usuario, con mensaje y 2 botón para confirmar o
    abortar acción.
    """
    def __init__(
            self,
            page: ft.Page,
            mensaje_advertencia: str,
            funcion
            ):
        """
        Al instanciarla abre automáticamente una ventana de alerta con un
        mensaje para el usuario. Posee un título con el contenido "Atención" y
        en el cuerpo de la ventana se encuentra el mensaje al usuario. Tiene
        dos (2) botones ("Sí" y "No") para confirmar o abortar la acción a
        realizar.

        Parameters
        ----------
        page : ft.Page
            Page de la app para poder abrir la ventana de alerta.
        mensaje : str
            Mensaje a alertar al usuario. Por ejemplo: "¿Estas seguro de que quieres..."
        funcion : function
            Referencia a la función a ejecutar al confirmar la acción.

        Returns
        -------
        None.

        """
        def confirmacion(alerta):
            funcion()
            page.close(alerta)
        
        # Limpia el texto de espacios innecesarios.
        mensaje: str = limpiar_espacios_texto(mensaje_advertencia)
        
        # Crea la ventana de alerta al usuario con el mensaje brindado.
        self.alerta = ft.AlertDialog(
            modal=True,
            title=ft.Text("Atención"),
            content=ft.Text(mensaje, size=16, selectable=True),
            actions=[
                ft.Button(
                    text="Sí",
                    on_click=lambda e: confirmacion(self.alerta)
                ),
                ft.Button(
                    text="No",
                    on_click=lambda e: page.close(self.alerta)
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print(f"Alertado al usuario: {mensaje}"),
        )
        
        # Abre la alerta. (se cierra clickeando el botón del mensaje).
        page.open(self.alerta)
