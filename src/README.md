# Backend SPCP · Módulo de Publicación de Anuncios

Adaptación del starter FastAPI de referencia para **crear y visualizar anuncios**
con filtrado estricto por rol y por curso.

> Un anuncio **solo es visible** para su autor, para el rol Administrador, para
> los usuarios cuyo **rol** figura entre los destinatarios y para los usuarios
> inscritos en alguno de los **cursos** destinatarios. Para el resto no aparece
> en los listados y responde `404` al consultarlo por id.

## Arranque (un solo comando)

```bash
pip install -r src/requirements.txt          # una vez
uvicorn main:app --app-dir src --reload
```

Documentación interactiva: <http://localhost:8000/docs>.
Los datos viven en memoria (`src/data/mock_data.py`); no hay persistencia.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Estado del servicio. |
| POST | `/anuncios?usuario_id=<id>` | Crea un anuncio (solo Administrador o Docente). |
| GET | `/anuncios?usuario_id=<id>&tipo=<opcional>` | Lista los anuncios **visibles** para ese usuario. |
| GET | `/anuncios/{id}?usuario_id=<id>` | Devuelve un anuncio (`404` si no es destinatario). |

No hay autenticación: `usuario_id` (query param) identifica a quien hace la
petición. En producción se sustituye por el token del Auth Service.

### Cuerpo de `POST /anuncios`

```json
{
  "titulo": "Salida pedagógica",
  "descripcion": "Nos vemos en la portería a las 7:00 am",
  "tipo": "evento",
  "fecha_evento": "2026-09-10",
  "hora_evento": "07:00",
  "lugar": "Portería principal",
  "roles_destino_ids": [],
  "cursos_destino_ids": [1]
}
```

`titulo` y `descripcion` son obligatorios; debe indicarse al menos un
destinatario en `roles_destino_ids` o `cursos_destino_ids`.

### Reglas de creación

- Solo **Administrador** y **Docente** publican (`403` en otro caso).
- El anuncio debe tener **al menos un destinatario** (rol o curso), si no `400`.
- El **Docente** solo puede dirigir anuncios a los **cursos que dicta** y no
  puede segmentar por rol → `403`.
- El **Administrador** puede dirigir a cualquier rol y/o curso.
- Cuerpo inválido (campos faltantes, longitud, tipo) → `422` con `{"detail": ...}`.

## Datos de ejemplo (`src/data/mock_data.py`)

Cursos: `1 = Quinto A`, `2 = Sexto B`.

| `usuario_id` | Correo | Rol | Cursos |
|---|---|---|---|
| 1 | `admin@bfa.edu` | Administrador | — |
| 2 | `diego@bfa.edu` | Docente | Quinto A |
| 3 | `elena@bfa.edu` | Docente | Sexto B |
| 4 | `pedro@bfa.edu` | Padre de familia | Quinto A |
| 5 | `paula@bfa.edu` | Padre de familia | Sexto B |
| 6 | `pablo@bfa.edu` | Padre de familia | Quinto A + Sexto B |

### Ejemplo

```bash
# Diego (Docente de Quinto A) publica un anuncio para su curso
curl -s "http://localhost:8000/anuncios?usuario_id=2" \
  -H 'Content-Type: application/json' \
  -d '{"titulo":"Reunión de padres","descripcion":"Viernes 3pm","cursos_destino_ids":[1]}'

# Pedro (Padre de Quinto A) lo ve; Paula (Sexto B) no
curl -s "http://localhost:8000/anuncios?usuario_id=4"
curl -s "http://localhost:8000/anuncios?usuario_id=5"
```

## Pruebas

```bash
cd src && python -m pytest
```

14 pruebas: permisos de creación, validación de entrada y visibilidad por
rol/curso (incluye casos que no son el "caso feliz").

## Estructura

```
src/
├── main.py                 # App FastAPI, rutas y esquema de entrada (AnuncioCreate)
├── requirements.txt        # Manifiesto de dependencias
├── conftest.py             # sys.path + reseteo de datos en memoria entre pruebas
├── data/
│   └── mock_data.py        # roles, cursos, usuarios, anuncios (listas de dicts)
├── services/
│   └── anuncio_service.py  # Reglas: puede_ver, listar_anuncios_visibles,
│                           #         obtener_anuncio_visible, crear_anuncio
└── tests/
    └── test_anuncios.py
```
