"""Catálogos y datos de ejemplo en memoria (sin base de datos), al estilo del
starter de referencia. Las demás capas leen y mutan estas listas.

Modelo (según docs/designs/diagramaModeloDeDatos-Labclass-PDS.drawio.png):

    rol(id, nombre)
    curso(id, nombre, grado)
    usuario(id, nombre, apellido, correo, rol_id, cursos_ids)
    anuncio(id, titulo, descripcion, tipo, fecha_publicacion, fecha_evento,
            hora_evento, lugar, autor_id, roles_destino_ids, cursos_destino_ids)

`cursos_ids` en un usuario = cursos que el Docente dicta, o cursos en los que el
Padre de familia tiene un hijo (equivale a la tabla UsuarioXCurso del diagrama).
"""

roles = [
    {"id": 1, "nombre": "Administrador"},
    {"id": 2, "nombre": "Docente"},
    {"id": 3, "nombre": "Padre de familia"},
]

cursos = [
    {"id": 1, "nombre": "Quinto A", "grado": "5"},
    {"id": 2, "nombre": "Sexto B", "grado": "6"},
]

usuarios = [
    {"id": 1, "nombre": "Ana", "apellido": "Admin", "correo": "admin@bfa.edu",
     "rol_id": 1, "cursos_ids": []},
    {"id": 2, "nombre": "Diego", "apellido": "Torres", "correo": "diego@bfa.edu",
     "rol_id": 2, "cursos_ids": [1]},
    {"id": 3, "nombre": "Elena", "apellido": "Ruiz", "correo": "elena@bfa.edu",
     "rol_id": 2, "cursos_ids": [2]},
    {"id": 4, "nombre": "Pedro", "apellido": "Perez", "correo": "pedro@bfa.edu",
     "rol_id": 3, "cursos_ids": [1]},
    {"id": 5, "nombre": "Paula", "apellido": "Paz", "correo": "paula@bfa.edu",
     "rol_id": 3, "cursos_ids": [2]},
    {"id": 6, "nombre": "Pablo", "apellido": "Pinto", "correo": "pablo@bfa.edu",
     "rol_id": 3, "cursos_ids": [1, 2]},
]

anuncios = [
    {
        "id": 1,
        "titulo": "Bienvenida al año escolar",
        "descripcion": "Les damos la bienvenida a todos los padres de familia.",
        "tipo": "anuncio",
        "fecha_publicacion": "2026-08-01",
        "fecha_evento": None,
        "hora_evento": None,
        "lugar": None,
        "autor_id": 1,
        "roles_destino_ids": [3],
        "cursos_destino_ids": [],
    },
    {
        "id": 2,
        "titulo": "Salida pedagógica Quinto A",
        "descripcion": "Nos encontramos en la portería a las 7:00 am.",
        "tipo": "evento",
        "fecha_publicacion": "2026-08-20",
        "fecha_evento": "2026-09-05",
        "hora_evento": "07:00",
        "lugar": "Portería principal",
        "autor_id": 2,
        "roles_destino_ids": [],
        "cursos_destino_ids": [1],
    },
]

# Se conserva `mock_data` para la ruta raíz del starter: ahora expone el estado
# del servicio en lugar de datos de demostración.
mock_data = {
    "servicio": "SPCP · Módulo de Publicación de Anuncios",
    "version": "0.1.0",
    "estado": "ok",
}
