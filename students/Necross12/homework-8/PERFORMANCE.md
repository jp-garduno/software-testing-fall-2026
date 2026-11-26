# Bonus C: Métricas de rendimiento

Este reporte mide cuánto tarda la aplicación [TodoMVC React](https://todomvc.com/examples/react/dist/) en cargar y cuánto tarda cada operación del Page Object, usando **Selenium** y **Playwright** sobre el mismo flujo.

## Cómo se midió

El script [performance/measure.js](performance/measure.js) reutiliza los dos Page Objects del proyecto ([selenium/pages/TodoPage.js](selenium/pages/TodoPage.js) y [playwright/pages/TodoPage.js](playwright/pages/TodoPage.js)) y ejecuta el mismo flujo con cada herramienta:

1. Arranca el navegador (Chrome headless en ambos casos, para que la comparación sea justa).
2. Navega a la página y lee la **Navigation Timing API** del navegador (`performance.getEntriesByType('navigation')`).
3. Ejecuta cada operación del Page Object y mide su duración con `performance.now()`.
4. Cierra el navegador. Repite todo **5 veces** y calcula promedio, mediana, mínimo y máximo.

Los resultados crudos se guardan en [performance/results.json](performance/results.json).

```bash
npm run perf            # 5 repeticiones (por defecto)
RUNS=10 npm run perf    # más repeticiones (en PowerShell: $env:RUNS=10; npm run perf)
```

**Entorno:** Windows 11, Node.js 22.20.0, Chrome 158, selenium-webdriver 4.51, Playwright 1.65.1 (Chromium incluido). Medido el 25/11/2026 con conexión a internet doméstica.

## 1. Carga de la página

| Métrica (ms)                          | Selenium (prom / mediana) | Playwright (prom / mediana) |
|---------------------------------------|---------------------------|-----------------------------|
| Arranque del navegador                | 372 / 340                 | 180 / 110                   |
| `navigate()` completo                 | 367 / 362                 | 284 / 288                   |
| Time To First Byte (TTFB)             | 124 / 117                 | 79 / 75                     |
| `DOMContentLoaded`                    | 233 / 238                 | 168 / 166                   |
| Evento `load`                         | 346 / 345                 | 259 / 261                   |

- La página carga en **~0.25–0.35 s** en ambos casos. La diferencia entre herramientas en TTFB y `load` se debe sobre todo a la red y al perfil del navegador (Chrome del sistema vs. Chromium de Playwright), no a la herramienta de pruebas, porque son métricas que mide el propio navegador.
- El **arranque del navegador** sí depende de la herramienta: Playwright tarda la mitad porque se comunica directamente con Chromium (CDP), mientras que Selenium tiene que iniciar `chromedriver` y crear una sesión WebDriver por HTTP.

## 2. Tiempo por operación

| Operación (ms)                    | Selenium prom | Playwright prom | Más rápido          |
|-----------------------------------|---------------|-----------------|---------------------|
| `addTodo` (1 tarea)               | 45            | 26              | Playwright          |
| `addTodos` (3 tareas)             | 63            | 28              | Playwright          |
| `toggleTodo`                      | 49            | 37              | Playwright          |
| `filterActive`                    | 44            | 35              | Playwright          |
| `filterCompleted`                 | 37            | 35              | Empate              |
| `filterAll`                       | 33            | 33              | Empate              |
| `getVisibleTodos`                 | 37            | 4               | Playwright (≈9x)    |
| `editTodo`                        | 195           | 48              | Playwright (≈4x)    |
| `deleteTodo`                      | 161           | 89              | Playwright          |
| `clearCompleted`                  | 33            | 46              | Selenium            |

Observaciones:

- **`getVisibleTodos`** es la diferencia más grande. En Selenium cada `findElement` y cada `getText` es una petición HTTP al driver, así que leer N tareas cuesta N+1 viajes de ida y vuelta. En Playwright, `allTextContents()` obtiene todos los textos en una sola llamada.
- **`editTodo`** es ~4 veces más lento en Selenium porque necesita varias llamadas: doble clic con `actions()`, una espera explícita a que el input sea visible, `Ctrl+A`, `Backspace` y escribir el texto. En Playwright basta con `dblclick()` y `fill()`.
- **`deleteTodo`** tarda más en ambos porque requiere un *hover* para que aparezca el botón `.destroy`.
- Los clics simples (filtros, `clearCompleted`) cuestan prácticamente lo mismo (~30–45 ms); ahí el costo lo domina el re-render de React, no la herramienta.

## 3. Tiempo de ejecución de las suites

Promedio de varias ejecuciones locales, sin contar la primera ("en frío"):

| Suite                                        | Pruebas      | Tiempo del runner | Tiempo total con `npm` | Promedio por prueba |
|----------------------------------------------|--------------|-------------------|------------------------|---------------------|
| Selenium + Jest (`--runInBand`)              | 15           | ~7.0 s            | ~9.2 s                 | ~0.47 s             |
| Playwright (2 workers, configuración actual) | 15           | ~8.7 s            | ~10.9 s                | ~0.58 s             |
| Playwright (`--workers=1`)                   | 15           | ~10.5 s           | ~12.6 s                | ~0.70 s             |
| Cucumber + Selenium (BDD)                    | 6 escenarios | ~6.3 s            | ~9.8 s                 | ~1.05 s / escenario |

Aunque Playwright es más rápido en cada operación, **la suite de Selenium termina antes**. Esto se debe a cómo están organizadas las pruebas, no a la herramienta:

- En Selenium se abre **un navegador por archivo** (`beforeAll`) y en cada prueba solo se vuelve a navegar a la página.
- En Playwright, cada prueba recibe un **contexto de navegador nuevo** (mejor aislamiento) y además está configurado `screenshot: 'on'` y `trace: 'retain-on-failure'`, lo que graba trazas y toma una captura extra en cada prueba, además de la captura de página completa del `afterEach`.
- En Cucumber se abre un navegador nuevo por escenario (`Before` en [features/support/hooks.js](features/support/hooks.js)), por eso el costo por escenario es el más alto.

La primera ejecución de cada suite siempre fue más lenta (Selenium 14.6 s, Playwright 12.2 s) por la caché del navegador y la red en frío.

## 4. Conclusiones

1. **Por operación, Playwright es más rápido** (de 1.3 a 9 veces en las operaciones que hacen varias llamadas), porque usa una conexión persistente con el navegador en lugar de una petición HTTP por comando.
2. **Por suite, el diseño de las pruebas pesa más que la herramienta.** Reutilizar el navegador (Selenium) es más rápido; aislar cada prueba (Playwright) es más confiable. Con Playwright se puede recuperar el tiempo aumentando `workers` o con `fullyParallel: true`.
3. **Las capturas y trazas tienen un costo.** Para ejecuciones rápidas en local se podría usar `screenshot: 'only-on-failure'` y dejar las capturas completas solo para CI.

## Limitaciones

- La página está en internet (todomvc.com), así que la red añade variación; por eso se reportan promedio y mediana.
- Solo son 5 repeticiones en una sola máquina; los números sirven para comparar, no como valores absolutos.
- La suite de Selenium corre con el navegador visible, mientras que Playwright y el script de rendimiento corren en modo headless.
