# Asignación Áulica

Este es el software de asignación áulica desarrollado como proyecto de la
materia "Ingeniería de Software".

## Créditos

Algunos [íconos](/assets/iconos/) fueron creados a partir del [Simple Design System](https://www.figma.com/community/file/1380235722331273046) de [Figma](https://www.figma.com/), licenciado bajo [CC BY 4.0](http://creativecommons.org/licenses/by/4.0/).

El ícono de ordenar es [Sort az icons created by Prosymbols Premium - Flaticon](https://www.flaticon.com/free-icons/sort-az).

El ícono de editar es [Write icons created by Arkinasi - Flaticon](https://www.flaticon.com/free-icons/write).

El ícono de guardar está basado en [Save Item 1411 by bypeople - svgrepo](https://www.svgrepo.com/svg/512798/save-item-1411).

La animación que se muestra durante la asignación es [cat Mark loading by Miroslav - LottieFiles](https://lottiefiles.com/free-animation/cat-mark-loading-VlrnxEpvgu).

# Ambiente de Desarrollo

Para desarrollar y probar este software es conveniente usar un ambiente virtual
de python.

**Prerequisitos:** Tener instalado Python version 3.11 o superior, y pip.

**Cómo usar el ambiente virtual:**

1. Crear el ambiente ejecutando en la raíz de este repositorio `python -m venv venv`.
2. Activar el ambiente con

    ```
    source venv/bin/activate # En linux
    .\venv\Scripts\activate  # En Windows
    ```

3. Instalar las dependencias del proyecto con `pip install --editable .[test,build]`

    Nota: la opción `[test,build,excel]` instala los paquetes extra necesarios
    para ejecutar las pruebas unitarias, para empaquetar el programa, y para
    generar las plantillas excel. Se puede omitir cualquiera de los tres extras
    si no se va a usar.

4. El programa (sin empaquetar) se puede ejecutar con el comando `asignacion-aulica`.

   Alternativamente, se puede ejecutar el archivo `src/asignacion_aulica/main.py`.

**Tests unitarios:**

Hay pruebas unitarias que usan la librería `pytest`. Están en el directorio
`tests/pytest`.

Hay algunas pruebas llamadas *stress tests* que pueden tardar en ejecutarse, así
que por defecto se saltean.

- Ejecutar todo excepto los *stress tests*:

    ```
    pytest
    ```

- Ejecutar y ver los logs:

    ```
    pytest --log-cli-level=INFO
    ```

- Ejecutar todo (incluyendo stress tests):

    ```
    pytest --stress-tests
    ```
## Empaquetado

El programa se empaqueta en dos pasos:

1. Se usa [cx_freeze](https://cx-freeze.readthedocs.io/en/stable/index.html)
   para generar una carpeta con un exe más el programa y todas sus dependencias.
2. Se usa [Inno Setup](https://jrsoftware.org/ishelp/index.php) para generar un
   instalador.

Hay una GitHub action que ejecuta los dos pasos. El paso 1 también se puede
ejecutar en el entorno virtual (ver comando en el archivo de la GitHub Action).

