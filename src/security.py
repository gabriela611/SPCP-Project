"""Autenticación e identificación del usuario conectado.

Simplificación de laboratorio: el token bearer es directamente el `id` del
usuario (obtenido en `POST /auth/login`). En producción esto se reemplaza por
un JWT firmado emitido por el Auth Service del diagrama de componentes; el resto
del código no cambia porque solo depende de `get_current_user`.
"""

from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from .database import get_session
from .models import Rol, Usuario

_bearer = HTTPBearer(auto_error=False, description="Token = id de usuario (lab)")


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    session: Session = Depends(get_session),
) -> Usuario:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no proporcionadas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        user_id = int(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        ) from exc

    user = session.get(Usuario, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado"
        )
    return user


def rol_nombre(session: Session, user: Usuario) -> str:
    """Devuelve el nombre del rol del usuario (o cadena vacía si no existe)."""
    rol = session.get(Rol, user.rol_id)
    return rol.nombre if rol else ""
