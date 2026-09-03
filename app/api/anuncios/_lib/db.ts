import { randomUUID } from "node:crypto";
import type { Anuncio, EstadoAnuncio } from "./schema";

/**
 * Cliente de datos en memoria para Anuncio.
 * El repositorio no traía ORM configurado; este módulo es el cliente
 * que usan las rutas de /api/anuncios.
 */
const anuncios: Anuncio[] = [];

export const anuncioDb = {
  reset(seed: Anuncio[] = []) {
    anuncios.splice(0, anuncios.length, ...seed);
  },

  list(): Anuncio[] {
    return [...anuncios];
  },

  findById(id: string): Anuncio | undefined {
    return anuncios.find((item) => item.id === id);
  },

  create(input: {
    titulo: string;
    contenido: string;
    rolesDestinatarios: string[];
    estado: EstadoAnuncio;
  }): Anuncio {
    const anuncio: Anuncio = {
      id: randomUUID(),
      titulo: input.titulo,
      contenido: input.contenido,
      rolesDestinatarios: input.rolesDestinatarios,
      estado: input.estado,
      fechaCreacion: new Date().toISOString(),
    };
    anuncios.push(anuncio);
    return anuncio;
  },

  updateEstado(id: string, estado: EstadoAnuncio): Anuncio | undefined {
    const actual = anuncios.find((item) => item.id === id);
    if (!actual) {
      return undefined;
    }
    actual.estado = estado;
    return { ...actual };
  },
};
