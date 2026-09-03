import { Anuncio, EstadoAnuncio } from "./modelo";

const anuncios: Anuncio[] = [];

export function crearAnuncio(
  datos: Omit<Anuncio, "id" | "fechaCreacion" | "estado"> & { estado?: EstadoAnuncio },
): Anuncio {
  const anuncio: Anuncio = {
    id: crypto.randomUUID(),
    titulo: datos.titulo,
    contenido: datos.contenido,
    rolesDestinatarios: datos.rolesDestinatarios,
    grupoDestinatario: datos.grupoDestinatario,
    estado: datos.estado ?? "publicado",
    fechaCreacion: new Date().toISOString(),
  };
  anuncios.push(anuncio);
  return anuncio;
}

export function listarAnuncios(): Anuncio[] {
  return anuncios;
}

export function actualizarEstado(id: string, estado: EstadoAnuncio): Anuncio | null {
  const anuncio = anuncios.find((item) => item.id === id);
  if (!anuncio) return null;
  anuncio.estado = estado;
  return anuncio;
}
