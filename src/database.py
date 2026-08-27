"""Configuración de la base de datos (SQLite + SQLModel).

Se usa SQLite por simplicidad del laboratorio; el diagrama de arquitectura
contempla una base de datos SQL relacional, por lo que el modelo es portable a
PostgreSQL/MySQL cambiando únicamente `DATABASE_URL`.
"""

from __future__ import annotations

import os
from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv("SPCP_DATABASE_URL", "sqlite:///./spcp.db")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)


def init_db() -> None:
    """Crea las tablas declaradas en `src.models` si no existen."""
    # Import perezoso para registrar los modelos en `SQLModel.metadata`.
    from . import models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Dependencia de FastAPI: entrega una sesión por request y la cierra al final."""
    with Session(engine) as session:
        yield session
