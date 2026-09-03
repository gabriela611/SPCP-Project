# Backend SPCP · Autenticación y gestión de roles (issue #4)

Segundo *slice* del proyecto. Sigue las convenciones de [`AGENTS.md`](../AGENTS.md)
(capas `main → services → data`, datos en memoria, imports relativos a la carpeta
raíz, respuestas JSON planas, errores `{"detail": ...}`, arranque de un comando).

Requisito formal (issue #4 · RFP-011 · SOW · sección Roles):

> El sistema SHALL autenticar usuarios y asignarles uno de los roles
> **Administrador**, **Docente** o **Padre de familia**, restringiendo el acceso
> a las funcionalidades según el rol.

## Arranque (un solo comando)

```bash
pip install -r srcprueba/requirements.txt          # una vez
uvicorn main:app --app-dir srcprueba --reload
```

Documentación interactiva: <http://localhost:8000/docs>. Los datos viven en
memoria (`srcprueba/data/mock_data.py`); no hay persistencia.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Estado del servicio. |
| POST | `/sesiones` | Autentica por `correo` + `contrasena`. `201` con la sesión (token, rol, permisos); `401` si las credenciales no son válidas. |
| GET | `/sesiones/{token}` | Devuelve la sesión activa; `404` si el token no existe. |
| GET | `/permisos?usuario_id=<id>` | Lista de funcionalidades habilitadas para el rol del usuario. |
| GET | `/permisos?usuario_id=<id>&funcionalidad=<clave>` | `200 {"permitido": true, ...}` si el rol habilita esa funcionalidad; `403` si no. |

`usuario_id` (query param) identifica al solicitante, igual que en el resto del
proyecto. `usuario_id` inexistente → `401`. Cuerpo inválido en `POST /sesiones`
→ `422` con detalle estructurado.

### Matriz de acceso por rol (`permisos_por_rol`)

| Funcionalidad | Administrador | Docente | Padre de familia |
|---|:---:|:---:|:---:|
| `anuncios.ver` | ✓ | ✓ | ✓ |
| `anuncios.crear` | ✓ | ✓ | — |
| `eventos.ver` | ✓ | ✓ | ✓ |
| `eventos.crear` | ✓ | ✓ | — |
| `lectura.confirmar` | — | ✓ | ✓ |
| `mensajes.estado.ver` | ✓ | ✓ | — |
| `roles.gestionar` | ✓ | — | — |
| `portal.supervisar` | ✓ | — | — |

## Usuarios de ejemplo (`srcprueba/data/mock_data.py`)

| `usuario_id` | Correo | Contraseña | Rol |
|---|---|---|---|
| 1 | `admin@bfa.edu` | `admin123` | Administrador |
| 2 | `diego@bfa.edu` | `diego123` | Docente |
| 3 | `elena@bfa.edu` | `elena123` | Docente |
| 4 | `pedro@bfa.edu` | `pedro123` | Padre de familia |
| 5 | `paula@bfa.edu` | `paula123` | Padre de familia |

Las contraseñas se guardan en texto plano: es una simplificación de laboratorio.

### Ejemplo

```bash
# Login
curl -s http://localhost:8000/sesiones \
  -H 'Content-Type: application/json' \
  -d '{"correo":"diego@bfa.edu","contrasena":"diego123"}'

# Funcionalidades del rol de un padre
curl -s "http://localhost:8000/permisos?usuario_id=4"

# Acceso bloqueado: un padre no puede crear anuncios -> 403
curl -s -o /dev/null -w '%{http_code}\n' \
  "http://localhost:8000/permisos?usuario_id=4&funcionalidad=anuncios.crear"
```

## Pruebas

```bash
cd srcprueba && python -m pytest
```

11 pruebas: login válido/ inválido, validación de entrada, permisos por rol y
bloqueo de acceso no autorizado (regla de negocio del issue).

## Estructura

```
srcprueba/
├── main.py                 # App FastAPI, rutas y esquema de entrada (SesionCreate)
├── requirements.txt        # Manifiesto de dependencias
├── conftest.py             # sys.path + reseteo de sesiones entre pruebas
├── data/
│   └── mock_data.py        # roles, usuarios, permisos_por_rol, sesiones
├── services/
│   └── auth_service.py     # autenticar, obtener_sesion, permisos_de, verificar_acceso
└── tests/
    └── test_auth.py
```
