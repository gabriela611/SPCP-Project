"""Pruebas de Autenticación y gestión de roles (issue #4).

Usuarios sembrados (srcprueba/data/mock_data.py):
    1 admin@bfa.edu / admin123  Administrador
    2 diego@bfa.edu / diego123  Docente
    3 elena@bfa.edu / elena123  Docente
    4 pedro@bfa.edu / pedro123  Padre de familia
    5 paula@bfa.edu / paula123  Padre de familia
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

ADMIN, DIEGO, PEDRO = 1, 2, 4


def _login(correo, contrasena):
    return client.post("/sesiones", json={"correo": correo, "contrasena": contrasena})


# --------------------------------------------------------------------------- #
# Login                                                                       #
# --------------------------------------------------------------------------- #
def test_root_ok():
    assert client.get("/").json()["estado"] == "ok"


def test_login_valido_devuelve_rol_y_permisos():
    r = _login("diego@bfa.edu", "diego123")
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert cuerpo["usuario_id"] == DIEGO
    assert cuerpo["rol"] == "Docente"
    assert "anuncios.crear" in cuerpo["permisos"]
    assert len(cuerpo["token"]) == 32


def test_login_credenciales_invalidas_devuelve_401():
    assert _login("diego@bfa.edu", "incorrecta").status_code == 401
    assert _login("noexiste@bfa.edu", "x").status_code == 401


def test_login_falta_campo_devuelve_422():
    r = client.post("/sesiones", json={"correo": "diego@bfa.edu"})
    assert r.status_code == 422
    assert "detail" in r.json()


# --------------------------------------------------------------------------- #
# Ajuste de funcionalidad según rol                                           #
# --------------------------------------------------------------------------- #
def test_permisos_de_administrador():
    permisos = client.get("/permisos", params={"usuario_id": ADMIN}).json()
    assert "roles.gestionar" in permisos
    assert "portal.supervisar" in permisos


def test_permisos_de_padre_no_incluyen_crear_anuncios():
    permisos = client.get("/permisos", params={"usuario_id": PEDRO}).json()
    assert "anuncios.ver" in permisos
    assert "anuncios.crear" not in permisos


def test_permisos_usuario_inexistente_devuelve_401():
    assert client.get("/permisos", params={"usuario_id": 999}).status_code == 401


# --------------------------------------------------------------------------- #
# Bloqueo de acceso no autorizado                                             #
# --------------------------------------------------------------------------- #
def test_acceso_permitido_para_rol_con_permiso():
    r = client.get(
        "/permisos", params={"usuario_id": DIEGO, "funcionalidad": "anuncios.crear"}
    )
    assert r.status_code == 200
    assert r.json()["permitido"] is True


def test_acceso_bloqueado_para_rol_sin_permiso():
    r = client.get(
        "/permisos", params={"usuario_id": PEDRO, "funcionalidad": "anuncios.crear"}
    )
    assert r.status_code == 403
    assert "detail" in r.json()


# --------------------------------------------------------------------------- #
# Consulta de sesión                                                          #
# --------------------------------------------------------------------------- #
def test_consultar_sesion_por_token():
    token = _login("admin@bfa.edu", "admin123").json()["token"]
    r = client.get(f"/sesiones/{token}")
    assert r.status_code == 200
    assert r.json()["rol"] == "Administrador"


def test_consultar_sesion_token_invalido_devuelve_404():
    assert client.get("/sesiones/tokenfalso").status_code == 404
