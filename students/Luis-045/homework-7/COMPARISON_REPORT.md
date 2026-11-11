# Pruebas tradicionales y parametrizadas

Las dos suites verifican los mismos 10 pedidos: dos simples, cinco de
descuentos, dos de envío y uno que combina varios productos, descuento y envío
exprés. En ambos enfoques se comprueba si el cupón fue aceptado cuando se
proporciona uno, y se comparan exactamente los cinco importes del desglose.
La suite parametrizada selecciona las filas con `comparison=true`.

## Líneas de código

Se contaron las líneas de cada archivo después de aplicar Black, incluyendo
importaciones y docstrings. Las dos columnas muestran el conteo con y sin
líneas vacías. El código de producción es común a ambos enfoques.

| Alcance | Líneas físicas | Líneas no vacías |
| --- | ---: | ---: |
| Tradicional: `tests/test_order_traditional.py` | 152 | 131 |
| Parametrizada: `tests/test_order_data_driven.py` | 13 | 8 |
| Soporte compartido: `tests/data_cases.py` | 76 | 64 |
| Parametrizada más todo el soporte compartido | 89 | 72 |

La reducción en el archivo de pruebas es `(152 - 13) / 152 = 91.45%`
por líneas físicas y `(131 - 8) / 131 = 93.89%` sin líneas vacías. Si se
imputa todo el módulo de soporte, incluso su lector JSON para otras suites,
la reducción es 41.45% por líneas físicas y 45.04% sin líneas vacías. El CSV
tiene 30 filas de datos y una cabecera; solo 10 filas se usan en esta
comparación. Separar ese conteo permite ver dónde se movieron los datos.

## Mantenimiento

En la suite tradicional, agregar un pedido implica escribir una función,
configurar el pedido y repetir la comprobación. Cambiar la forma de comprobar
el resultado exige editar las funciones afectadas. En la parametrizada,
agregar o corregir un pedido consiste en editar una fila del CSV. Un cambio
de lógica se hace una sola vez en la prueba o en el módulo de soporte. A
cambio, si se modifica el formato del CSV, también hay que adaptar el lector.

## Lectura y organización

La prueba tradicional se lee de principio a fin sin abrir otro archivo, lo
que ayuda a revisar un ejemplo aislado. En la parametrizada, pytest muestra
el nombre de la fila que falló y la lógica de verificación se puede leer en
una sola función. Para entender un fallo hay que consultar la fila del CSV;
la columna de artículos, al contener JSON, puede resultar menos cómoda de
leer que un literal de Python.

## Cobertura y esfuerzo para crecer

Cada versión ejecuta 10 escenarios y comprueba las mismas reglas. La
parametrización por sí sola no añade cobertura. Permite ampliar la tabla sin
duplicar código: la suite principal reutiliza el mismo CSV para 30 escenarios
de cálculo. Esos casos adicionales no se atribuyen a ninguna de las dos
suites de esta comparación.

Con los datos y resultados ya calculados, estimo **8 a 13 minutos** para
escribir y revisar 10 funciones nuevas, o **3 a 5 minutos** para agregar y
revisar 10 filas. Son estimaciones de edición: aproximadamente 45 a 75
segundos por función frente a 15 a 30 por fila. Diseñar los casos, calcular
los resultados esperados y ejecutar las pruebas requiere trabajo en ambos
enfoques.

## Conclusión

Conviene usar una prueba tradicional cuando el escenario tiene un flujo o
una verificación propios. Para reglas que se ejercitan con muchas
combinaciones de datos, parametrizar reduce la repetición y facilita ampliar
la cobertura. El costo es mantener el formato de datos y localizar la
entrada en un archivo separado cuando falla una prueba.
