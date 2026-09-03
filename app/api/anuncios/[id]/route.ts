import { anuncioDb } from "../_lib/db";
import { jsonError, jsonOk } from "../_lib/http";
import { validarCambioEstado } from "../_lib/validacion";

type RutaParams = { params: Promise<{ id: string }> };

export async function PATCH(request: Request, { params }: RutaParams) {
  const { id } = await params;

  if (!anuncioDb.findById(id)) {
    return jsonError(404, "NOT_FOUND", `No existe un anuncio con id ${id}`);
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return jsonError(400, "INVALID_JSON", "El cuerpo debe ser JSON válido");
  }

  const resultado = validarCambioEstado(body);
  if (!resultado.ok) {
    return jsonError(
      400,
      "VALIDATION_ERROR",
      "Estado inválido",
      resultado.details,
    );
  }

  const actualizado = anuncioDb.updateEstado(id, resultado.value.estado);
  return jsonOk(actualizado);
}
