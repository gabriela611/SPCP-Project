/**
 * Recurso Anuncio — Bright Future (SPCP)
 *
 * Arranque: npm run dev  (API en http://localhost:3000/api/anuncios)
 * Identidad de visibilidad (sin módulo de auth): headers
 *   x-user-role   p. ej. padre | docente | administrador
 *   x-user-grupo  p. ej. 5A
 */
import { anuncioDb } from "./_lib/db";
import { jsonError, jsonOk } from "./_lib/http";
import { tieneIdentidad, usuarioDesdeHeaders } from "./_lib/usuario";
import { validarCreacionAnuncio } from "./_lib/validacion";
import { filtrarAnunciosPorVisibilidad } from "./_lib/visibilidad";

export async function GET(request: Request) {
  const usuario = usuarioDesdeHeaders(request.headers);

  if (!tieneIdentidad(usuario)) {
    return jsonError(
      400,
      "IDENTITY_REQUIRED",
      "Indica x-user-role y/o x-user-grupo para filtrar por visibilidad",
    );
  }

  const visibles = filtrarAnunciosPorVisibilidad(anuncioDb.list(), usuario);
  return jsonOk(visibles);
}

export async function POST(request: Request) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return jsonError(400, "INVALID_JSON", "El cuerpo debe ser JSON válido");
  }

  const resultado = validarCreacionAnuncio(body);
  if (!resultado.ok) {
    return jsonError(
      400,
      "VALIDATION_ERROR",
      "Datos de anuncio inválidos",
      resultado.details,
    );
  }

  const creado = anuncioDb.create(resultado.value);
  return jsonOk(creado, 201);
}
