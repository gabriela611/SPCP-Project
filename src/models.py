"""Modelo de datos (tablas SQLModel).

Sigue `docs/designs/diagramaModeloDeDatos-Labclass-PDS.drawio.png`:

    Rol 1---n Usuario n---1 Rol
    Usuario 1---n UsuarioXCurso n---1 Curso
    Usuario 1---n Publicacion

`Anuncio` corresponde a la entidad `publicacion` del diagrama filtrada por
`tipo`. Para cumplir "un anuncio solo es visible para los roles o grupos
destinatarios" se agregan dos tablas de destinatarios:

    Anuncio 1---n AnuncioRol   n---1 Rol     (destinatarios por rol)
    Anuncio 1---n AnuncioCurso n---1 Curso   (destinatarios por curso/grupo)
"""

from __future__ import annotations

from datetime import date, datetime, time, timezone

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

# Nombres canónicos de los roles del sistema (SOW · sección Roles).
ROL_ADMIN = "Administrador"
ROL_DOCENTE = "Docente"
ROL_PADRE = "Padre de familia"

TIPO_ANUNCIO = "anuncio"


class Rol(SQLModel, table=True):
    __tablename__ = "rol"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True)


class Curso(SQLModel, table=True):
    __tablename__ = "curso"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    grado: str


class Usuario(SQLModel, table=True):
    __tablename__ = "usuario"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    correo: str = Field(index=True, unique=True)
    rol_id: int = Field(foreign_key="rol.id", index=True)


class UsuarioXCurso(SQLModel, table=True):
    __tablename__ = "usuario_x_curso"
    __table_args__ = (UniqueConstraint("usuario_id", "curso_id"),)

    id: int | None = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    curso_id: int = Field(foreign_key="curso.id", index=True)


class Anuncio(SQLModel, table=True):
    __tablename__ = "anuncio"

    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    tipo: str = Field(default=TIPO_ANUNCIO, index=True)
    fecha_publicacion: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    # Campos opcionales heredados de `publicacion` (útiles cuando tipo == "evento").
    fecha_evento: date | None = None
    hora_evento: time | None = None
    lugar: str | None = None
    autor_id: int = Field(foreign_key="usuario.id", index=True)


class AnuncioRol(SQLModel, table=True):
    """Destinatario de un anuncio expresado como rol (p. ej. todos los padres)."""

    __tablename__ = "anuncio_rol"
    __table_args__ = (UniqueConstraint("anuncio_id", "rol_id"),)

    id: int | None = Field(default=None, primary_key=True)
    anuncio_id: int = Field(foreign_key="anuncio.id", index=True)
    rol_id: int = Field(foreign_key="rol.id", index=True)


class AnuncioCurso(SQLModel, table=True):
    """Destinatario de un anuncio expresado como curso/grupo."""

    __tablename__ = "anuncio_curso"
    __table_args__ = (UniqueConstraint("anuncio_id", "curso_id"),)

    id: int | None = Field(default=None, primary_key=True)
    anuncio_id: int = Field(foreign_key="anuncio.id", index=True)
    curso_id: int = Field(foreign_key="curso.id", index=True)
