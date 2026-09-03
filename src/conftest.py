"""Configuración de pruebas.

Al vivir en `src/`, hace que pytest añada `src/` a `sys.path`, de modo que los
tests puedan importar `main` y `data.mock_data` igual que la app en ejecución.
Además restaura la lista de anuncios en memoria antes de cada prueba.
"""

import copy

import pytest

import data.mock_data as mock_data

_ANUNCIOS_INICIALES = copy.deepcopy(mock_data.anuncios)


@pytest.fixture(autouse=True)
def _reset_anuncios():
    mock_data.anuncios[:] = copy.deepcopy(_ANUNCIOS_INICIALES)
    yield
    mock_data.anuncios[:] = copy.deepcopy(_ANUNCIOS_INICIALES)
