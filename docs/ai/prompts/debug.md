# Plantilla de prompt: Debug

Usa esta plantilla cuando tengas un error, un comportamiento inesperado o una
prueba que falla y necesites ayuda para diagnosticarlo.

## Plantilla

~~~
Contexto:
- Lenguaje / framework y versión: <ej. Node.js 20, Express 4>
- Qué estaba haciendo cuando falló: <acción o comando>

Comportamiento esperado:
- <lo que debería pasar>

Comportamiento actual:
- <lo que pasa en su lugar>

Mensaje de error / stack trace:
  <pega aquí el error completo, sin recortar>

Código relevante:
  <pega la función o el bloque implicado>

Qué ya intenté:
- <intento 1 y resultado>
- <intento 2 y resultado>

Lo que necesito:
- Identifica la causa raíz y explícala brevemente.
- Propón la corrección mínima.
- Indica cómo verificar que quedó resuelto.
~~~

## Ejemplo rápido

~~~
Contexto:
- Python 3.11, pytest
- Ejecuté: pytest tests/test_carrito.py

Comportamiento esperado:
- test_total_con_descuento pasa con total = 90.0

Comportamiento actual:
- Falla con total = 100.0

Mensaje de error:
  AssertionError: assert 100.0 == 90.0

Código relevante:
  def aplicar_descuento(total, porcentaje):
      return total - porcentaje

Qué ya intenté:
- Revisé que el test pasa porcentaje=10; parece correcto.

Lo que necesito:
- Causa raíz y corrección mínima.
~~~

## Buenas prácticas

- Pega el error completo, no un fragmento; el stack trace suele señalar la línea.
- Muestra el código que sospechas, pero también dónde se llama.
- Di qué ya probaste para no recibir sugerencias que ya descartaste.
- Pide primero la causa, luego la solución: entender el porqué evita repetir el bug.
