import type { Anuncio, UsuarioVisibilidad } from "./schema";

/**
 * Un anuncio es visible si el rol o el grupo del usuario coincide
 * con algún valor de rolesDestinatarios.
 */
export function anuncioVisibleParaUsuario(
  anuncio: Anuncio,
  usuario: UsuarioVisibilidad,
): boolean {
  const destinatarios = anuncio.rolesDestinatarios.map((valor) =>
    valor.trim().toLowerCase(),
  );

  const rol = usuario.rol?.trim().toLowerCase();
  const grupo = usuario.grupo?.trim().toLowerCase();

  if (rol && destinatarios.includes(rol)) {
    return true;
  }

  if (grupo && destinatarios.includes(grupo)) {
    return true;
  }

  return false;
}

export function filtrarAnunciosPorVisibilidad(
  anuncios: Anuncio[],
  usuario: UsuarioVisibilidad,
): Anuncio[] {
  return anuncios.filter((anuncio) =>
    anuncioVisibleParaUsuario(anuncio, usuario),
  );
}
