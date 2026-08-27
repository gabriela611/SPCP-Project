# Plantilla de prompt: Documentar código

Usa esta plantilla cuando necesites docstrings, comentarios, un README o una
explicación de un fragmento de código existente.

## Plantilla

~~~
Contexto:
- Lenguaje / framework: <ej. Java 17>
- Audiencia de la documentación: <ej. otros desarrolladores del equipo, usuarios finales>
- Estándar o estilo a seguir: <ej. Javadoc, docstrings estilo Google, Markdown>

Código a documentar:
  <pega aquí el código>

Qué necesito:
- <docstring por función | comentarios en línea | README | explicación paso a paso>

Requisitos:
1. Describe propósito, parámetros, valor de retorno y excepciones.
2. No cambies la lógica del código, solo documenta.
3. Comentarios en línea únicamente donde el porqué no sea evidente.
4. Idioma: <español | inglés>.

Formato de la respuesta:
- Devuelve el código con la documentación integrada.
- Si hay un README, entrégalo en Markdown aparte.
~~~

## Ejemplo rápido

~~~
Contexto:
- Python 3.11
- Audiencia: desarrolladores del equipo
- Estilo: docstrings estilo Google, en español

Código a documentar:
  def normalizar(texto):
      return " ".join(texto.lower().split())

Qué necesito:
- Docstring para la función.

Requisitos:
1. Indica propósito, parámetro y valor de retorno.
2. No cambies la lógica.

Formato de la respuesta:
- La función con el docstring integrado.
~~~

## Buenas prácticas

- Indica el estándar de documentación esperado (Javadoc, Google, NumPy, JSDoc...).
- Aclara la audiencia: no se documenta igual para un usuario que para el equipo.
- Pide explícitamente que no se altere la lógica al documentar.
- Para código complejo, pide primero una explicación en prosa y luego los comentarios.
