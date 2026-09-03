# SPCP · Portal de Comunicación para Padres de Familia

Repositorio del proyecto **SPCP** para *Bright Future Academy*: un portal web
centralizado que reemplaza los canales informales de comunicación del colegio.
El sistema completo (según el SOW) tiene tres módulos —publicación de anuncios
filtrada por rol, calendario de eventos con notificaciones por correo, y panel de
seguimiento de lectura de mensajes— y tres roles de usuario: **Administrador**,
**Docente** y **Padre de familia**.

Este repositorio contiene la **documentación del proyecto** y la implementación
backend de dos *slices* verticales, desarrollados como parte del Laboratorio 03.

## Contexto académico (Laboratorio 03)

El laboratorio es un experimento sobre ingeniería de prompts y contexto para
agentes de código:

1. **La escalera** — se pidió el mismo endpoint (Publicación de Anuncios) en
   cuatro prompts de especificidad creciente y se calificó cada resultado contra
   una lista fija de 8 criterios. Ver [`docs/ai/escalera-lab03.md`](docs/ai/escalera-lab03.md).
2. **El `AGENTS.md`** — se tomó el mejor resultado de la escalera y se escribió
   [`AGENTS.md`](AGENTS.md) con todo el contexto que había que repetir en cada
   prompt (convenciones, estructura, criterios de aceptación).
3. **El segundo slice** — se implementó un segundo endpoint
   ([issue #4](https://github.com/gabriela611/SPCP-Project/issues/4):
   Autenticación y gestión de roles) apoyándose solo en `AGENTS.md`, sin volver a
   repetir el contexto en el prompt.

Las ramas `V1`–`V4` conservan las cuatro versiones de la escalera; `main` integra
el resultado final más el segundo slice. El detalle de herramientas usadas está
en [`docs/ai/uso-ia.md`](docs/ai/uso-ia.md).

## Estructura del repositorio

```
.
├── AGENTS.md                 # Especificación y convenciones para agentes (módulo de anuncios)
├── README.md                 # Este archivo
├── .github/ISSUE_TEMPLATE/    # Plantilla de issues en formato RFP
├── docs/
│   ├── proposals/            # Statement of Work y plantilla de propuesta
│   ├── designs/              # Diagramas UML y mockups
│   └── ai/                   # Entregables del laboratorio de IA
├── src/                      # Slice 1 · Módulo de Publicación de Anuncios (FastAPI)
└── srcprueba/                # Slice 2 · Autenticación y gestión de roles (FastAPI)
```

### `docs/`

| Ruta | Contenido |
|------|-----------|
| `docs/proposals/statement_of_work.md` | SOW: alcance, valor, pagos, roles, matriz RACI y métricas de rendimiento del proyecto. |
| `docs/proposals/software proyect porposal template.png` | Plantilla de propuesta de software. |
| `docs/designs/Diagrama Casos de Uso.jpeg` | Casos de uso por actor (Administrador / Docente / Padre) y por módulo. |
| `docs/designs/Diagrama de arquitectura.pdf` | Arquitectura de despliegue: clientes → SPA → nube (API Gateway, servicios, BD SQL, respaldo, proveedor de correo). |
| `docs/designs/Diagrama de componentes.pdf` | Componentes del frontend y backend y tablas de la base de datos. |
| `docs/designs/diagramaModeloDeDatos-Labclass-PDS.drawio.png` | Modelo de datos: `Rol`, `Usuario`, `UsuarioXCurso`, `Curso`, `publicacion`. |
| `docs/designs/mockups.md` | Enlace a Figma y capturas de las pantallas. |
| `docs/ai/escalera-lab03.md` | Experimento de la escalera: 4 prompts, calificaciones (2/5/7/8), alucinaciones y conclusión. |
| `docs/ai/uso-ia.md` | Herramientas de IA usadas por versión (Claude Code / Cursor). |
| `docs/ai/prompts/pedir-codigo.md` | Plantilla de prompt para pedir código. |
| `docs/ai/prompts/debug.md` | Plantilla de prompt para depurar. |
| `docs/ai/prompts/documentar-codigo.md` | Plantilla de prompt para documentar código. |

### `AGENTS.md`

Guía que define **qué** construir y **cómo** debe verse el código del módulo de
anuncios: objetivo y regla de negocio, roles, restricciones, 10 criterios de
aceptación `SHALL` y el formato a seguir (estructura de carpetas, convenciones
heredadas del starter, formato de respuesta y comando de arranque). Es el
contrato que el segundo slice reutiliza sin repetir contexto.

## Backend

Ambos *slices* son APIs FastAPI independientes, **sin base de datos**: los datos
viven en listas de diccionarios en memoria (`data/mock_data.py`) y se pierden al
reiniciar. Comparten arquitectura por capas `main → services → data`, imports
relativos a la carpeta de la app, identificación del solicitante por el query
param `usuario_id`, respuestas JSON planas y errores `{"detail": "..."}`.

Requisitos: Python 3.12. Instalar dependencias con
`pip install -r <carpeta>/requirements.txt`.

### `src/` — Módulo de Publicación de Anuncios

Creación y visualización de anuncios con filtrado segmentado: **un anuncio solo
es visible para su autor, para el Administrador, para los usuarios cuyo rol es
destinatario y para los inscritos en un curso destinatario.**

| | |
|---|---|
| Rutas | `POST /anuncios`, `GET /anuncios`, `GET /anuncios/{id}` (todas con `usuario_id`) |
| Lógica | `src/services/anuncio_service.py` — `crear_anuncio`, `listar_anuncios_visibles`, `obtener_anuncio_visible`, `puede_ver` |
| Arranque | `uvicorn main:app --app-dir src --reload` |
| Pruebas | `cd src && python -m pytest` — 14 pruebas |
| Detalle | [`src/README.md`](src/README.md) |

### `srcprueba/` — Autenticación y gestión de roles (issue #4)

Login por correo/contraseña que asigna uno de los tres roles y restringe el
acceso a las funcionalidades según una matriz `permisos_por_rol`.

| | |
|---|---|
| Rutas | `POST /sesiones`, `GET /sesiones/{token}`, `GET /permisos?usuario_id=&funcionalidad=` |
| Lógica | `srcprueba/services/auth_service.py` — `autenticar`, `obtener_sesion`, `permisos_de`, `verificar_acceso` |
| Arranque | `uvicorn main:app --app-dir srcprueba --reload` |
| Pruebas | `cd srcprueba && python -m pytest` — 11 pruebas |
| Detalle | [`srcprueba/README.md`](srcprueba/README.md) |

## Inicio rápido

```bash
# Slice 1 — Anuncios
pip install -r src/requirements.txt
uvicorn main:app --app-dir src --reload          # http://localhost:8000/docs

# Slice 2 — Autenticación y roles
pip install -r srcprueba/requirements.txt
uvicorn main:app --app-dir srcprueba --reload    # http://localhost:8000/docs
```

Cada servicio se levanta por separado (ambos usan el puerto 8000 por defecto).

## Ramas

| Rama | Contenido |
|------|-----------|
| `main` | Resultado integrado: documentación + `src/` + `srcprueba/`. |
| `V1`–`V4` | Las cuatro versiones de la escalera de prompts del Laboratorio 03. |
