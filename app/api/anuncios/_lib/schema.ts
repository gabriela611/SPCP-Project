export const ESTADOS_ANUNCIO = ["borrador", "publicado", "archivado"] as const;

export type EstadoAnuncio = (typeof ESTADOS_ANUNCIO)[number];

/**
 * Modelo Anuncio (Bright Future).
 * `rolesDestinatarios` contiene roles y/o identificadores de grupo
 * (p. ej. "padre", "docente", "5A"). Un usuario ve el anuncio si su rol
 * o su grupo aparece en ese arreglo.
 */
export type Anuncio = {
  id: string;
  titulo: string;
  contenido: string;
  rolesDestinatarios: string[];
  estado: EstadoAnuncio;
  fechaCreacion: string;
};

export type UsuarioVisibilidad = {
  rol?: string;
  grupo?: string;
};

export type ApiErrorBody = {
  code: string;
  message: string;
  details?: unknown;
};

export type ApiResponse<T> = {
  data: T | null;
  error: ApiErrorBody | null;
};
