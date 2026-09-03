# AGENTS.md — SPCP · Módulo de Publicación de Anuncios

Guía para agentes que trabajen en esta rama. Describe **qué** hay que construir
y **cómo** debe verse, tomando como base el código de referencia de `src/`.

## Objetivo

Implementar en el backend la **creación y visualización de anuncios** del Portal
de Comunicación para Padres de Familia (SPCP) de Bright Future Academy.

Regla de negocio central (SOW · *"filtrado segmentado estrictamente según el
rol"*): **un anuncio solo es visible para los roles o los grupos (cursos)
destinatarios**, además de su autor y del Administrador. Para cualquier otro
usuario el anuncio no existe.

## Roles

| Rol | En los anuncios |
|---|---|
| **Administrador** | Crea anuncios institucionales dirigidos a cualquier rol y/o curso. Ve todos los anuncios. |
| **Docente** | Crea anuncios dirigidos únicamente a los cursos que dicta. Ve los anuncios de sus cursos, los dirigidos a su rol y los que creó. |
| **Padre de familia** | No crea anuncios. Ve los anuncios dirigidos a su rol y a los cursos en los que tiene un hijo. |

## Restricciones

1. **Adaptar el código de referencia de `src/`** sin cambiar su estilo:
   arquitectura por capas `main → services → data`, datos en memoria (sin base
   de datos ni ORM), imports relativos a `src/`, respuestas JSON como
   listas/objetos planos.
2. Sin autenticación real. El usuario que hace la petición se identifica con el
   parámetro de consulta `usuario_id` (documentado en el README).
3. No agregar dependencias fuera de `src/requirements.txt`. Si se necesita una
   nueva, se declara ahí.
4. No inventar endpoints, campos ni archivos que el problema no pida.
5. Python 3.12 + FastAPI. Dominio en español (nombres de campos y mensajes).
6. El servicio arranca con **un solo comando documentado**.
7. Los errores se devuelven como `{"detail": "..."}` con el código HTTP correcto.

## Criterios de aceptación

`SHALL` = obligatorio. Cumple o no cumple, sin puntos intermedios.

1. El sistema SHALL permitir a un **Administrador** o **Docente** crear un
   anuncio con `titulo`, `descripcion` y al menos un destinatario
   (`roles_destino_ids` y/o `cursos_destino_ids`), y responder **201** con el
   anuncio creado.
2. El sistema SHALL rechazar con **400** un anuncio sin ningún destinatario.
3. El sistema SHALL rechazar con **403** la creación de anuncios por un
   **Padre de familia**.
4. El sistema SHALL rechazar con **403** un anuncio de un **Docente** dirigido a
   un curso que no dicta o segmentado por rol.
5. El sistema SHALL validar el cuerpo de la petición y responder **422** con
   detalle estructurado cuando falten campos o no cumplan longitud/tipo.
6. `GET /anuncios?usuario_id=<id>` SHALL devolver **solo** los anuncios visibles
   para ese usuario según la regla de negocio (autor + Administrador + rol
   destinatario + curso destinatario).
7. `GET /anuncios/{id}?usuario_id=<id>` SHALL responder **404** si el anuncio no
   es visible para ese usuario (no revela su existencia).
8. `GET /anuncios` SHALL aceptar el filtro opcional `tipo`.
9. El proyecto SHALL incluir al menos una prueba automatizada que ejercite la
   regla de visibilidad (no solo el caso feliz) y todas SHALL pasar.
10. Todas las dependencias SHALL estar declaradas en `src/requirements.txt` y el
    comando de arranque SHALL estar documentado en `src/README.md`.

## Formato a seguir

### Estructura de carpetas

```
src/
├── main.py                     # App FastAPI, rutas y esquema de entrada
├── requirements.txt            # Manifiesto de dependencias
├── README.md                   # Comando de arranque y uso
├── conftest.py                 # sys.path + reseteo de datos para las pruebas
├── data/
│   └── mock_data.py            # Catálogos y datos en memoria (listas de dicts)
├── services/
│   └── anuncio_service.py      # Reglas de negocio: crear / listar / obtener
└── tests/
    └── test_anuncios.py        # Pruebas (pytest + TestClient)
```

### Convenciones (heredadas del código de referencia)

- **Imports** relativos a `src/`: `from data.mock_data import ...`,
  `from services.anuncio_service import ...`. La app se ejecuta con `src/` en el
  path (`--app-dir src`).
- **Capas**: `main.py` solo define rutas y el esquema de entrada y delega en
  `services/`; `services/` contiene la lógica y opera sobre las listas de
  `data/mock_data.py`; `data/` no importa de las otras capas.
- **Datos**: listas de diccionarios en memoria. `crear_anuncio` hace `append`
  sobre la lista `anuncios`. No hay persistencia entre reinicios.
- **Rutas REST**: recurso en plural `/anuncios`; `POST` crea, `GET` lista,
  `GET /anuncios/{id}` consulta uno. El identificador del solicitante viaja
  siempre como query param `usuario_id`.
- **Respuestas**: el objeto anuncio se devuelve tal cual se almacena:

  ```json
  {
    "id": 2,
    "titulo": "Salida pedagógica Quinto A",
    "descripcion": "Nos encontramos en la portería a las 7:00 am.",
    "tipo": "evento",
    "fecha_publicacion": "2026-08-20",
    "fecha_evento": "2026-09-05",
    "hora_evento": "07:00",
    "lugar": "Portería principal",
    "autor_id": 2,
    "roles_destino_ids": [],
    "cursos_destino_ids": [1]
  }
  ```

  Las colecciones se devuelven como lista JSON de ese objeto. Los errores como
  `{"detail": "<mensaje>"}`.
- **Errores**: `raise HTTPException(status_code=..., detail="...")` desde
  `services/`.

### Comando de arranque

```
uvicorn main:app --app-dir src --reload
```

Pruebas: `cd src && python -m pytest`.
