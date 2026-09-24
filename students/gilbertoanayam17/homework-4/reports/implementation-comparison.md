# Implementation Comparison: JavaScript vs Python

Las dos suites cubren los mismos 28 casos con los mismos IDs de diseño. Estas son
las diferencias que salieron al portar una a la otra.

## Differences

| Tema                    | JavaScript (Jest)                          | Python (pytest)                                |
| ----------------------- | ------------------------------------------ | ---------------------------------------------- |
| Comparar montos         | `expect(x).toBeCloseTo(y, 2)`              | `assert x == pytest.approx(y)`                 |
| Redondeo                | `Math.round(v * 100) / 100`                | `round(v, 2)`                                  |
| Tabla de reglas         | `Map` con `.get()` / `.has()`              | `dict` con `in` y `[]`                         |
| Validar que sea número  | `typeof v !== "number"`                    | `isinstance(v, (int, float))` + excluir `bool` |
| Errores de construcción | `throw new Error()` / `.toThrow()`         | `raise ValueError()` / `pytest.raises()`       |
| Datos de prueba         | Se construye la cuenta dentro de cada test | Fixture `make_account` en `conftest.py`        |
| Nombres en el resultado | camelCase (`dailyTransferTotal`)           | snake_case (`daily_transfer_total`)            |
| Cobertura que reporta   | Líneas, ramas y funciones                  | Solo líneas                                    |

## Las dos que sí cambian el comportamiento

El redondeo no es igual. `Math.round` en JavaScript redondea los empates hacia
arriba, pero `round()` en Python usa redondeo bancario, que va al par más cercano.
Por eso `round(0.125, 2)` da `0.12` en Python mientras que
`Math.round(0.125 * 100) / 100` da `0.13` en JavaScript. En esta tarea no afecta,
porque ninguno de los montos que uso cae en un empate exacto de medio centavo,
pero si el sistema manejara montos con tres decimales los dos lenguajes darían
saldos distintos.

Los booleanos son números en Python. `isinstance(True, int)` devuelve `True`,
así que `transfer(True)` habría pasado la validación de tipo y se habría tratado
como transferir $1. Tuve que excluir `bool` a mano en `is_number()`. En JavaScript
no hace falta, porque `typeof true` es `"boolean"` y no `"number"`.

## Coverage

Ambas implementaciones superan el 80 % que pide el bonus: JavaScript 84.8 % de
líneas (79.8 % de ramas) y Python 87.7 % de líneas. La diferencia sale de que
Jest cuenta como línea algunas cosas que `coverage.py` no, como los parámetros
por defecto.
