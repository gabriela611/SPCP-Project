import { ESTADOS_ANUNCIO, type EstadoAnuncio } from "./schema";

export type ResultadoValidacion<T> =
  | { ok: true; value: T }
  | { ok: false; details: Record<string, string> };

function esStringNoVacio(valor: unknown): valor is string {
  return typeof valor === "string" && valor.trim().length > 0;
}

export function validarCreacionAnuncio(body: unknown): ResultadoValidacion<{
  titulo: string;
  contenido: string;
  rolesDestinatarios: string[];
  estado: EstadoAnuncio;
}> {
  const details: Record<string, string> = {};
  const payload =
    body && typeof body === "object" ? (body as Record<string, unknown>) : {};

  if (!esStringNoVacio(payload.titulo)) {
    details.titulo = "El título es obligatorio";
  }

  if (!esStringNoVacio(payload.contenido)) {
    details.contenido = "El contenido es obligatorio";
  }

  const roles = payload.rolesDestinatarios;
  const rolesValidos =
    Array.isArray(roles) &&
    roles.length > 0 &&
    roles.every((rol) => esStringNoVacio(rol));

  if (!rolesValidos) {
    details.rolesDestinatarios =
      "rolesDestinatarios debe ser un arreglo no vacío de textos";
  }

  let estado: EstadoAnuncio = "borrador";
  if (payload.estado !== undefined) {
    if (
      typeof payload.estado !== "string" ||
      !ESTADOS_ANUNCIO.includes(payload.estado as EstadoAnuncio)
    ) {
      details.estado = `estado debe ser uno de: ${ESTADOS_ANUNCIO.join(", ")}`;
    } else {
      estado = payload.estado as EstadoAnuncio;
    }
  }

  if (Object.keys(details).length > 0) {
    return { ok: false, details };
  }

  return {
    ok: true,
    value: {
      titulo: String(payload.titulo).trim(),
      contenido: String(payload.contenido).trim(),
      rolesDestinatarios: (roles as string[]).map((rol) => rol.trim()),
      estado,
    },
  };
}

export function validarCambioEstado(body: unknown): ResultadoValidacion<{
  estado: EstadoAnuncio;
}> {
  const payload =
    body && typeof body === "object" ? (body as Record<string, unknown>) : {};

  if (
    typeof payload.estado !== "string" ||
    !ESTADOS_ANUNCIO.includes(payload.estado as EstadoAnuncio)
  ) {
    return {
      ok: false,
      details: {
        estado: `estado debe ser uno de: ${ESTADOS_ANUNCIO.join(", ")}`,
      },
    };
  }

  return { ok: true, value: { estado: payload.estado as EstadoAnuncio } };
}
