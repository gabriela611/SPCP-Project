"""Reglas de negocio del Módulo de Publicación de Anuncios.

Regla central (SOW · "filtrado segmentado estrictamente según el rol"):
un anuncio SOLO es visible para:

  * su autor,
  * los usuarios con rol Administrador (supervisión del portal),
  * los usuarios cuyo rol está en los destinatarios del anuncio, o
  * los usuarios inscritos en alguno de los cursos destinatarios del anuncio.

Cualquier otro usuario recibe el anuncio como inexistente (404), sin filtrarse
en los listados.
"""

from __future__ import annotations

from fastapi import HTTPException, status
from sqlmodel import Session, col, or_, select

from ..models import (
    ROL_ADMIN,
    ROL_DOCENTE,
    Anuncio,
    AnuncioCurso,
    AnuncioRol,
    Curso,
    Rol,
    Usuario,
    UsuarioXCurso,
)
from ..schemas import AnuncioCreate, AnuncioPublic, CursoPublic, UsuarioPublic

ROLES_QUE_PUBLICAN = {ROL_ADMIN, ROL_DOCENTE}


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _rol_nombre(session: Session, rol_id: int) -> str:
    rol = session.get(Rol, rol_id)
    return rol.nombre if rol else ""


def _cursos_de(session: Session, usuario: Usuario) -> set[int]:
    filas = session.exec(
        select(UsuarioXCurso.curso_id).where(UsuarioXCurso.usuario_id == usuario.id)
    ).all()
    return set(filas)


def _roles_destino_ids(session: Session, anuncio_id: int) -> set[int]:
    return set(
        session.exec(
            select(AnuncioRol.rol_id).where(AnuncioRol.anuncio_id == anuncio_id)
        ).all()
    )


def _cursos_destino_ids(session: Session, anuncio_id: int) -> set[int]:
    return set(
        session.exec(
            select(AnuncioCurso.curso_id).where(AnuncioCurso.anuncio_id == anuncio_id)
        ).all()
    )


# --------------------------------------------------------------------------- #
# Visibilidad                                                                 #
# --------------------------------------------------------------------------- #
def puede_ver(session: Session, usuario: Usuario, anuncio: Anuncio) -> bool:
    """Indica si `usuario` está autorizado a ver `anuncio`."""
    if anuncio.autor_id == usuario.id:
        return True
    if _rol_nombre(session, usuario.rol_id) == ROL_ADMIN:
        return True
    if usuario.rol_id in _roles_destino_ids(session, anuncio.id):
        return True
    if _cursos_de(session, usuario) & _cursos_destino_ids(session, anuncio.id):
        return True
    return False


def listar_visibles(
    session: Session, usuario: Usuario, tipo: str | None = None
) -> list[Anuncio]:
    """Anuncios visibles para `usuario`, del más reciente al más antiguo."""
    base = select(Anuncio)
    if tipo:
        base = base.where(Anuncio.tipo == tipo)

    orden = (col(Anuncio.fecha_publicacion).desc(), col(Anuncio.id).desc())

    if _rol_nombre(session, usuario.rol_id) == ROL_ADMIN:
        return list(session.exec(base.order_by(*orden)))

    ids_por_rol = set(
        session.exec(
            select(AnuncioRol.anuncio_id).where(AnuncioRol.rol_id == usuario.rol_id)
        ).all()
    )
    ids_por_curso: set[int] = set()
    cursos_ids = _cursos_de(session, usuario)
    if cursos_ids:
        ids_por_curso = set(
            session.exec(
                select(AnuncioCurso.anuncio_id).where(
                    col(AnuncioCurso.curso_id).in_(cursos_ids)
                )
            ).all()
        )

    permitidos = ids_por_rol | ids_por_curso or {-1}  # {-1}: nunca coincide
    stmt = base.where(
        or_(Anuncio.autor_id == usuario.id, col(Anuncio.id).in_(permitidos))
    ).order_by(*orden)
    return list(session.exec(stmt))


def obtener_visible(session: Session, usuario: Usuario, anuncio_id: int) -> Anuncio:
    anuncio = session.get(Anuncio, anuncio_id)
    if anuncio is None or not puede_ver(session, usuario, anuncio):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Anuncio no encontrado"
        )
    return anuncio


