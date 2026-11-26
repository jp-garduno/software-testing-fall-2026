# Selenium y Playwright — comparación de ejecución

Vittorio Catino · Tarea 8 · Python 3.14.6 · macOS ARM64.

## Condiciones y resultados

Ambas suites ejecutaron los mismos quince escenarios contra TodoMVC React en
Google Chrome **158.0.8127.37**, headless, ventana de 1280 × 900. Se ejecutaron
secuencialmente, con datos limpios y procesos pytest separados mediante
`scripts/run_all.py`. No se mezcló una ejecución simulada con una real.

| Métrica | Selenium | Playwright |
|---|---:|---:|
| Tiempo total de sesión pytest, s | 5.2745 | 7.5499 |
| Promedio de fase call por caso, s | 0.2207 | 0.0889 |
| Inicialización de navegador, s | 0.4414 | 0.3159 |
| Casos ejecutados | 15 | 15 |
| Aprobados | 14 | 14 |
| Fallas conocidas estrictas | 1 | 1 |
| Fallos inesperados | 0 | 0 |

Los datos originales están en `reports/selenium_metrics.json` y
`reports/playwright_metrics.json`. `reports/execution-summary.json` registra
además el tiempo de pared de cada proceso completo, que incluye el arranque del
intérprete y la carga de pytest. La tabla usa la duración interna de sesión;
la media por caso usa sólo la fase call y excluye fixtures y capturas.

El total de Selenium fue menor, mientras que la mayoría de sus operaciones
individuales tardaron más. Playwright creó un contexto nuevo por caso y la
preparación de cada página incluyó navegación, limpieza y recarga; Selenium
reutilizó un perfil desechable de la sesión y limpió sus datos por caso. Por
eso no sería correcto concluir que Selenium es más rápido en general mirando
sólo este total. Además, es una muestra de una ejecución final con cachés y
controlador ya preparados; no es un benchmark estadístico ni incluye el tiempo
de descarga de herramientas. Los detalles de carga y operaciones están en
`PERFORMANCE_REPORT.md`.

La prueba de cancelación encuentra el mismo defecto externo con ambos
frameworks: Escape seguido de blur conserva el texto descartado. Se mantiene
la expectativa correcta con `xfail(strict=True, raises=AssertionError)`.
No se presenta como un caso aprobado. El informe `DEFECTS.md` incluye los pasos
y capturas. BDD pasó ocho escenarios y 37 pasos reutilizando el POM Playwright.

## Código y complejidad

| Código equivalente | Selenium | Playwright |
|---|---:|---:|
| Líneas físicas del Page Object | 150 | 116 |
| Líneas no vacías/no comentarios, incluyendo docstrings | 128 | 95 |

Las líneas se contaron después del formateo. La diferencia de 33 líneas no
vacías representa una reducción de 25.78% en el adaptador Playwright. Los
archivos de prueba son equivalentes: ambos usan los mismos métodos de negocio
y aserciones de listas, estados y contadores, por lo que la diferencia está en
la adaptación al navegador y la sincronización, no en probar menos conductas.

Selenium requiere localizar filas nuevamente después de cambios, implementar
WebDriverWait y manejar el botón visible por hover. Un ejemplo concreto fue
la edición: `clear()` provocaba un ciclo de foco/cambio que invalidaba el
elemento; se sustituyó por selección de texto y escritura mediante teclado.
Playwright usa locators que vuelven a resolver los elementos y `expect` con
reintentos, reduciendo esa coordinación manual. Ninguna suite usa sleeps fijos.

## Experiencia de desarrollo

| Aspecto | Selenium | Playwright | Observación de esta entrega |
|---|---|---|---|
| Instalación | Paquete y controlador compatible | Paquete y navegador/canal | Ambos usan Chrome; Selenium Manager resuelve el driver |
| Auto-waiting | Esperas explícitas para estado de aplicación | Locators y expect con reintentos | Click esperado no sustituye comprobar el resultado |
| Depuración | Excepciones WebDriver, DOM y capturas | Log de acciones, locators y capturas | Playwright mostró valor esperado y valor vivo del input |
| Documentación | Amplia, multilenguaje y con historial largo | Ejemplos coherentes de locators/assertions | Ambas documentaciones ayudaron a aislar los fallos |
| Mensajes de error | TimeoutException o stale element | Expected/actual y acciones esperadas | La información de Playwright fue más directa en edición |
| IDE | Python/pytest y tipado de bindings | Python/pytest y tipado de bindings | Los mismos nombres de caso facilitan navegar entre suites |

## Recomendaciones y aprendizaje

Elegiría Selenium para mantener una suite WebDriver existente, integrarme con
Grid o trabajar en un entorno que ya depende de sus controladores y herramientas.
Elegiría Playwright para un proyecto web nuevo donde importen aislamiento por
contextos, locators y diagnósticos de acciones. Ninguna elección elimina la
necesidad de diseñar escenarios claros y comprobar resultados completos.

El POM permitió adaptar el contador actual sin cambiar todas las pruebas. BDD
expresó creación, completado, eliminación, filtros y guardado con lenguaje de
negocio y tablas de ejemplos. La lección más relevante fue distinguir tres
causas: cambios de URL/DOM, errores de interacción del test y un defecto real de
la aplicación. Convertir la expectativa de cancelación para que aceptara el texto
incorrecto habría ocultado precisamente el problema que las pruebas deben revelar.
