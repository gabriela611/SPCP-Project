"""Endpoints de autenticación (versión simplificada de laboratorio)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Usuario
from ..schemas import LoginRequest, TokenResponse, UsuarioPublic
from ..security import get_current_user, rol_nombre

router = APIRouter(prefix="/auth", tags=["auth"])


def _to_public(session: Session, user: Usuario) -> UsuarioPublic:
    return UsuarioPublic(
        id=user.id,
        nombre=user.nombre,
        apellido=user.apellido,
        correo=user.correo,
        rol=rol_nombre(session, user),
    )


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, session: Session = Depends(get_session)) -> TokenResponse:
    """Autentica por correo y devuelve un token (el `id` del usuario)."""
    user = session.exec(select(Usuario).where(Usuario.correo == body.correo)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Correo no registrado"
        )
    return TokenResponse(access_token=str(user.id), usuario=_to_public(session, user))


@router.get("/me", response_model=UsuarioPublic)
def me(
    user: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> UsuarioPublic:
    return _to_public(session, user)
