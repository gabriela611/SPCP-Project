"""Esquemas de entrada/salida de la API (Pydantic).

Se mantienen separados de las tablas de `src.models` para no exponer la
estructura interna ni los identificadores de llaves foráneas.
"""

from __future__ import annotations

from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    correo: str


class UsuarioPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    apellido: str
    correo: str
    rol: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioPublic


class RolPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str


class CursoPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    grado: str


class AnuncioCreate(BaseModel):
    """Datos para crear un anuncio.

    Debe indicarse al menos un destinatario (`roles_destino` o `cursos_destino`);
    de lo contrario el anuncio no sería visible para nadie y se rechaza.
    """

    titulo: str = Field(min_length=3, max_length=200)
    descripcion: str = Field(min_length=1)
    tipo: str = "anuncio"
    fecha_evento: date | None = None
    hora_evento: time | None = None
    lugar: str | None = None
    roles_destino: list[str] = Field(
        default_factory=list,
        description="Nombres de rol destinatarios. Reservado al Administrador.",
    )
    cursos_destino: list[int] = Field(
        default_factory=list, description="IDs de curso/grupo destinatarios."
    )


class AnuncioPublic(BaseModel):
    id: int
    titulo: str
    descripcion: str
    tipo: str
    fecha_publicacion: datetime
    fecha_evento: date | None
    hora_evento: time | None
    lugar: str | None
    autor: UsuarioPublic
    roles_destino: list[str]
    cursos_destino: list[CursoPublic]
