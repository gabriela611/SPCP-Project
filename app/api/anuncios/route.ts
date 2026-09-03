import { NextRequest, NextResponse } from "next/server";
import { esVisiblePara } from "./modelo";
import { crearAnuncio, listarAnuncios } from "./store";

function destinatarioDelRequest(request: NextRequest) {
  const { searchParams } = request.nextUrl;
  return {
    rol: searchParams.get("rol") ?? request.headers.get("x-user-rol") ?? undefined,
    grupo: searchParams.get("grupo") ?? request.headers.get("x-user-grupo") ?? undefined,
  };
}

export async function GET(request: NextRequest) {
  const { rol, grupo } = destinatarioDelRequest(request);
  const visibles = listarAnuncios().filter((anuncio) => esVisiblePara(anuncio, rol, grupo));
  return NextResponse.json(visibles);
}

export async function POST(request: NextRequest) {
  const body = await request.json().catch(() => null);
  if (!body || typeof body.titulo !== "string" || typeof body.contenido !== "string") {
    return NextResponse.json({ error: "titulo y contenido son requeridos" }, { status: 400 });
  }

  const rolesDestinatarios = Array.isArray(body.rolesDestinatarios)
    ? body.rolesDestinatarios.filter((rol: unknown) => typeof rol === "string")
    : [];
  const grupoDestinatario =
    typeof body.grupoDestinatario === "string" ? body.grupoDestinatario : undefined;

  if (rolesDestinatarios.length === 0 && !grupoDestinatario) {
    return NextResponse.json(
      { error: "indica rolesDestinatarios o grupoDestinatario" },
      { status: 400 },
    );
  }

  const anuncio = crearAnuncio({
    titulo: body.titulo,
    contenido: body.contenido,
    rolesDestinatarios,
    grupoDestinatario,
  });

  return NextResponse.json(anuncio, { status: 201 });
}