# --------------------------------------------------------------------------- #
# Creación                                                                    #
# --------------------------------------------------------------------------- #
def crear_anuncio(session: Session, autor: Usuario, data: AnuncioCreate) -> Anuncio:
    """Crea un anuncio y registra sus destinatarios, validando permisos.

    - Solo Administrador y Docente pueden publicar.
    - El anuncio debe tener al menos un destinatario (rol o curso).
    - El Docente solo puede dirigir anuncios a los cursos que dicta y no puede
      segmentar por rol (evita difusión masiva fuera de su curso).
    """
    rol_autor = _rol_nombre(session, autor.rol_id)
    if rol_autor not in ROLES_QUE_PUBLICAN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo un Administrador o Docente puede crear anuncios",
        )

    roles_pedidos = {n.strip() for n in data.roles_destino if n and n.strip()}
    cursos_pedidos = {int(c) for c in data.cursos_destino}

    if not roles_pedidos and not cursos_pedidos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El anuncio debe tener al menos un rol o curso destinatario",
        )

    roles = []
    for nombre in roles_pedidos:
        rol = session.exec(select(Rol).where(Rol.nombre == nombre)).first()
        if rol is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Rol destinatario inexistente: {nombre!r}",
            )
        roles.append(rol)

    cursos = []
    for curso_id in cursos_pedidos:
        curso = session.get(Curso, curso_id)
        if curso is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Curso destinatario inexistente: {curso_id}",
            )
        cursos.append(curso)

    if rol_autor == ROL_DOCENTE:
        if roles_pedidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Un Docente solo puede dirigir anuncios a sus cursos, no a roles",
            )
        propios = _cursos_de(session, autor)
        ajenos = sorted(c.id for c in cursos if c.id not in propios)
        if ajenos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"El Docente no dicta el/los curso(s): {ajenos}",
            )

    anuncio = Anuncio(
        titulo=data.titulo,
        descripcion=data.descripcion,
        tipo=data.tipo or "anuncio",
        fecha_evento=data.fecha_evento,
        hora_evento=data.hora_evento,
        lugar=data.lugar,
        autor_id=autor.id,
    )
    session.add(anuncio)
    session.commit()
    session.refresh(anuncio)

    for rol in roles:
        session.add(AnuncioRol(anuncio_id=anuncio.id, rol_id=rol.id))
    for curso in cursos:
        session.add(AnuncioCurso(anuncio_id=anuncio.id, curso_id=curso.id))
    session.commit()
    session.refresh(anuncio)
    return anuncio


# --------------------------------------------------------------------------- #
# Serialización                                                               #
# --------------------------------------------------------------------------- #
def serializar(session: Session, anuncio: Anuncio) -> AnuncioPublic:
    autor = session.get(Usuario, anuncio.autor_id)
    autor_public = UsuarioPublic(
        id=autor.id,
        nombre=autor.nombre,
        apellido=autor.apellido,
        correo=autor.correo,
        rol=_rol_nombre(session, autor.rol_id),
    )
    roles = session.exec(
        select(Rol.nombre)
        .join(AnuncioRol, col(AnuncioRol.rol_id) == col(Rol.id))
        .where(AnuncioRol.anuncio_id == anuncio.id)
        .order_by(col(Rol.nombre))
    ).all()
    cursos = session.exec(
        select(Curso)
        .join(AnuncioCurso, col(AnuncioCurso.curso_id) == col(Curso.id))
        .where(AnuncioCurso.anuncio_id == anuncio.id)
        .order_by(col(Curso.nombre))
    ).all()
    return AnuncioPublic(
        id=anuncio.id,
        titulo=anuncio.titulo,
        descripcion=anuncio.descripcion,
        tipo=anuncio.tipo,
        fecha_publicacion=anuncio.fecha_publicacion,
        fecha_evento=anuncio.fecha_evento,
        hora_evento=anuncio.hora_evento,
        lugar=anuncio.lugar,
        autor=autor_public,
        roles_destino=list(roles),
        cursos_destino=[CursoPublic.model_validate(c) for c in cursos],
    )
