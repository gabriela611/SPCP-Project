"""Pruebas del Módulo de Publicación de Anuncios.

Datos sembrados (`src/seed.py`):
    Cursos:   1 = Quinto A, 2 = Sexto B
    admin@bfa.edu   Administrador
    diego@bfa.edu   Docente  -> Quinto A
    elena@bfa.edu   Docente  -> Sexto B
    pedro@bfa.edu   Padre    -> Quinto A
    paula@bfa.edu   Padre    -> Sexto B
    pablo@bfa.edu   Padre    -> Quinto A + Sexto B
"""

from __future__ import annotations

QUINTO_A = 1
SEXTO_B = 2


def _crear(client, headers, **campos):
    cuerpo = {"titulo": "Aviso importante", "descripcion": "Contenido del aviso"}
    cuerpo.update(campos)
    return client.post("/anuncios", json=cuerpo, headers=headers)


# --------------------------------------------------------------------------- #
# Autenticación                                                               #
# --------------------------------------------------------------------------- #
def test_sin_token_devuelve_401(client):
    assert client.get("/anuncios").status_code == 401


def test_login_devuelve_rol(client):
    r = client.post("/auth/login", json={"correo": "diego@bfa.edu"})
    assert r.status_code == 200
    assert r.json()["usuario"]["rol"] == "Docente"


# --------------------------------------------------------------------------- #
# Creación                                                                    #
# --------------------------------------------------------------------------- #
def test_docente_crea_anuncio_para_su_curso(client, login):
    r = _crear(client, login("diego@bfa.edu"), cursos_destino=[QUINTO_A])
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert [c["id"] for c in cuerpo["cursos_destino"]] == [QUINTO_A]
    assert cuerpo["autor"]["correo"] == "diego@bfa.edu"


def test_padre_no_puede_crear(client, login):
    r = _crear(client, login("pedro@bfa.edu"), cursos_destino=[QUINTO_A])
    assert r.status_code == 403


def test_anuncio_sin_destinatarios_se_rechaza(client, login):
    r = _crear(client, login("admin@bfa.edu"))
    assert r.status_code == 400


def test_docente_no_puede_dirigir_a_curso_ajeno(client, login):
    r = _crear(client, login("diego@bfa.edu"), cursos_destino=[SEXTO_B])
    assert r.status_code == 403


def test_docente_no_puede_segmentar_por_rol(client, login):
    r = _crear(
        client,
        login("diego@bfa.edu"),
        cursos_destino=[QUINTO_A],
        roles_destino=["Padre de familia"],
    )
    assert r.status_code == 403


def test_curso_inexistente_se_rechaza(client, login):
    r = _crear(client, login("admin@bfa.edu"), cursos_destino=[999])
    assert r.status_code == 400


# --------------------------------------------------------------------------- #
# Visibilidad                                                                 #
# --------------------------------------------------------------------------- #
def test_anuncio_de_curso_solo_lo_ven_los_de_ese_curso(client, login):
    _crear(client, login("diego@bfa.edu"), titulo="Salida pedagógica Quinto",
           cursos_destino=[QUINTO_A])

    titulos_pedro = {a["titulo"] for a in client.get(
        "/anuncios", headers=login("pedro@bfa.edu")).json()}
    titulos_paula = {a["titulo"] for a in client.get(
        "/anuncios", headers=login("paula@bfa.edu")).json()}
    titulos_pablo = {a["titulo"] for a in client.get(
        "/anuncios", headers=login("pablo@bfa.edu")).json()}

    assert "Salida pedagógica Quinto" in titulos_pedro   # Quinto A
    assert "Salida pedagógica Quinto" not in titulos_paula  # solo Sexto B
    assert "Salida pedagógica Quinto" in titulos_pablo   # inscrito en ambos


def test_docente_no_ve_anuncio_de_otro_curso(client, login):
    _crear(client, login("diego@bfa.edu"), titulo="Reunión Quinto",
           cursos_destino=[QUINTO_A])
    titulos_elena = {a["titulo"] for a in client.get(
        "/anuncios", headers=login("elena@bfa.edu")).json()}
    assert "Reunión Quinto" not in titulos_elena


def test_admin_ve_todos_los_anuncios(client, login):
    _crear(client, login("diego@bfa.edu"), titulo="Aviso Quinto A", cursos_destino=[QUINTO_A])
    _crear(client, login("elena@bfa.edu"), titulo="Aviso Sexto B", cursos_destino=[SEXTO_B])
    titulos_admin = {a["titulo"] for a in client.get(
        "/anuncios", headers=login("admin@bfa.edu")).json()}
    assert {"Aviso Quinto A", "Aviso Sexto B"} <= titulos_admin


def test_anuncio_por_rol_llega_a_todos_los_padres(client, login):
    _crear(client, login("admin@bfa.edu"), titulo="Circular institucional",
           roles_destino=["Padre de familia"])

    for correo in ("pedro@bfa.edu", "paula@bfa.edu", "pablo@bfa.edu"):
        titulos = {a["titulo"] for a in client.get(
            "/anuncios", headers=login(correo)).json()}
        assert "Circular institucional" in titulos

    # Un docente que no es destinatario por rol ni por curso no lo ve.
    titulos_elena = {a["titulo"] for a in client.get(
        "/anuncios", headers=login("elena@bfa.edu")).json()}
    assert "Circular institucional" not in titulos_elena


def test_get_por_id_de_anuncio_no_visible_devuelve_404(client, login):
    anuncio_id = _crear(client, login("diego@bfa.edu"),
                        cursos_destino=[QUINTO_A]).json()["id"]
    r = client.get(f"/anuncios/{anuncio_id}", headers=login("paula@bfa.edu"))
    assert r.status_code == 404


def test_get_por_id_visible_para_destinatario(client, login):
    anuncio_id = _crear(client, login("diego@bfa.edu"),
                        cursos_destino=[QUINTO_A]).json()["id"]
    r = client.get(f"/anuncios/{anuncio_id}", headers=login("pedro@bfa.edu"))
    assert r.status_code == 200
    assert r.json()["id"] == anuncio_id


def test_filtro_por_tipo(client, login):
    _crear(client, login("admin@bfa.edu"), titulo="Solo anuncio",
           roles_destino=["Docente"])
    _crear(client, login("admin@bfa.edu"), titulo="Es evento", tipo="evento",
           roles_destino=["Docente"])
    r = client.get("/anuncios", params={"tipo": "evento"},
                   headers=login("diego@bfa.edu"))
    titulos = {a["titulo"] for a in r.json()}
    assert titulos == {"Es evento"}
