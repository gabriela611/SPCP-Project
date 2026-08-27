"""Fixtures compartidas: base de datos en memoria + cliente HTTP autenticado."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from src.database import get_session
from src.main import app
from src.seed import seed


@pytest.fixture()
def session() -> Iterator[Session]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        seed(s)
        yield s


@pytest.fixture()
def client(session: Session) -> Iterator[TestClient]:
    def _get_session() -> Iterator[Session]:
        yield session

    app.dependency_overrides[get_session] = _get_session
    # Sin `with`: no dispara el lifespan y no toca la base real.
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture()
def login(client: TestClient):
    """Devuelve una función correo -> headers con el token bearer."""

    def _login(correo: str) -> dict[str, str]:
        resp = client.post("/auth/login", json={"correo": correo})
        assert resp.status_code == 200, resp.text
        return {"Authorization": f"Bearer {resp.json()['access_token']}"}

    return _login
