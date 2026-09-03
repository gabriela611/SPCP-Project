"""Configuración de pruebas.

Al vivir en `srcprueba/`, hace que pytest añada esa carpeta a `sys.path`, de modo
que los tests importen `main` y `data.mock_data` igual que la app en ejecución.
Además vacía las sesiones en memoria antes de cada prueba.
"""

import pytest

import data.mock_data as mock_data


@pytest.fixture(autouse=True)
def _reset_sesiones():
    mock_data.sesiones.clear()
    yield
    mock_data.sesiones.clear()
