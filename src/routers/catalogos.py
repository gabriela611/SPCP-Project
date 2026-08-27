"""Endpoints de solo lectura para poblar selectores del frontend."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import Session, col, select

from ..database import get_session
from ..models import Curso, Rol
from ..schemas import CursoPublic, RolPublic
from ..security import get_current_user

router = APIRouter(tags=["catálogos"], dependencies=[Depends(get_current_user)])


@router.get("/roles", response_model=list[RolPublic])
def listar_roles(session: Session = Depends(get_session)) -> list[Rol]:
    return list(session.exec(select(Rol).order_by(col(Rol.id))))


@router.get("/cursos", response_model=list[CursoPublic])
def listar_cursos(session: Session = Depends(get_session)) -> list[Curso]:
    return list(session.exec(select(Curso).order_by(col(Curso.nombre))))
