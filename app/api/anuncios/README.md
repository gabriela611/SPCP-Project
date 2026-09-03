# API de Anuncios — Bright Future

Arranque en un comando:

```bash
npm install
npm run dev
```

Servidor: `http://localhost:3000`

## Rutas

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/anuncios` | Crear anuncio |
| `GET` | `/api/anuncios` | Listar anuncios visibles para el usuario |
| `PATCH` | `/api/anuncios/[id]` | Cambiar estado (`borrador` \| `publicado` \| `archivado`) |

## Visibilidad

El listado no es global: solo devuelve anuncios cuyo `rolesDestinatarios` incluye el **rol** o el **grupo** del solicitante.

Headers (sustituto de sesión; no se modificó un módulo de autenticación):

- `x-user-role` — p. ej. `padre`, `docente`, `administrador`
- `x-user-grupo` — p. ej. `5A`

## Ejemplo

```bash
curl -X POST http://localhost:3000/api/anuncios ^
  -H "Content-Type: application/json" ^
  -d "{\"titulo\":\"Reunión\",\"contenido\":\"Martes 8:00\",\"rolesDestinatarios\":[\"padre\"]}"

curl http://localhost:3000/api/anuncios -H "x-user-role: docente"
```

El segundo `GET` debe devolver `{ "data": [], "error": null }` porque `docente` no es destinatario.

## Pruebas

```bash
npm test
```
