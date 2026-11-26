# Comparison Report: Traditional vs Data-Driven Testing

Los mismos 10 escenarios de calculo de ordenes se implementaron de dos formas:
`tests/test_order_traditional.py` (datos hardcodeados, sin parametrizar) y
`tests/test_order_data_driven.py` (datos cargados desde `test_data/order_calculations.csv`).

## 1. Lines of Code

LOC medidas con `scripts/count_loc.py` (sin lineas vacias ni comentarios).

| Approach | File(s) | LOC |
|---|---|---|
| Traditional | test_order_traditional.py | 60 |
| Data-driven (solo test) | test_order_data_driven.py | 14 |
| Data-driven (test + loader) | test_order_data_driven.py + data_loader.py | 59 |

- Reduccion solo del archivo de test: (60 - 14) / 60 = **76.67%**.
- Reduccion incluyendo el loader: (60 - 59) / 60 = **1.67%**.
- El loader (45 LOC) es un costo fijo que se paga una sola vez: lo comparten
  `test_order_calculator.py`, `test_customer_validator.py`, `test_integration.py`
  y `test_generated_orders.py`. Para un unico archivo de 10 tests casi no hay ahorro;
  el beneficio aparece al reutilizarlo en mas archivos y al crecer el numero de casos.
- El archivo data-driven incluye 1 test adicional (`test_all_ten_scenarios_loaded`) que
  verifica que se carguen los 10 escenarios, por eso se recolectan 11 tests frente a 10.

## 2. Maintainability

- **Agregar un caso:** en el enfoque tradicional hay que escribir una funcion completa
  (6 LOC por test en promedio: 60 LOC / 10 tests); en el data-driven se agrega una fila
  al CSV sin tocar codigo.
- **Cambiar una regla** (p. ej. impuesto 8% -> 10%): en el tradicional se edita cada test
  afectado; en el data-driven se actualizan los valores esperados en el CSV y la logica
  de test no cambia.
- **Riesgo del data-driven:** los valores esperados del CSV pueden quedar desactualizados
  o contener errores de calculo que pasan desapercibidos si no se revisan.

## 3. Readability

- **Traditional:** cada test es autocontenido y se entiende sin abrir otros archivos,
  pero hay mucha repeticion y la estructura (arrange/act/assert) se repite 10 veces.
- **Data-driven:** la logica es unica y corta (14 LOC), pero para ver los escenarios hay
  que abrir el CSV. El CSV ofrece una vista tabular de toda la cobertura de un vistazo, y
  los ids de pytest (`test_order_data_driven[save10_at_threshold]`) mantienen nombres
  descriptivos en el reporte.
- **Organizacion:** el data-driven separa claramente logica (Python) y datos (CSV); el
  tradicional mezcla ambos en cada funcion.

## 4. Coverage

- Escenarios en el comparativo: 10 en el tradicional y 10 en el data-driven (los mismos).
- El archivo data-driven solo selecciona 10 de las 29 filas del CSV mediante un filtro por
  nombre; sin cambiar su codigo podria ejecutar las 29 filas.
- Suite completa data-driven: 29 escenarios de ordenes (`order_calculations.csv`), 30 casos
  de validacion de clientes (`customer_validation.json`) y 4 workflows end-to-end
  (`order_workflows.json`), todos ejecutados con logica de test reutilizable.
- Tiempo de ejecucion medido con pytest:

| Approach | Tests | Tiempo |
|---|---|---|
| Traditional | 10 passed | 0.17 s |
| Data-driven | 11 passed | 0.15 s |
| Ambos juntos | 21 passed | 0.21 s |

  La diferencia es despreciable. El mayor costo en ambos casos fue un `setup` de ~0.11-0.12 s
  en el primer test (arranque de pytest e imports), no la ejecucion de los tests en si.
  Con tan pocos casos, el rendimiento no es un factor de decision.

## 5. Conclusion

**Usar data-driven cuando:** hay muchas combinaciones entrada/salida con la misma logica,
los datos cambian seguido o los mantienen personas no programadoras, o se quiere escalar
la cantidad de casos sin escalar el codigo.

**Usar tradicional cuando:** hay pocos casos, los flujos son distintos entre si, o se
necesita logica especial por test (mocks, setup particular, aserciones propias).

| Pros data-driven | Contras data-driven |
|---|---|
| Escala: mas casos sin mas codigo (76.67% menos LOC en el archivo de test) | Requiere infraestructura de carga y parseo (45 LOC de loader) |
| Separa logica de datos | Depurar una fila puede ser menos directo que un test explicito |
| Facil de revisar en formato tabular | Datos mal formados causan errores confusos |
| Reutilizable entre multiples archivos de test | Un valor esperado erroneo en el dato puede ocultar un bug |