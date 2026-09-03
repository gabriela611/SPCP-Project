import { NextRequest, NextResponse } from "next/server";
import { esEstadoAnuncio } from "../modelo";
import { actualizarEstado } from "../store";

export async function PATCH(
  request: NextRequest,
  context: { params: Promise<{ id: string }> },
) {
  const { id } = await context.params;
  const body = await request.json().catch(() => null);
  if (!body || !esEstadoAnuncio(body.estado)) {
    return NextResponse.json({ error: "estado debe ser publicado o archivado" }, { status: 400 });
  }

  const anuncio = actualizarEstado(id, body.estado);
  if (!anuncio) {
    return NextResponse.json({ error: "anuncio no encontrado" }, { status: 404 });
  }

  return NextResponse.json(anuncio);
}
