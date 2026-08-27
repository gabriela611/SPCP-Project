"""Punto de entrada de la API del Portal de Comunicación (SPCP).

Arranque local:

    pip install -r src/requirements.txt
    uvicorn src.main:app --reload

Documentación interactiva: http://localhost:8000/docs
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import init_db
from .routers import anuncios, auth, catalogos
from .seed import seed_if_empty


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    seed_if_empty()
    yield


app = FastAPI(
    title="SPCP · Módulo de Publicación de Anuncios",
    version="0.1.0",
    description=(
        "Creación y visualización de anuncios con filtrado estricto por rol y "
        "por curso (grupo destinatario)."
    ),
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(catalogos.router)
app.include_router(anuncios.router)


@app.get("/", tags=["salud"], summary="Estado del servicio")
def raiz() -> dict[str, str]:
    return {"servicio": app.title, "version": app.version, "estado": "ok"}
