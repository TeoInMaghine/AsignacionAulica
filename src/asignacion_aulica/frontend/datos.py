# -*- coding: utf-8 -*-
import flet as ft
from pandas import DataFrame
import re


def crear_tabla(df: DataFrame) -> ft.DataTable:
    """
    Crea una ft.DataTable (UI, Flet) a partir de una DataFrame.

    Parameters
    ----------
    df : DataFrame
        DataFrame (tabla) con todos los datos de la tabla.

    Returns
    -------
    ft.DataTable
        Tabla con todos los datos de la DataFrame, para mostrar en la UI.

    """
    
    columnas = []
    filas = []
    
    # Se obtienen los nombres de las columnas.
    for col_name in df:
        columnas.append(ft.DataColumn(ft.Text(col_name)))
    
    # Se obtienen número de filas de la tabla.
    num_rows = df.shape[0]
    
    # Para cada fila se cargan los datos de todas las celdas, de sus
    # respectivas columnas.
    for row in range(num_rows):
        celdas = []
        for col in df:
            celdas.append(ft.DataCell(ft.Text(df[col].iloc[row])))
        filas.append(ft.DataRow(cells=celdas))
    
    return ft.DataTable(columns=columnas, rows=filas)

def limpiar_texto(texto: str) -> str:
    """
    Limpia un texto o string de símbolos o espacios conflictivos que pudieran
    llegar a dar problema en el procesamiento de los datos.
    
    Quita los espacios antes y después del texto. Suprime los múltiples
    espacios a uno solo. Quita los símbolos problemáticos, a excepción del
    guión (-) y guión bajo (_).

    Parameters
    ----------
    texto : str
        Texto/string a limpiar. Por ejemplo: " h$o@la   soy   yo ".

    Returns
    -------
    str
        Texto/string limpio. Por ejemplo (usando el ejemplo del input): "hola soy yo".

    """
    # Se eliminan los caracteres que no sean letras, números, espacio, guión o
    # guión bajo.
    texto = re.sub(r"[^\w\s\-_]", "", texto)
    
    # Se eliminan los espacios al principio y al final.
    texto = texto.strip()

    # Se reemplazan los múltiples espacios por uno solo.
    texto = re.sub(r"\s+", " ", texto)

    return texto
