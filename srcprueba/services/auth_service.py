"""Reglas de negocio de Autenticación y gestión de roles (issue #4).

El sistema autentica a un usuario por correo y contraseña, le asigna su rol
(Administrador, Docente o Padre de familia) y restringe el acceso a las
funcionalidades según la matriz `permisos_por_rol`.
"""

import secrets

from fastapi import HTTPException

from data.mock_data import permisos_por_rol, roles, sesiones, usuarios


# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def _nombre_rol(rol_id):
    rol = next((r for r in roles if r["id"] == rol_id), None)
    return rol["nombre"] if rol else ""


def _usuario(usuario_id):
    usuario = next((u for u in usuarios if u["id"] == usuario_id), None)
    if usuario is None:
        raise HTTPException(status_code=401, detail="usuario_id no válido")
    return usuario


# --------------------------------------------------------------------------- #
# Autenticación                                                               #
# --------------------------------------------------------------------------- #
def autenticar(correo, contrasena):
    usuario = next((u for u in usuarios if u["correo"] == correo), None)
    if usuario is None or usuario["contrasena"] != contrasena:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    nombre_rol = _nombre_rol(usuario["rol_id"])
    sesion = {
        "token": secrets.token_hex(16),
        "usuario_id": usuario["id"],
        "rol": nombre_rol,
        "permisos": permisos_por_rol.get(nombre_rol, []),
    }
    sesiones.append(sesion)
    return sesion


def obtener_sesion(token):
    sesion = next((s for s in sesiones if s["token"] == token), None)
    if sesion is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return sesion


# --------------------------------------------------------------------------- #
# Control de acceso por rol                                                   #
# --------------------------------------------------------------------------- #
def permisos_de(usuario_id):
    usuario = _usuario(usuario_id)
    return permisos_por_rol.get(_nombre_rol(usuario["rol_id"]), [])


def verificar_acceso(usuario_id, funcionalidad):
    usuario = _usuario(usuario_id)
    nombre_rol = _nombre_rol(usuario["rol_id"])
    if funcionalidad not in permisos_por_rol.get(nombre_rol, []):
        raise HTTPException(
            status_code=403,
            detail=f"El rol {nombre_rol!r} no tiene acceso a {funcionalidad!r}",
        )
    return {
        "permitido": True,
        "usuario_id": usuario_id,
        "rol": nombre_rol,
        "funcionalidad": funcionalidad,
    }
