"""Pruebas del Módulo de Publicación de Anuncios.

Datos sembrados (src/data/mock_data.py):
    Cursos:  1 = Quinto A,  2 = Sexto B
    1 admin@bfa.edu  Administrador
    2 diego@bfa.edu  Docente  -> Quinto A
    3 elena@bfa.edu  Docente  -> Sexto B
    4 pedro@bfa.edu  Padre    -> Quinto A
    5 paula@bfa.edu  Padre    -> Sexto B
    6 pablo@bfa.edu  Padre    -> Quinto A + Sexto B
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

ADMIN, DIEGO, ELENA, PEDRO, PAULA, PABLO = 1, 2, 3, 4, 5, 6
QUINTO_A, SEXTO_B = 1, 2
ROL_PADRE = 3


def _crear(usuario_id, **campos):
    cuerpo = {"titulo": "Aviso de prueba", "descripcion": "Contenido del aviso"}
    cuerpo.update(campos)
    return client.post("/anuncios", params={"usuario_id": usuario_id}, json=cuerpo)


def _titulos(usuario_id, **params):
    params["usuario_id"] = usuario_id
    return {a["titulo"] for a in client.get("/anuncios", params=params).json()}


# --------------------------------------------------------------------------- #
# Creación                                                                    #
# --------------------------------------------------------------------------- #
def test_docente_crea_anuncio_para_su_curso():
    r = _crear(DIEGO, cursos_destino_ids=[QUINTO_A])
    assert r.status_code == 201, r.text
    cuerpo = r.json()
    assert cuerpo["cursos_destino_ids"] == [QUINTO_A]
    assert cuerpo["autor_id"] == DIEGO
    assert cuerpo["tipo"] == "anuncio"


def test_padre_no_puede_crear():
    assert _crear(PEDRO, cursos_destino_ids=[QUINTO_A]).status_code == 403


def test_anuncio_sin_destinatarios_se_rechaza():
    assert _crear(ADMIN).status_code == 400


def test_docente_no_puede_dirigir_a_curso_ajeno():
    assert _crear(DIEGO, cursos_destino_ids=[SEXTO_B]).status_code == 403


def test_docente_no_puede_segmentar_por_rol():
    r = _crear(DIEGO, cursos_destino_ids=[QUINTO_A], roles_destino_ids=[ROL_PADRE])
    assert r.status_code == 403


def test_curso_inexistente_se_rechaza():
    assert _crear(ADMIN, cursos_destino_ids=[999]).status_code == 400


def test_entrada_invalida_devuelve_422():
    r = _crear(ADMIN, titulo="ab", cursos_destino_ids=[QUINTO_A])  # título muy corto
    assert r.status_code == 422
    assert "detail" in r.json()


# --------------------------------------------------------------------------- #
# Visibilidad                                                                 #
# --------------------------------------------------------------------------- #
def test_anuncio_de_curso_solo_lo_ven_los_de_ese_curso():
    _crear(DIEGO, titulo="Reunión Quinto A", cursos_destino_ids=[QUINTO_A])
    assert "Reunión Quinto A" in _titulos(PEDRO)       # Quinto A
    assert "Reunión Quinto A" not in _titulos(PAULA)   # solo Sexto B
    assert "Reunión Quinto A" in _titulos(PABLO)       # inscrito en ambos


def test_docente_no_ve_anuncio_de_otro_curso():
    _crear(DIEGO, titulo="Circular Quinto", cursos_destino_ids=[QUINTO_A])
    assert "Circular Quinto" not in _titulos(ELENA)


def test_anuncio_por_rol_llega_a_todos_los_padres():
    _crear(ADMIN, titulo="Comunicado institucional", roles_destino_ids=[ROL_PADRE])
    for uid in (PEDRO, PAULA, PABLO):
        assert "Comunicado institucional" in _titulos(uid)
    assert "Comunicado institucional" not in _titulos(ELENA)  # docente no destinatario


def test_admin_ve_todos_los_anuncios():
    _crear(DIEGO, titulo="Aviso Quinto A", cursos_destino_ids=[QUINTO_A])
    _crear(ELENA, titulo="Aviso Sexto B", cursos_destino_ids=[SEXTO_B])
    assert {"Aviso Quinto A", "Aviso Sexto B"} <= _titulos(ADMIN)


def test_get_por_id_de_anuncio_no_visible_devuelve_404():
    anuncio_id = _crear(DIEGO, cursos_destino_ids=[QUINTO_A]).json()["id"]
    assert client.get(f"/anuncios/{anuncio_id}",
                      params={"usuario_id": PAULA}).status_code == 404


def test_get_por_id_visible_para_destinatario():
    anuncio_id = _crear(DIEGO, cursos_destino_ids=[QUINTO_A]).json()["id"]
    r = client.get(f"/anuncios/{anuncio_id}", params={"usuario_id": PEDRO})
    assert r.status_code == 200
    assert r.json()["id"] == anuncio_id


def test_filtro_por_tipo():
    _crear(ADMIN, titulo="Es un anuncio", roles_destino_ids=[2])
    _crear(ADMIN, titulo="Es un evento", tipo="evento", roles_destino_ids=[2])
    titulos = _titulos(DIEGO, tipo="evento")
    assert "Es un evento" in titulos
    assert "Es un anuncio" not in titulos
