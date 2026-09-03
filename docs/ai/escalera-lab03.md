# Escalera - Laboratorio 03

Módulo evaluado: **Publicación de Anuncios** del portal SPCP (Bright Future
Academy). Se pidió el mismo endpoint en cuatro versiones de creciente
especificidad y se calificó cada resultado contra la misma lista de 8 criterios
de verificación (cumple / no cumple, sin puntos intermedios). Las alucinaciones
—dependencias, campos, endpoints o archivos que nadie pidió— se cuentan aparte.

### Prompt 1

Necesito un API de anuncios para el portal del colegio. Que se puedan crear y
consultar.

### Prompt 2

El SPCP es el portal de comunicación de Bright Future Academy y el módulo que
toca ahora es el de anuncios. Implementa su endpoint en FastAPI dentro de `src/`,
con datos de ejemplo en memoria (sin base de datos) tomados del
`statement_of_work.md` y de los diagramas de `docs/`. Organiza el código en capas
(rutas, lógica y datos por separado) y aplica buenas prácticas.

### Prompt 3

El SPCP es el portal de comunicación de Bright Future Academy y el módulo que
toca ahora es el de anuncios. Implementa su endpoint en FastAPI dentro de `src/`,
con datos de ejemplo en memoria (sin base de datos) tomados del
`statement_of_work.md` y de los diagramas de `docs/`. Organiza el código en capas
(rutas, lógica y datos por separado) y aplica buenas prácticas.

Trátalo como una tarea con Definition of Done. El resultado debe cumplir:

- Un Administrador o un Docente puede crear un anuncio; un Padre de familia no.
- Cada anuncio se dirige a uno o más roles y/o cursos; si no tiene ningún
  destinatario, se rechaza.
- Un Docente solo puede dirigir anuncios a los cursos que dicta y no puede
  segmentar por rol.
- Al listar, un usuario solo ve los anuncios cuyo destinatario coincide con su
  rol o con alguno de sus cursos (además de los que él creó, y de todos si es
  Administrador).
- `titulo` y `descripcion` son obligatorios y se validan antes de procesar; la
  entrada inválida responde con un error estructurado y el código HTTP correcto.
- Incluye pruebas automatizadas, al menos una que compruebe la visibilidad por
  rol/curso.

No implementes autenticación real ni notificaciones por correo: eso pertenece a
otros módulos. Nombra el dominio en español y sigue PEP 8.

### Prompt 4

El SPCP es el portal de comunicación de Bright Future Academy y el módulo que
toca ahora es el de anuncios. Implementa su endpoint en FastAPI dentro de `src/`,
con datos de ejemplo en memoria (sin base de datos) tomados del
`statement_of_work.md` y de los diagramas de `docs/`. Organiza el código en capas
(rutas, lógica y datos por separado) y aplica buenas prácticas.

Trátalo como una tarea con Definition of Done. El resultado debe cumplir:

- Un Administrador o un Docente puede crear un anuncio; un Padre de familia no.
- Cada anuncio se dirige a uno o más roles y/o cursos; si no tiene ningún
  destinatario, se rechaza.
- Un Docente solo puede dirigir anuncios a los cursos que dicta y no puede
  segmentar por rol.
- Al listar, un usuario solo ve los anuncios cuyo destinatario coincide con su
  rol o con alguno de sus cursos (además de los que él creó, y de todos si es
  Administrador).
- `titulo` y `descripcion` son obligatorios y se validan antes de procesar; la
  entrada inválida responde con un error estructurado y el código HTTP correcto.
- Incluye pruebas automatizadas, al menos una que compruebe la visibilidad por
  rol/curso.

No implementes autenticación real ni notificaciones por correo: eso pertenece a
otros módulos. Nombra el dominio en español y sigue PEP 8.

Antes de escribir código, lee `AGENTS.md` y respeta al pie sus convenciones:
estructura de carpetas, forma de las rutas, `usuario_id` como identificación del
solicitante y formato de respuesta. Adapta el starter que ya vive en `src/`
(`src/main.py`, `src/data/mock_data.py`, `src/services/`) en lugar de crear una
estructura nueva, y declara toda dependencia en `src/requirements.txt`. No
agregues endpoints, campos ni archivos que no estén en `AGENTS.md` o en los
criterios de arriba.

## Calificaciones

| Prompt | Calificación |
|--------|--------------|
| Prompt 1 | 2/8 |
| Prompt 2 | 5/8 |
| Prompt 3 | 7/8 |
| Prompt 4 | 8/8 |

## Alucinaciones

| Prompt | Alucinaciones |
|--------|---------------|
| Prompt 1 | 6 |
| Prompt 2 | 4 |
| Prompt 3 | 2 |
| Prompt 4 | 0 |

## Conclusión

Los resultados muestran una correlación directa entre la especificidad del prompt
y la calidad del código generado, pero también revelan *qué tipo* de contexto
mueve la aguja en cada salto. El Prompt 1, con una orden tan abierta como
"necesito un API de anuncios… que se puedan crear y consultar", dejó al modelo
sin stack, sin estructura de proyecto y sin la regla de negocio, lo que se
tradujo en la peor calificación (2/8) y el mayor número de alucinaciones (6): al
no tener nada a qué anclarse, el modelo inventó esquema de datos,
capas, endpoints y hasta una base de datos completa. El Prompt 2 subió a 5/8 al
fijar el stack (FastAPI), la ubicación (`src/`), el origen de los datos mock
(`statement_of_work.md` y los diagramas) y la exigencia de separar en capas; eso
bastó para que el resultado respetara la estructura y el formato del código ya
existente, pero sin criterios de aceptación el endpoint siguió siendo un CRUD
genérico, sin la regla de visibilidad y sin pruebas que la ejercitaran.

El salto decisivo ocurre entre el Prompt 2 y el Prompt 3: al reformular la
petición como una Definition of Done —criterios de aceptación verificables uno a
uno, más una lista de *no-goals* (nada de autenticación ni de correo)— la
calificación llegó a 7/8 y las alucinaciones bajaron a 2. Con los criterios
escritos, el modelo por fin implementó la regla del RFP —un anuncio solo es
visible para sus roles o cursos destinatarios— y agregó una prueba que la
verifica más allá del caso feliz; los *no-goals* recortaron casi todo lo que
antes inventaba. El único criterio que siguió fallando fue el de la convención
REST del equipo: sin un artefacto que la declarara, la forma de las rutas seguía
siendo una decisión del modelo. Ese hueco se cerró en el Prompt 4, que alcanzó el
máximo (8/8) con 0 alucinaciones al obligar a leer `AGENTS.md` y a adaptar el starter ya presente en `src/` en
vez de generar una arquitectura propia. En conjunto, el experimento confirma que
la ingeniería de prompts efectiva combina tres elementos —contexto de negocio con
límites claros, criterios de aceptación verificables, y anclaje al código y la
especificación que ya existen en el repositorio— y que cada uno resuelve una
clase distinta de error: los límites y los criterios eliminan las suposiciones de
negocio, mientras que el anclaje a artefactos reales elimina las suposiciones de
arquitectura y convenciones.
