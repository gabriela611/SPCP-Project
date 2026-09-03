export const ESTADOS_ANUNCIO = ["publicado", "archivado"] as const;
export type EstadoAnuncio = (typeof ESTADOS_ANUNCIO)[number];

export type Anuncio = {
  id: string;
  titulo: string;
  contenido: string;
  rolesDestinatarios: string[];
  grupoDestinatario?: string;
  estado: EstadoAnuncio;
  fechaCreacion: string;
};

export function esEstadoAnuncio(valor: unknown): valor is EstadoAnuncio {
  return typeof valor === "string" && ESTADOS_ANUNCIO.includes(valor as EstadoAnuncio);
}

export function esVisiblePara(
  anuncio: Anuncio,
  rol?: string,
  grupo?: string,
): boolean {
  const porRol =
    Boolean(rol) && anuncio.rolesDestinatarios.includes(rol as string);
  const porGrupo =
    Boolean(grupo) && Boolean(anuncio.grupoDestinatario) && anuncio.grupoDestinatario === grupo;
  return porRol || porGrupo;
}
