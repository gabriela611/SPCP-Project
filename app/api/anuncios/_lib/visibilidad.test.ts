import assert from "node:assert/strict";
import { describe, it } from "node:test";
import type { Anuncio } from "./schema";
import { filtrarAnunciosPorVisibilidad } from "./visibilidad";

function anuncio(parcial: Partial<Anuncio> & Pick<Anuncio, "rolesDestinatarios">): Anuncio {
  return {
    id: parcial.id ?? "a1",
    titulo: parcial.titulo ?? "Reunión de padres",
    contenido: parcial.contenido ?? "Martes 8:00",
    rolesDestinatarios: parcial.rolesDestinatarios,
    estado: parcial.estado ?? "publicado",
    fechaCreacion: parcial.fechaCreacion ?? "2026-09-02T00:00:00.000Z",
  };
}

describe("filtro de visibilidad de anuncios", () => {
  const dirigidoAPadres = anuncio({
    id: "padres",
    rolesDestinatarios: ["padre"],
  });
  const dirigidoADocentesY5A = anuncio({
    id: "mixto",
    rolesDestinatarios: ["docente", "5A"],
  });

  it("un usuario cuyo rol no está en destinatarios no ve el anuncio", () => {
    const visibles = filtrarAnunciosPorVisibilidad(
      [dirigidoAPadres],
      { rol: "docente" },
    );

    assert.deepEqual(visibles, []);
  });

  it("un usuario con rol destinatario sí ve el anuncio", () => {
    const visibles = filtrarAnunciosPorVisibilidad(
      [dirigidoAPadres],
      { rol: "padre" },
    );

    assert.equal(visibles.length, 1);
    assert.equal(visibles[0]?.id, "padres");
  });

  it("un usuario cuyo grupo no coincide no ve el anuncio", () => {
    const visibles = filtrarAnunciosPorVisibilidad(
      [dirigidoADocentesY5A],
      { rol: "padre", grupo: "3B" },
    );

    assert.deepEqual(visibles, []);
  });

  it("un usuario ve el anuncio si su grupo coincide aunque su rol no", () => {
    const visibles = filtrarAnunciosPorVisibilidad(
      [dirigidoADocentesY5A],
      { rol: "padre", grupo: "5A" },
    );

    assert.equal(visibles.length, 1);
    assert.equal(visibles[0]?.id, "mixto");
  });
});
