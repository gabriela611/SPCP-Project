from fastapi import FastAPI
from pydantic import BaseModel, Field

from data.mock_data import mock_data
from services.anuncio_service import (
    crear_anuncio,
    listar_anuncios_visibles,
    obtener_anuncio_visible,
)

app = FastAPI(
    title="SPCP · Módulo de Publicación de Anuncios",
    description="Creación y visualización de anuncios con filtrado por rol y curso.",
    version="0.1.0",
)


class AnuncioCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=200)
    descripcion: str = Field(min_length=1)
    tipo: str = "anuncio"
    fecha_evento: str | None = None
    hora_evento: str | None = None
    lugar: str | None = None
    roles_destino_ids: list[int] = Field(default_factory=list)
    cursos_destino_ids: list[int] = Field(default_factory=list)


@app.get("/")
def read_root():
    return mock_data


@app.post("/anuncios", status_code=201)
def crear(usuario_id: int, anuncio: AnuncioCreate):
    return crear_anuncio(usuario_id, anuncio.model_dump())


@app.get("/anuncios")
def listar(usuario_id: int, tipo: str | None = None):
    return listar_anuncios_visibles(usuario_id, tipo)


@app.get("/anuncios/{anuncio_id}")
def obtener(anuncio_id: int, usuario_id: int):
    return obtener_anuncio_visible(usuario_id, anuncio_id)
