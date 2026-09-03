"""Reglas de negocio del Módulo de Publicación de Anuncios.

Un anuncio SOLO es visible para:
  * su autor,
  * los usuarios con rol Administrador,
  * los usuarios cuyo rol está entre los destinatarios del anuncio, o
  * los usuarios inscritos en alguno de los cursos destinatarios del anuncio.
"""

from datetime import date

from fastapi import HTTPException

from data.mock_data import anuncios, cursos, roles, usuarios

ROL_ADMIN = "Administrador"
ROL_DOCENTE = "Docente"
ROLES_QUE_PUBLICAN = {ROL_ADMIN, ROL_DOCENTE}


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _usuario(usuario_id):
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
    if usuario is None:
        raise HTTPException(status_code=401, detail="usuario_id no válido")
    return usuario


def _nombre_rol(rol_id):
    rol = next((r for r in roles if r["id"] == rol_id), None)
    return rol["nombre"] if rol else ""


def _existe_rol(rol_id):
    return any(r["id"] == rol_id for r in roles)


def _existe_curso(curso_id):
    return any(c["id"] == curso_id for c in cursos)


# --------------------------------------------------------------------------- #
# Visibilidad                                                                 #
# --------------------------------------------------------------------------- #
def puede_ver(usuario, anuncio):
    if anuncio["autor_id"] == usuario["id"]:
        return True
    if _nombre_rol(usuario["rol_id"]) == ROL_ADMIN:
        return True
    if usuario["rol_id"] in anuncio["roles_destino_ids"]:
        return True
    if set(usuario["cursos_ids"]) & set(anuncio["cursos_destino_ids"]):
        return True
    return False


def listar_anuncios_visibles(usuario_id, tipo=None):
    usuario = _usuario(usuario_id)
    visibles = [a for a in anuncios if puede_ver(usuario, a)]
    if tipo:
        visibles = [a for a in visibles if a["tipo"] == tipo]
    return sorted(visibles, key=lambda a: (a["fecha_publicacion"], a["id"]), reverse=True)


def obtener_anuncio_visible(usuario_id, anuncio_id):
    usuario = _usuario(usuario_id)
    anuncio = next((a for a in anuncios if a["id"] == anuncio_id), None)
    if anuncio is None or not puede_ver(usuario, anuncio):
        raise HTTPException(status_code=404, detail="Anuncio no encontrado")
    return anuncio


# --------------------------------------------------------------------------- #
# Creación                                                                    #
# --------------------------------------------------------------------------- #
def crear_anuncio(usuario_id, datos):
    autor = _usuario(usuario_id)
    rol_autor = _nombre_rol(autor["rol_id"])
    if rol_autor not in ROLES_QUE_PUBLICAN:
        raise HTTPException(
            status_code=403,
            detail="Solo un Administrador o Docente puede crear anuncios",
        )

    roles_destino = sorted(set(datos.get("roles_destino_ids") or []))
    cursos_destino = sorted(set(datos.get("cursos_destino_ids") or []))

    if not roles_destino and not cursos_destino:
        raise HTTPException(
            status_code=400,
            detail="El anuncio debe tener al menos un rol o curso destinatario",
        )

    for rol_id in roles_destino:
        if not _existe_rol(rol_id):
            raise HTTPException(
                status_code=400, detail=f"Rol destinatario inexistente: {rol_id}"
            )
    for curso_id in cursos_destino:
        if not _existe_curso(curso_id):
            raise HTTPException(
                status_code=400, detail=f"Curso destinatario inexistente: {curso_id}"
            )

    if rol_autor == ROL_DOCENTE:
        if roles_destino:
            raise HTTPException(
                status_code=403,
                detail="Un Docente solo puede dirigir anuncios a sus cursos, no a roles",
            )
        ajenos = [c for c in cursos_destino if c not in autor["cursos_ids"]]
        if ajenos:
            raise HTTPException(
                status_code=403,
                detail=f"El Docente no dicta el/los curso(s): {ajenos}",
            )

    nuevo = {
        "id": max((a["id"] for a in anuncios), default=0) + 1,
        "titulo": datos["titulo"],
        "descripcion": datos["descripcion"],
        "tipo": datos.get("tipo") or "anuncio",
        "fecha_publicacion": date.today().isoformat(),
        "fecha_evento": datos.get("fecha_evento"),
        "hora_evento": datos.get("hora_evento"),
        "lugar": datos.get("lugar"),
        "autor_id": autor["id"],
        "roles_destino_ids": roles_destino,
        "cursos_destino_ids": cursos_destino,
    }
    anuncios.append(nuevo)
    return nuevo
