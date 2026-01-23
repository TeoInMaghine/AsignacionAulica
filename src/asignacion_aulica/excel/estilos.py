from openpyxl.styles import NamedStyle, PatternFill, Border, Side, Alignment, Font
from openpyxl.utils.units import points_to_pixels
from openpyxl.drawing.image import Image
from copy import copy

from asignacion_aulica import assets

logo_path = assets.get_path('logo_unrn_excel.png')

rojo_unrn = 'EB1C38'
fill_rojo_unrn = PatternFill(patternType='solid', fgColor=rojo_unrn)

font_default = Font(name = 'arial', size = 12)

font_bold = copy(font_default)
font_bold.bold = True

font_encabezado = copy(font_bold)
font_encabezado.size = 18
font_encabezado.color = 'FFFFFF'

centrado = Alignment(horizontal='center', vertical='center', wrap_text=True)
a_la_derecha = Alignment(horizontal = 'right', vertical='center')
a_la_izquierda = Alignment(horizontal = 'left', vertical='center')

borde_negro = Side(border_style='thin', color='000000')
borde_negro_grueso = Side(border_style='medium', color='000000')
borde_blanco = Side(border_style='thin', color='FFFFFF')
todos_los_bordes_negros = Border(top=borde_negro, bottom=borde_negro, left=borde_negro, right=borde_negro)

estilo_header = NamedStyle(name='header', font=font_bold, border=todos_los_bordes_negros, alignment=centrado)
estilo_tabla = NamedStyle(name='tabla', font=font_default, alignment=centrado)
estilo_horarios = NamedStyle(name='horarios', font=font_default, alignment=centrado, number_format='HH:MM')

def get_logo(height_points: float) -> Image:
    imagen = Image(logo_path)
    scale_ratio = points_to_pixels(height_points) / imagen.height
    imagen.height *= scale_ratio
    imagen.width *= scale_ratio

    return imagen
