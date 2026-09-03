"""Catálogos y datos de ejemplo en memoria (sin base de datos), al estilo del
starter de referencia. Las demás capas leen y mutan estas listas.

Modelo (según docs/designs/diagramaModeloDeDatos-Labclass-PDS.drawio.png y la
sección Roles del SOW):

    rol(id, nombre)
    usuario(id, nombre, apellido, correo, contrasena, rol_id, cursos_ids)
    permisos_por_rol: matriz de funcionalidades habilitadas por nombre de rol
    sesiones: sesiones activas creadas al autenticar

`contrasena` en texto plano es una simplificación de laboratorio.
"""

roles = [
    {"id": 1, "nombre": "Administrador"},
    {"id": 2, "nombre": "Docente"},
    {"id": 3, "nombre": "Padre de familia"},
]

usuarios = [
    {"id": 1, "nombre": "Ana", "apellido": "Admin", "correo": "admin@bfa.edu",
     "contrasena": "admin123", "rol_id": 1, "cursos_ids": []},
    {"id": 2, "nombre": "Diego", "apellido": "Torres", "correo": "diego@bfa.edu",
     "contrasena": "diego123", "rol_id": 2, "cursos_ids": [1]},
    {"id": 3, "nombre": "Elena", "apellido": "Ruiz", "correo": "elena@bfa.edu",
     "contrasena": "elena123", "rol_id": 2, "cursos_ids": [2]},
    {"id": 4, "nombre": "Pedro", "apellido": "Perez", "correo": "pedro@bfa.edu",
     "contrasena": "pedro123", "rol_id": 3, "cursos_ids": [1]},
    {"id": 5, "nombre": "Paula", "apellido": "Paz", "correo": "paula@bfa.edu",
     "contrasena": "paula123", "rol_id": 3, "cursos_ids": [2]},
]

# Matriz de control de acceso por rol (SOW · sección Roles).
permisos_por_rol = {
    "Administrador": [
        "anuncios.crear", "anuncios.ver", "eventos.crear", "eventos.ver",
        "mensajes.estado.ver", "roles.gestionar", "portal.supervisar",
    ],
    "Docente": [
        "anuncios.crear", "anuncios.ver", "eventos.crear", "eventos.ver",
        "mensajes.estado.ver", "lectura.confirmar",
    ],
    "Padre de familia": [
        "anuncios.ver", "eventos.ver", "lectura.confirmar",
    ],
}

# Sesiones activas; las crea POST /sesiones (append). No hay persistencia.
sesiones = []

# Se conserva `mock_data` para la ruta raíz del starter: expone el estado
# del servicio.
mock_data = {
    "servicio": "SPCP · Autenticación y gestión de roles",
    "version": "0.1.0",
    "estado": "ok",
}
