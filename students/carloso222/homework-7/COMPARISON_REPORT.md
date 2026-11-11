# Reporte de comparación: pruebas tradicionales vs. basadas en datos

Se escribieron los mismos 10 escenarios de `Order` de dos maneras:

- `tests/test_order_traditional.py`: 10 funciones sin parametrización, datos escritos en el código.
- `tests/test_order_data_driven.py`: una prueba parametrizada que carga los 10 escenarios desde
  `test_data/order_calculations.csv` (a través de `tests/data_loader.py`).

Ambas versiones pasan (`20 passed`).

## 1. Líneas de código (medidas)

Se contaron las líneas no vacías (ninguno de los archivos tiene comentarios de línea completa) con:

```bash
grep -cv '^[[:space:]]*$' tests/test_order_traditional.py   # 79
grep -cv '^[[:space:]]*$' tests/test_order_data_driven.py   # 19
grep -cv '^[[:space:]]*$' tests/data_loader.py              # 42
```

Después de aplicar `black --line-length 120` (que expande los diccionarios largos de las aserciones).

| Enfoque                                 | LOC    | Detalle                            |
| --------------------------------------- | ------ | ---------------------------------- |
| Tradicional                             | **79** | 10 pruebas, ~7.9 líneas por prueba |
| Data-driven (solo el archivo de prueba) | **19** | 1 prueba + lista de 10 nombres     |
| Data-driven + cargador compartido       | 61     | 19 + 42 de `data_loader.py`        |
| Data-driven + cargador + 10 filas CSV   | 71     | + 10 filas de datos                |

Reducción: **75.9 %** solo contando el archivo de prueba ((79 - 19) / 79); **22.8 %** si se suma
el cargador; **10.1 %** si además se cuentan las 10 filas del CSV. Con solo 10 escenarios la ganancia
real es modesta porque el cargador se amortiza poco. Pero ese cargador lo usan también
`test_order_calculator.py` (33 casos), `test_customer_validator.py` (37) y `test_order_generator.py` (100):
con 170 filas de datos, el código de prueba no crece.

## 2. Mantenibilidad

- **Agregar un caso**: tradicional = copiar una función de ~8 líneas y editar valores (se arriesga
  a olvidar cambiar un nombre o un valor). Data-driven = agregar 1 fila al CSV, sin tocar código.
- **Actualizar una regla** (p. ej. cambiar el impuesto): en ambos casos hay que recalcular los esperados, pero en
  data-driven todos están juntos en una tabla; en el tradicional están repartidos por 10 funciones. Si
  cambia la _forma_ de la verificación (p. ej. tolerancia), data-driven edita 1 sitio; tradicional, 10.
- **Quién puede contribuir**: alguien sin conocimientos de Python puede añadir filas al CSV.
- **Riesgo propio de data-driven**: datos mal formados. Se mitiga con el validador de datos (bonus C),
  que reporta `archivo:línea` antes de correr las pruebas.

## 3. Legibilidad

- El tradicional es más fácil de leer de forma aislada: cada prueba cuenta su historia
  (Arrange-Act-Assert) con un nombre que describe condición y resultado.
- El data-driven es más fácil de **revisar en conjunto**: la tabla muestra de un vistazo qué entradas
  y límites están cubiertos y cuáles faltan. Cada fila aparece en pytest con su `test_name` como id,
  p. ej. `test_order_scenario_from_csv_returns_expected_breakdown[shipping_freeship_code]`.
- Organización: en data-driven la lógica (1 función) y los datos (tabla) están separados;
  en el tradicional se mezclan en cada función.
- Contra: un JSON dentro de una celda CSV (`items`) es incómodo de leer y de editar a mano.

## 4. Cobertura y esfuerzo

- Escenarios: ambas versiones cubren los mismos 10 escenarios. El CSV completo cubre 33 y el
  generador añade 100 más con la misma función de prueba.
- Cobertura de código de `src/`: **99 %** con la suite completa (268 pruebas). Las 10 pruebas
  tradicionales y las 10 data-driven cubren las mismas ramas, así que la diferencia no está en la
  cobertura de líneas sino en cuántos casos se pueden añadir.
- Tiempo para añadir 10 casos más: tradicional ~ +79 líneas de código a escribir y revisar;
  data-driven = +10 líneas de CSV, 0 de código (la mayor parte del tiempo se va en calcular a mano los
  valores esperados, que es igual en ambos).
- Tiempo de ejecución: indistinguible a esta escala (`pytest` informa 0.24 s para las 20 pruebas de ambos
  archivos; la mayor parte es el arranque de pytest).

## 5. Conclusión

**Usar pruebas data-driven** cuando se prueba la misma lógica con muchas combinaciones de entrada/salida
(cálculos, validadores, reglas de negocio, tablas de decisión), cuando los datos pueden crecer o los aportan
personas no programadoras.

**Usar pruebas tradicionales** para escenarios únicos con preparación distinta (mocks, flujos con estado,
secuencias de pasos), cuando se quiere que cada prueba sea autoexplicativa, o cuando hay pocos casos.

|             | Ventajas                                                                                                                                                 | Desventajas                                                                                                                                                                                                                    |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Data-driven | Menos código repetido; agregar casos es barato; datos visibles y revisables; fácil de escalar (33 -> 133 casos sin tocar código); separa datos de lógica | Cargador y validación de datos extra; los fallos apuntan a una fila, no a una función con nombre propio; errores en los datos pueden dar falsos positivos/negativos; difícil expresar casos con lógica de preparación distinta |
| Tradicional | Simple, explícito, sin infraestructura; cada prueba es independiente y legible                                                                           | Mucha repetición; cada caso nuevo cuesta ~8 líneas; cambios transversales se repiten N veces                                                                                                                                   |

En esta tarea las dos aproximaciones se combinan: casos con datos para calculadora y validador,
y pruebas tradicionales para los casos de error (`ValueError`) y la lógica del flujo, que no encajan en una tabla.
