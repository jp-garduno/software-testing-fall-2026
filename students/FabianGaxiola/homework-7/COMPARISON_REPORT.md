# Comparación: pruebas tradicionales y basadas en datos

## Metodología

Las dos suites verifican los mismos primeros diez casos de
`test_data/order_calculations.csv`, con las mismas reglas y resultados esperados.
Las cifras de LOC cuentan líneas no vacías que no sean comentarios; no cuentan
docstrings como comentarios. La carga CSV compartida se informa por separado.

## Líneas de código

| Enfoque                                           | LOC | Alcance                                          |
| ------------------------------------------------- | --: | ------------------------------------------------ |
| Tradicional (`tests/test_order_traditional.py`)   |  99 | Diez funciones con sus datos explícitos y helper |
| Parametrizado (`tests/test_order_data_driven.py`) |  24 | Carga compartida y una prueba parametrizada      |
| Loader común (`tests/data_loaders.py`)            |  33 | Parser compartido por pruebas CSV/JSON/workflows |

Solo los módulos de prueba reducen LOC de 99 a 24: **75.8%**. Si se atribuyen
las 33 líneas completas del loader común a la suite parametrizada, esta suma 57
LOC y la reducción neta es **42.4%**. El loader también lo usan otras suites,
así que el costo se amortiza.

## Mantenibilidad y legibilidad

- Para agregar un escenario de pedido en la suite parametrizada se agrega una
  fila al CSV; no hace falta duplicar el flujo de aserciones.
- En la suite tradicional los valores y las aserciones quedan juntos, lo que
  facilita entender un caso aislado, pero un escenario nuevo exige una función
  adicional.
- Los nombres de caso del CSV identifican cada instancia en el reporte de
  pytest. Las funciones tradicionales tienen nombres descriptivos individuales.
- Los datos externos permiten revisar categorías y resultados sin modificar la
  lógica de prueba. Un esquema de datos mal formado se detecta antes de probar
  los resultados.

## Cobertura y costo de crecimiento

Ambas suites tienen diez casos comparables. La ejecución completa incluye 128
pruebas y cubre las cuatro implementaciones de `src/` al 100% de statements.
Agregar diez casos adicionales a la suite de datos requiere diez filas validadas
con resultados esperados; en la tradicional se requieren diez funciones y
aserciones. No se midió tiempo con cronómetro; como estimación de mantenimiento,
editar y revisar diez filas toma alrededor de 5–10 minutos, frente a 15–30
minutos para redactar y revisar diez pruebas tradicionales.

## Conclusión

El enfoque basado en datos conviene cuando muchos escenarios ejercitan el mismo
comportamiento y los datos pueden describirse claramente en una tabla. Las
pruebas tradicionales siguen siendo útiles para transiciones o comportamientos
únicos cuya intención se expresa mejor con una función independiente. En este
proyecto se usan ambas: casos repetibles desde CSV y pruebas tradicionales para
comparar el mismo comportamiento de forma explícita.
