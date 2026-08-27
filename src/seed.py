"""Datos iniciales de demostración.

Ejecutar de forma independiente:

    python -m src.seed

También se llama automáticamente al arrancar la app si la base está vacía.
"""

from __future__ import annotations

from sqlmodel import Session, select

from .database import engine, init_db
from .models import (
    ROL_ADMIN,
    ROL_DOCENTE,
    ROL_PADRE,
    Curso,
    Rol,
    Usuario,
    UsuarioXCurso,
)


def seed(session: Session) -> None:
    """Inserta roles, cursos y usuarios de ejemplo. Idempotente."""
    if session.exec(select(Rol)).first() is not None:
        return

    roles = {
        ROL_ADMIN: Rol(nombre=ROL_ADMIN),
        ROL_DOCENTE: Rol(nombre=ROL_DOCENTE),
        ROL_PADRE: Rol(nombre=ROL_PADRE),
    }
    session.add_all(roles.values())

    quinto = Curso(nombre="Quinto A", grado="5")
    sexto = Curso(nombre="Sexto B", grado="6")
    session.add_all([quinto, sexto])
    session.commit()
    for obj in (*roles.values(), quinto, sexto):
        session.refresh(obj)

    usuarios = {
        "admin": Usuario(
            nombre="Ana", apellido="Admin", correo="admin@bfa.edu",
            rol_id=roles[ROL_ADMIN].id,
        ),
        "diego": Usuario(
            nombre="Diego", apellido="Docente", correo="diego@bfa.edu",
            rol_id=roles[ROL_DOCENTE].id,
        ),
        "elena": Usuario(
            nombre="Elena", apellido="Docente", correo="elena@bfa.edu",
            rol_id=roles[ROL_DOCENTE].id,
        ),
        "pedro": Usuario(
            nombre="Pedro", apellido="Perez", correo="pedro@bfa.edu",
            rol_id=roles[ROL_PADRE].id,
        ),
        "paula": Usuario(
            nombre="Paula", apellido="Paz", correo="paula@bfa.edu",
            rol_id=roles[ROL_PADRE].id,
        ),
        "pablo": Usuario(
            nombre="Pablo", apellido="Pinto", correo="pablo@bfa.edu",
            rol_id=roles[ROL_PADRE].id,
        ),
    }
    session.add_all(usuarios.values())
    session.commit()
    for obj in usuarios.values():
        session.refresh(obj)

    # Inscripciones (UsuarioXCurso):
    #   Diego dicta Quinto A;   Elena dicta Sexto B
    #   Pedro -> Quinto A;      Paula -> Sexto B;   Pablo -> ambos
    inscripciones = [
        (usuarios["diego"], quinto),
        (usuarios["elena"], sexto),
        (usuarios["pedro"], quinto),
        (usuarios["paula"], sexto),
        (usuarios["pablo"], quinto),
        (usuarios["pablo"], sexto),
    ]
    session.add_all(
        UsuarioXCurso(usuario_id=u.id, curso_id=c.id) for u, c in inscripciones
    )
    session.commit()


def seed_if_empty() -> None:
    with Session(engine) as session:
        seed(session)


if __name__ == "__main__":
    init_db()
    seed_if_empty()
    print("Base de datos inicializada con datos de ejemplo.")
