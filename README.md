# Asignación Áulica

Este es el software de asignación áulica desarrollado como proyecto de la
materia "Ingeniería de Software".

# Ambiente de Desarrollo

Para desarrollar y probar este software es conveniente usar un ambiente virtual
de python.

**Prerequisitos:** Tener instalado Python version 3.11 o superior, y pip.

**Cómo usar el ambiente virtual:**

1. Crear el ambiente con `python -m venv venv`.
2. Activar el ambiente con
   
   ```
   source venv/bin/activate # En linux
   .\venv\Scripts\activate  # En Windows
   ```

3. Instalar las dependencias del proyecto con `pip install --editable .[test]`

   Nota: la opción `[test]` instala los paquetes necesarios para ejecutar las
   pruebas unitarias. Se puede omitir si no vas a ejecutar las pruebas
   unitarias.

4. Ejecutar el programa con `flet run`.

   Nota: No ejecutar los archivos `.py` directamente, porque flet agrega
   variables de entorno y otras magias que, si no se tienen en cuenta, pueden
   causar problemas del tipo "en mi conpu aparecen los íconos pero  en las otras
   compus no".
