"""Endpoints del Módulo de Publicación de Anuncios.

    POST /anuncios        -> crear anuncio (Administrador / Docente)
    GET  /anuncios        -> listar anuncios visibles para el usuario conectado
    GET  /anuncios/{id}   -> ver un anuncio (404 si no es destinatario)
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from ..database import get_session
from ..models import Usuario
from ..schemas import AnuncioCreate, AnuncioPublic
from ..security import get_current_user
from ..services import anuncios as service

router = APIRouter(prefix="/anuncios", tags=["anuncios"])


@router.post(
    "",
    response_model=AnuncioPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un anuncio dirigido a roles o cursos",
)
def crear_anuncio(
    body: AnuncioCreate,
    user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> AnuncioPublic:
    anuncio = service.crear_anuncio(session, user, body)
    return service.serializar(session, anuncio)


@router.get(
    "",
    response_model=list[AnuncioPublic],
    summary="Listar los anuncios visibles para el usuario conectado",
)
def listar_anuncios(
    tipo: str | None = Query(default=None, description="Filtra por tipo, p. ej. 'anuncio'"),
    user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> list[AnuncioPublic]:
    return [
        service.serializar(session, a)
        for a in service.listar_visibles(session, user, tipo)
    ]


@router.get(
    "/{anuncio_id}",
    response_model=AnuncioPublic,
    summary="Ver un anuncio por id (solo si el usuario es destinatario)",
)
def obtener_anuncio(
    anuncio_id: int,
    user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> AnuncioPublic:
    anuncio = service.obtener_visible(session, user, anuncio_id)
    return service.serializar(session, anuncio)
