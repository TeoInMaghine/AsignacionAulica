'''
Configuraciones comunes a todos los tests unitarios.
'''
import pytest

def pytest_configure(config):
    # Registrar un marker para reconocer stress tests
    config.addinivalue_line("markers", "stress_test: indica que es un stress test, solo se ejecuta al usar el argumento --stress-tests")

def pytest_addoption(parser):
    # Añadir opción de línea de comandos personalizada a pytest
    parser.addoption("--stress-tests", action="store_true",
                     default=False, help="Incluir stress tests en la ejecución")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    # Saltear stress tests, excepto si se usa la opción --stress-test
    mark = item.get_closest_marker(name="stress_test")
    if mark and not item.config.getoption("--stress-tests"):
        item.add_marker(pytest.mark.skip(reason="Estas pruebas toman mucho tiempo en ejecutar. Ejecutar con --stress-tests si quiere incluirlas."), append=False)

