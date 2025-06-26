# -*- coding: utf-8 -*-
"""
Funciones para la creación, apertura y guardado de archivos.
También importación y exportación.

@author: Cristian
"""

import flet as ft

from .alertas import VentanaAlerta
from asignacion_aulica.frontend.universidad import Universidad 


# Función que se llama cuando se selecciona una ruta.
def resultado_nuevo(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    if file_picker.result != None and file_picker.result.path != None:
        ruta = file_picker.result.path
        
        # TODO
        # IMPLEMENTAR CREACION DE ARCHIVO NUEVO
        # universidad.tu_funcion()...
        
        # Se crea un archivo vacío.
        with open(ruta, "w") as f:
            f.write("")
    
def nuevo_archivo(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    """
    Funcion ejecutada al hacer click en el botón de Nuevo.
    Abre una ventana del sistema operativo para elegir la ruta y nombre de
    archivo para crear un nuevo proyecto.
    Exporta en: .unrn # TODO

    Parameters
    ----------
    page : ft.Page
        Página principal de flet.
    file_picker : ft.FilePicker
        Objeto de flet que se encarga de abrir la ventana y obtener la ruta del
        archivo.

    Returns
    -------
    None.

    """
    # Función que se llama cuando se clickeó en el botón "Guardar".
    file_picker.on_result = lambda e: resultado_nuevo(page, file_picker, universidad)
    
    # Se ejecuta la función para abrir la ventana de archivo.
    file_picker.save_file(
        dialog_title="Nuevo archivo",
        file_name="Sin título.unrn",
        allowed_extensions=["unrn"],
    )

# Función que se llama cuando se selecciona una ruta.
def resultado_apertura(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    if (file_picker.result != None) and file_picker.result.files:
        ruta = file_picker.result.files[0].path
        
        print("Archivo seleccionado:", ruta)
        
        # TODO
        # Acá podés abrirlo, leerlo o procesarlo
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as exc:
            mensaje_de_alerta: str = "Error al abrir el archivo:\n"
            mensaje_de_alerta += str(exc)
            VentanaAlerta(page, mensaje_de_alerta)
            
        page.update()

def abrir_archivo(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    """
    Funcion ejecutada al hacer click en el botón de Abrir.
    Abre una ventana del sistema operativo para elegir la ruta y nombre de
    archivo para abrir un proyecto.
    Importa en: .unrn # TODO

    Parameters
    ----------
    page : ft.Page
        Página principal de flet.
    file_picker : ft.FilePicker
        Objeto de flet que se encarga de abrir la ventana y obtener la ruta del
        archivo.

    Returns
    -------
    None.

    """
    # Función que se llama cuando se clickeó en el botón "Guardar".
    file_picker.on_result = lambda e: resultado_apertura(page, file_picker, universidad)
    
    # Se ejecuta la función para abrir la ventana de archivo.
    file_picker.pick_files(
        dialog_title="Abrir archivo",
        allow_multiple=False,
        allowed_extensions=["unrn"],
    )

# Función que se llama cuando se selecciona una ruta.
def resultado_guardado(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    if file_picker.result != None and file_picker.result.path != None:
        ruta = file_picker.result.path
        
        # TODO
        # IMPLEMENTAR GUARDADO DE ARCHIVO
        # Se crea un archivo vacío.
        with open(ruta, "w") as f:
            f.write("")

def guardar_archivo(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    """
    Funcion ejecutada al hacer click en el botón de Guardar.
    Abre una ventana del sistema operativo para elegir la ruta y nombre de
    archivo para guardar el proyecto.
    Exporta en: .unrn # TODO

    Parameters
    ----------
    page : ft.Page
        Página principal de flet.
    file_picker : ft.FilePicker
        Objeto de flet que se encarga de abrir la ventana y obtener la ruta del
        archivo.

    Returns
    -------
    None.

    """
    # Función que se llama cuando se clickeó en el botón "Guardar".
    file_picker.on_result = lambda e: resultado_guardado(page, file_picker, universidad)
    
    # Se ejecuta la función para abrir la ventana de archivo.
    file_picker.save_file(
        dialog_title="Guardar como...",
        file_name="Sin título.unrn",
        allowed_extensions=["unrn"],
    )

# Función que se llama cuando se selecciona una ruta.
def resultado_importacion(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    if (file_picker.result != None) and file_picker.result.files:
        ruta = file_picker.result.files[0].path
        
        print("Archivo seleccionado:", ruta)
        
        # TODO
        # Acá podés abrirlo, leerlo o procesarlo
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as exc:
            mensaje_de_alerta: str = "Error al abrir el archivo:\n"
            mensaje_de_alerta += str(exc)
            VentanaAlerta(page, mensaje_de_alerta)
            
        page.update()

def importar_archivo(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    """
    Funcion ejecutada al hacer click en el botón de Importar.
    Abre una ventana del sistema operativo para elegir la ruta y nombre de
    archivo para exportar el proyecto.
    Importa en: TODO

    Parameters
    ----------
    page : ft.Page
        Página principal de flet.
    file_picker : ft.FilePicker
        Objeto de flet que se encarga de abrir la ventana y obtener la ruta del
        archivo.

    Returns
    -------
    None.

    """
    # Función que se llama cuando se clickeó en el botón "Guardar".
    file_picker.on_result = lambda e: resultado_importacion(page, file_picker, universidad)
    
    # Se ejecuta la función para abrir la ventana de archivo.
    file_picker.pick_files(
        dialog_title="Importar archivo",
        allow_multiple=False,
        allowed_extensions=["csv", "xlsx"],
    )


# Función que se llama cuando se selecciona una ruta.
def resultado_exportacion(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    if file_picker.result != None and file_picker.result.path != None:
        ruta = file_picker.result.path

        if not ruta.endswith(".xlsx"):
            ruta+=".xlsx"
        
        universidad.exportar_horarios(ruta)
    else:
        VentanaAlerta("La ruta de exportación es inválida.")

def exportar_archivo(page: ft.Page, file_picker: ft.FilePicker, universidad: Universidad):
    """
    Funcion ejecutada al hacer click en el botón de Exportar.
    Abre una ventana del sistema operativo para elegir la ruta y nombre de
    archivo para exportar el proyecto.
    Exporta en: .xlsx, .csv TODO

    Parameters
    ----------
    page : ft.Page
        Página principal de flet.
    file_picker : ft.FilePicker
        Objeto de flet que se encarga de abrir la ventana y obtener la ruta del
        archivo.

    Returns
    -------
    None.

    """
    # Función que se llama cuando se clickeó en el botón "Guardar".
    file_picker.on_result = lambda e: resultado_exportacion(page, file_picker, universidad)
    
    # Se ejecuta la función para abrir la ventana de archivo.
    file_picker.save_file(
        dialog_title="Exportar archivo como...",
        file_name="",
        allowed_extensions=["csv", "xlsx"],
    )
