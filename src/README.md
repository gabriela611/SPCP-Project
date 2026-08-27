# Backend SPCP · Módulo de Publicación de Anuncios

Implementación en **FastAPI + SQLModel (SQLite)** de la creación y visualización
de anuncios del Portal de Comunicación para Padres de Familia.

Regla principal (SOW · *"filtrado segmentado estrictamente según el rol"*):

> Un anuncio **solo es visible** para su autor, para el rol Administrador, para
> los usuarios cuyo **rol** figura entre los destinatarios, o para los usuarios
> inscritos en alguno de los **cursos** destinatarios. Para el resto, el anuncio
> no aparece en los listados y responde `404` al consultarlo por id.

## Puesta en marcha

```bash
pip install -r src/requirements.txt
uvicorn src.main:app --reload
# Documentación interactiva: http://localhost:8000/docs
```

Al arrancar, si la base está vacía se cargan datos de ejemplo
(`python -m src.seed` los recarga manualmente).

## Modelo de datos

Sigue `docs/designs/diagramaModeloDeDatos-Labclass-PDS.drawio.png`
(`Rol`, `Usuario`, `UsuarioXCurso`, `Curso`, `publicacion`). La entidad
`publicacion` se implementa como `Anuncio` (campo `tipo`, por defecto
`"anuncio"`). Se añaden dos tablas de destinatarios que el diagrama no detallaba
pero que la regla de negocio exige:

| Tabla          | Propósito                                   |
|----------------|---------------------------------------------|
| `anuncio_rol`  | destinatarios de un anuncio por **rol**     |
| `anuncio_curso`| destinatarios de un anuncio por **curso**   |

## Endpoints

| Método | Ruta               | Descripción                                          | Autoriza |
|--------|--------------------|------------------------------------------------------|----------|
| POST   | `/auth/login`      | Login por correo. Devuelve `access_token`.           | —        |
| GET    | `/auth/me`         | Usuario conectado.                                   | token    |
| GET    | `/roles`           | Catálogo de roles.                                   | token    |
| GET    | `/cursos`          | Catálogo de cursos.                                  | token    |
| POST   | `/anuncios`        | Crea un anuncio dirigido a roles y/o cursos.         | Admin / Docente |
| GET    | `/anuncios`        | Lista los anuncios **visibles** para el usuario. `?tipo=` opcional. | token |
| GET    | `/anuncios/{id}`   | Ve un anuncio (404 si no es destinatario).           | token    |

Autenticación: cabecera `Authorization: Bearer <access_token>`.
**Simplificación de laboratorio:** el token es el `id` del usuario; en
producción se sustituye por un JWT del Auth Service sin tocar el resto del código.

### Reglas de creación

- Solo **Administrador** y **Docente** pueden publicar (`403` en otro caso).
- El anuncio debe tener **al menos un destinatario** (rol o curso), si no `400`.
- El **Docente** solo puede dirigir anuncios a los **cursos que dicta** y no
  puede segmentar por rol (evita difusión masiva fuera de su curso) → `403`.
- El **Administrador** puede dirigir a cualquier rol y/o curso.

### Ejemplo

```bash
TOKEN=$(curl -s localhost:8000/auth/login -H 'Content-Type: application/json' \
  -d '{"correo":"diego@bfa.edu"}' | python -c 'import sys,json;print(json.load(sys.stdin)["access_token"])')

curl -s localhost:8000/anuncios -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d '{
    "titulo": "Salida pedagógica",
    "descripcion": "Nos vemos en la entrada a las 7:00 am",
    "fecha_evento": "2026-09-10",
    "hora_evento": "07:00:00",
    "lugar": "Portería principal",
    "cursos_destino": [1]
  }'
```

## Datos de ejemplo (`src/seed.py`)

Cursos: `1 = Quinto A`, `2 = Sexto B`.

| Correo           | Rol             | Cursos            |
|------------------|-----------------|-------------------|
| `admin@bfa.edu`  | Administrador   | —                 |
| `diego@bfa.edu`  | Docente         | Quinto A          |
| `elena@bfa.edu`  | Docente         | Sexto B           |
| `pedro@bfa.edu`  | Padre de familia| Quinto A          |
| `paula@bfa.edu`  | Padre de familia| Sexto B           |
| `pablo@bfa.edu`  | Padre de familia| Quinto A + Sexto B|

## Pruebas

```bash
python -m pytest        # 15 pruebas: permisos de creación y visibilidad por rol/curso
```

## Estructura

```
src/
├── main.py              # App FastAPI + registro de routers + lifespan (init + seed)
├── database.py          # Engine y sesión SQLModel
├── models.py            # Tablas (Rol, Usuario, UsuarioXCurso, Curso, Anuncio, AnuncioRol, AnuncioCurso)
├── schemas.py           # Modelos Pydantic de entrada/salida
├── security.py          # get_current_user (Bearer)
├── seed.py              # Datos de ejemplo
├── routers/
│   ├── auth.py          # /auth/login, /auth/me
│   ├── catalogos.py     # /roles, /cursos
│   └── anuncios.py      # /anuncios (POST, GET, GET/{id})
├── services/
│   └── anuncios.py      # Reglas de negocio: crear, visibilidad, serializar
└── tests/
    ├── conftest.py      # BD en memoria + cliente autenticado
    └── test_anuncios.py
```
