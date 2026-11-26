# Comparación: pruebas tradicionales y basadas en datos

**Vittorio Catino — Tarea 7**

## Método y equivalencia

Se compararon `test_order_traditional.py`, con diez funciones y entradas
literales, y `test_order_data_driven.py`, con una función parametrizada desde
CSV. Ambas verifican exactamente los mismos diez escenarios y el mismo
desglose completo: subtotal, descuento, impuesto, envío y total. El script
`scripts/compare_suites.py` comprueba que los nombres de las diez funciones
coincidan, en orden, con los primeros diez registros del archivo externo.

Los escenarios son: pedido simple, cantidad múltiple, pedido vacío, SAVE10
exactamente en 50 y por encima, SAVE20 exactamente en 100 y por encima,
SAVE10 por debajo del umbral, NEWUSER elegible y cliente recurrente no elegible.
El análisis no compara diez pruebas tradicionales con los 100 pedidos generados,
porque eso mezclaría estilos de prueba con cantidades de escenarios diferentes.

## Líneas de código

| Medida | Tradicional | Data-driven |
|---|---:|---:|
| Líneas físicas del archivo de pruebas | 152 | 24 |
| Líneas no vacías y no comentarios, incluyendo docstrings | 131 | 18 |
| Funciones de prueba escritas | 10 | 1 |
| Escenarios ejecutados | 10 | 10 |

La reducción del código de prueba es `(131 − 18) / 131 × 100 = 86.26%`.
Los resultados crudos y las cinco mediciones por suite están en
`reports/comparison_metrics.json`. La métrica no incluye el CSV ni el lector
compartido: separar datos mueve parte del trabajo a esos archivos, no lo elimina.
Los diez registros equivalentes ocupan once líneas de CSV incluyendo encabezado.
Contarlos junto con las 18 líneas de prueba da 29 líneas frente a 131, una
reducción de 77.86%; el validador/lector reutilizable sigue siendo un costo
adicional compartido por la suite completa.

## Mantenibilidad

Agregar un caso al enfoque tradicional exige crear otra función, construir un
pedido, configurar cupón y envío y repetir las aserciones. La versión basada en
datos sólo necesita otro registro con entradas y expectativas revisadas. Si
cambia la forma del resultado, una corrección a la prueba parametrizada alcanza
a todos los escenarios. En la versión tradicional hay diez lugares que revisar.

La separación también impone responsabilidades: validar tipos, manejar las
comillas del CSV y no confundir datos intencionalmente inválidos con archivos
corruptos. Los lectores de este proyecto comprueban el esquema y reportan
archivo y línea antes de las pruebas de negocio. Las expectativas principales
son literales independientes del sistema bajo prueba, para evitar que un error
del calculador se copie automáticamente a los datos esperados.

## Legibilidad y organización

Una función tradicional se entiende de forma aislada: contiene todas las
entradas y el resultado esperado. Es conveniente para un flujo excepcional o
una regresión compleja. Cuando muchas funciones repiten la misma secuencia,
el ruido hace más difícil encontrar las diferencias importantes.

La parametrización expresa una vez el contrato y conserva nombres legibles en
pytest. El CSV permite comparar umbrales y descuentos por filas. Su desventaja
es que entender un caso requiere revisar la prueba y el archivo de datos;
además, un array JSON dentro de CSV es menos cómodo de editar manualmente.

## Cobertura, tiempo y escalabilidad

Cada versión ejecuta diez escenarios equivalentes. La suite completa contiene
31 pedidos base, 30 clientes, cinco flujos, cien pedidos generados y pruebas
adicionales de errores y estado. El resultado final es 212 pruebas aprobadas y
100% de sentencias y ramas de `src/`. Tener más filas no garantiza mejores
pruebas: el valor depende de cubrir límites, estados y reglas diferentes.

En Python 3.14.6 se ejecutó cada suite cinco veces en procesos nuevos. La mediana
del tiempo total, incluyendo inicio y colección de pytest, fue 0.1768 s para
tradicional y 0.1742 s para data-driven. La diferencia es demasiado pequeña
para concluir una ventaja de velocidad; el beneficio demostrado está en
reducción de repetición y facilidad de mantenimiento.

Agregar diez casos se estima en 5–10 minutos con CSV y 15–25 minutos con
funciones repetidas, suponiendo que los oráculos ya estén definidos. Son
estimaciones de edición, no tiempos medidos: revisar reglas y calcular los
resultados esperados cuesta trabajo en ambos enfoques.

## Conclusión

Usaría pruebas basadas en datos para combinaciones repetidas de entrada/salida,
fronteras y regresión masiva. Preferiría funciones explícitas cuando cada caso
necesita preparación, acciones o verificaciones distintas. Combinar ambos
permite mantener visible la intención de los casos especiales y escalar los
contratos repetibles, sin sacrificar la independencia de sus expectativas.
