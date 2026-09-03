from fastapi import FastAPI
from pydantic import BaseModel, Field

from data.mock_data import mock_data
from services.auth_service import (
    autenticar,
    obtener_sesion,
    permisos_de,
    verificar_acceso,
)

app = FastAPI(
    title="SPCP · Autenticación y gestión de roles",
    description="Login por rol y control de acceso a funcionalidades (issue #4).",
    version="0.1.0",
)


class SesionCreate(BaseModel):
    correo: str = Field(min_length=3)
    contrasena: str = Field(min_length=1)


@app.get("/")
def read_root():
    return mock_data


@app.post("/sesiones", status_code=201)
def iniciar_sesion(credenciales: SesionCreate):
    return autenticar(credenciales.correo, credenciales.contrasena)


@app.get("/sesiones/{token}")
def consultar_sesion(token: str):
    return obtener_sesion(token)


@app.get("/permisos")
def permisos(usuario_id: int, funcionalidad: str | None = None):
    if funcionalidad is None:
        return permisos_de(usuario_id)
    return verificar_acceso(usuario_id, funcionalidad)
