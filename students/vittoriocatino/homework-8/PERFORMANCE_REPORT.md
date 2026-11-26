# Bonus C — mediciones de rendimiento

Las medidas proceden de navegadores reales. Cada operación del POM se registra
con `perf_counter`, nombre, framework, duración y éxito en los archivos
`reports/*_metrics.json`. No se insertan tiempos de espera fijos ni se fabrican
valores para el reporte. Los pasos BDD se ejecutan aparte de la comparación.

## Carga de página

Se usa Navigation Timing del navegador:
`performance.getEntriesByType('navigation')[0].loadEventEnd / 1000`.
El valor es la duración del último documento recargado, en segundos desde su
inicio. Se obtiene una muestra por caso: quince por framework. No mide sólo
tiempo de servidor ni debe confundirse con todo el tiempo de un caso.

| Métrica de carga | Selenium | Playwright |
|---|---:|---:|
| Muestras | 15 | 15 |
| Media, s | 0.0240 | 0.0278 |
| Máximo observado, s | 0.0303 | 0.0331 |
| Navegación + limpieza + recarga + app lista, media s | 0.0758 | 0.2951 |

La última fila corresponde a la operación `navigate`, una medida de preparación
completa que incluye dos navegaciones y sincronización con el input. Es distinta
del evento load del último documento. Las cachés y la distancia a la demo externa
influyen en ambos valores.

## Operaciones de interfaz

| Operación | Muestras por framework | Selenium media s | Playwright media s |
|---|---:|---:|---:|
| Crear tarea | 28 | 0.0207 | 0.0157 |
| Cambiar completado | 11 | 0.0537 | 0.0315 |
| Eliminar tarea | 2 | 0.3191 | 0.0875 |
| Editar tarea | 3 | 0.3360 | 0.0518 |
| Cambiar filtro | 4 | 0.0311 | 0.0379 |
| Limpiar completados | 1 | 0.0383 | 0.0296 |

Estas duraciones incluyen las esperas de confirmación que implementa cada
adaptador. La operación editar sólo mide interacción y salida del editor; el
defecto de cancelación se detecta en la aserción posterior del test. Un tiempo
corto no implica que el comportamiento sea correcto.

## Alcance

Son muestras pequeñas en un único equipo y Chrome. No se calculan percentiles
ni se afirma una mejora universal. El objetivo es mostrar un método reproducible
para registrar carga y operaciones, identificar dónde se consume tiempo y
comparar ambas suites bajo condiciones documentadas. Para un estudio más sólido
harían falta múltiples repeticiones, orden alternado, control de caché, red y
versiones, además de separar corridas frías y calientes.
