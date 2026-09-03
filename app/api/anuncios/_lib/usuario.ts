import type { UsuarioVisibilidad } from "./schema";

export function usuarioDesdeHeaders(headers: Headers): UsuarioVisibilidad {
  const rol = headers.get("x-user-role") ?? undefined;
  const grupo = headers.get("x-user-grupo") ?? undefined;
  return {
    rol: rol?.trim() || undefined,
    grupo: grupo?.trim() || undefined,
  };
}

export function tieneIdentidad(usuario: UsuarioVisibilidad): boolean {
  return Boolean(usuario.rol || usuario.grupo);
}
