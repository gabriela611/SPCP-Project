# Plantilla de prompt: Pedir código

Usa esta plantilla cuando necesites que la IA genere una nueva funcionalidad,
módulo, función o script.

## Plantilla

```
Contexto del proyecto:
- Lenguaje / framework: <ej. Python 3.11, Flask>
- Estructura relevante: <archivos o carpetas donde debe encajar el código>
- Convenciones a respetar: <estilo, nombres, librerías permitidas>

Objetivo:
- Quiero que implementes <descripción concreta de la funcionalidad>.

Entrada y salida esperada:
- Entrada: <parámetros, tipos, formato>
- Salida: <valor de retorno, formato, efectos secundarios>

Requisitos:
1. <requisito funcional 1>
2. <requisito funcional 2>
3. <restricciones: rendimiento, seguridad, compatibilidad>

Casos borde a considerar:
- <caso 1>
- <caso 2>

Formato de la respuesta:
- Solo el código necesario, en <archivo/función> indicado.
- Incluye comentarios breves solo donde el porqué no sea obvio.
- No agregues dependencias nuevas sin avisar.
```

## Ejemplo rápido

```
Contexto del proyecto:
- Lenguaje: Python 3.11, sin frameworks
- Estructura: el código va en src/utils/fechas.py

Objetivo:
- Implementa una función que calcule los días hábiles entre dos fechas.

Entrada y salida esperada:
- Entrada: fecha_inicio y fecha_fin como datetime.date
- Salida: int con la cantidad de días hábiles (lunes a viernes), sin contar la fecha inicial

Requisitos:
1. Lanza ValueError si fecha_fin < fecha_inicio.
2. No uses librerías externas.

Casos borde a considerar:
- Mismo día de inicio y fin
- Rango que empieza o termina en fin de semana

Formato de la respuesta:
- Solo la función con su docstring.
```

## Buenas prácticas

- Da contexto antes de la petición: lenguaje, versión y dónde va el código.
- Separa "qué quiero" de "cómo debe comportarse" (requisitos y casos borde).
- Pide un formato de salida concreto para evitar respuestas largas de más.
- Si el resultado no convence, itera indicando qué parte cambiar, no repitas todo.
