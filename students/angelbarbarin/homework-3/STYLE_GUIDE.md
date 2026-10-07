# Guia de estilo — cotizador de camaras de reversa

Bonus de la tarea 3. Define las convenciones que las herramientas configuradas
hacen cumplir de forma automatica, y las que dependen del criterio de quien
escribe el codigo.

## Lo que la herramienta decide (no se discute en revision)

| Aspecto | Regla | Quien la aplica |
|---|---|---|
| Formato (indentacion, comillas, saltos) | Estilo `black`, sin excepciones | `black` |
| Orden de imports | stdlib, terceros, locales; alfabetico | `isort --profile=black` |
| Longitud de linea | 100 caracteres | `black` + `.pylintrc` |
| Espacios al final de linea | No se permiten | hook `trailing-whitespace` |
| Salto de linea final | Obligatorio | hook `end-of-file-fixer` |

Discutir formato en una revision de codigo es tiempo perdido: si `black` lo
acepta, esta bien. Esa es justamente la razon de adoptar un formateador con
opinion propia y sin configuracion.

## Nomenclatura

- `snake_case` para funciones, metodos, variables y argumentos.
- `PascalCase` para clases.
- `UPPER_CASE` para constantes de modulo.
- Nombres en espanol sin acentos, consistentes con el vocabulario del negocio:
  `cotizar`, `carrito`, `sku`, `instalacion`. El dominio se nombra como lo
  nombra el cliente, no traducido a medias.
- Prefijo `_` para lo que es privado del modulo.

## Docstrings

- Obligatorios en todo modulo, clase y funcion publica (`no-docstring-rgx=^_`).
- Una linea si la funcion cabe en una idea; parrafo adicional solo cuando hay
  una **decision** que explicar.
- El docstring dice **que** hace y **que garantiza**, no como lo hace.

## Comentarios

Un comentario que repite lo que dice la linea de abajo es ruido que hay que
mantener. Los comentarios de este proyecto explican una de tres cosas:

1. Por que se eligio una alternativa sobre otra.
2. De que condicion depende esa decision (para saber cuando deja de valer).
3. Un caso limite que no es evidente leyendo el codigo.

Ejemplo real de este proyecto, en `agregar_item`:

```python
# Sin carrito explicito se crea uno nuevo en cada llamada: usar una lista
# como valor por defecto haria que todas las cotizaciones compartieran el
# mismo carrito.
```

## Manejo de errores

- Las entradas invalidas lanzan `ValueError` con un mensaje que **nombra el
  valor recibido**. Un error sin el dato que lo causo obliga a depurar algo que
  el programa ya sabia.
- Nunca `except:` a secas. Se capturan tipos concretos.
- Nunca valores centinela (`-1`, `None`, `NaN`) para senalar un fallo cuando el
  llamador podria confundirlos con un resultado valido.

## Validacion

La validacion vive en el constructor o en la entrada de la funcion, no en los
metodos de calculo. Si un objeto existe, es valido; ningun metodo posterior
debe volver a desconfiar de el.

## Pruebas

- Un `assert` por comportamiento, no uno por linea de codigo.
- Nombres de prueba que describan el caso, no el metodo:
  `test_carrito_no_se_comparte_entre_cotizaciones`, no `test_agregar_item_2`.
- Toda correccion de un defecto entra acompanada de la prueba de regresion que
  habria fallado antes.
- Los flotantes se comparan con `pytest.approx`, nunca con `==`.
