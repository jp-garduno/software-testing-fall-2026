# Comparison Report: Selenium vs Playwright

Las dos suites prueban **los mismos 30 escenarios** (creación, completar, borrar, editar y filtros) sobre la
misma app, con el mismo patrón Page Object y el mismo navegador (Chromium 153, headless, ventana de 1280×900).

**Entorno de medición:** Linux con 2 núcleos, la app servida localmente (misma versión que todomvc.com), tres
ejecuciones de cada suite. Las cifras sirven para comparar entre sí, no como valores absolutos: contra el sitio
real hay que sumar la latencia de red.

## 1. Execution Time Comparison

| Metric | Selenium (pytest) | Playwright (1 worker) | Playwright (paralelo, 2 workers) |
| ------ | ----------------- | --------------------- | -------------------------------- |
| Total execution time (3 corridas) | 12.2 / 12.6 / 12.6 s | 12.2 / 12.7 / 13.1 s | 13.3 / 13.2 / 13.6 s |
| Average per test | ~0.41 s | ~0.42 s | ~0.44 s |
| Setup time (abrir navegador) | 0.35-0.37 s | 0.12-0.19 s | 0.12-0.19 s |
| Primera carga de la página | 0.10-0.11 s | 0.08-0.10 s | 0.08-0.10 s |

Observaciones:

- **El tiempo total quedó prácticamente empatado.** No es el resultado que esperaba, y tiene explicación:
  - Selenium abre **un solo navegador** para toda la sesión y solo recarga la página entre pruebas.
  - Playwright crea un **contexto nuevo** (perfil limpio) para cada prueba, que es un aislamiento más fuerte y
    cuesta un poco más.
- **El paralelismo no ayudó aquí**: con 2 núcleos, dos navegadores compiten por la CPU. En una máquina con más
  núcleos el modo paralelo de Playwright sí reduce el tiempo total; Selenium necesitaría `pytest-xdist` y un
  navegador por proceso para lograr lo mismo.
- **Arranque**: Playwright inicia Chromium unas 2-3 veces más rápido porque habla con el navegador directamente
  (CDP), sin el proceso intermedio de chromedriver.

## 2. Code Comparison

Líneas de código sin líneas en blanco ni comentarios:

| Parte | Selenium (Python) | Playwright (JavaScript) |
| ----- | ----------------- | ----------------------- |
| Page Object | 136 (sin docstrings) | 86 |
| Configuración / fixtures | 47 (`conftest.py` + `driver_factory.py`) | 22 (`playwright.config.js`) |
| Pruebas CRUD + filtros | 146 | 189 |
| Esperas explícitas escritas a mano | 11 `wait.until(...)` | 0 |

- **El Page Object de Playwright es ~35% más corto.** Casi toda la diferencia son esperas: en Selenium cada acción
  tiene que esperar el estado que produce. Por ejemplo, `add_todo` espera a que el campo se vacíe y a que cambie
  el número de elementos, y además debe saber que en el filtro Completed la tarea nueva no aparece. En
  Playwright `addTodo` son dos líneas y la espera la hace la aserción.
- **Las pruebas de Playwright tienen más líneas**, pero por estilo, no por complejidad: cada aserción es un
  `await expect(...)` en su propia línea, y JavaScript agrega llaves y `async`.
- **Complejidad:** en Selenium la dificultad está en el Page Object (sincronización); en Playwright, en entender
  qué hace cada matcher web-first (`toHaveText`, `toHaveCount`), que reintenta hasta cumplirse.
- **Interacciones:** borrar requiere pasar el mouse sobre la tarea para que aparezca la ×. En Selenium:
  `ActionChains(...).move_to_element(...)` más una espera. En Playwright: `hover()` y `click()`.

## 3. Developer Experience

| Aspect | Selenium | Playwright | Notes |
| ------ | -------- | ---------- | ----- |
| Setup difficulty | Media | Fácil | Selenium Manager ya resuelve el driver, pero sigue habiendo un proceso intermedio cuya versión debe coincidir con la del navegador (aquí 147 contra 153 obligó a usar `--disable-build-check`). Playwright descarga su propio navegador con `npx playwright install`. |
| Auto-waiting | No (manual) | Sí | Las dos fallas de mi primera corrida de Selenium fueron de sincronización o de clics bloqueados; en Playwright no hubo ninguna. |
| Debugging | Básico | Excelente | Selenium: capturas al fallar (las agregué yo en `conftest.py`) y el stacktrace. Playwright: trace viewer con cada paso, DOM y red, video y modo `--debug` paso a paso. |
| Documentation quality | Buena | Muy buena | La de Playwright tiene ejemplos por lenguaje y una guía de buenas prácticas; la de Selenium es más extensa pero dispersa entre lenguajes y versiones. |
| Error messages | Regulares | Muy buenos | Un `TimeoutException` de Selenium llega con mensaje vacío; Playwright dice qué localizador esperaba, qué recibió y el log de reintentos. |
| IDE support | Bueno | Muy bueno | Ambos tienen autocompletado; Playwright tiene extensión oficial de VS Code con ejecución por prueba y generación de localizadores (`codegen`). |

Ejemplo real de mensajes de error, de la primera corrida:

- **Selenium** al hacer clic en "marcar todas": `ElementClickInterceptedException: element click intercepted:
  Element <label class="toggle-all-label"> is not clickable... Other element would receive the click: <input
  class="toggle-all">`. Es claro, pero la prueba ya falló.
- **Selenium** al esperar una tarea nueva en el filtro Completed: `TimeoutException: Message:` (vacío). Hubo que
  depurar para descubrir que la tarea no se muestra en esa vista.

## 4. Recommendations

**¿Cuándo elegiría Selenium?**

- Cuando hay que probar navegadores o plataformas que Playwright no cubre: Safari real en macOS, Internet
  Explorer/Edge legacy, navegadores móviles reales con Appium, o granjas como Selenium Grid / BrowserStack ya
  contratadas.
- Cuando el equipo ya tiene una suite grande en Selenium o trabaja en un lenguaje con mejor soporte de Selenium
  (por ejemplo Ruby o PHP).
- Cuando se requiere un estándar W3C (WebDriver) por políticas de la empresa.

**¿Cuándo elegiría Playwright?**

- Para un proyecto nuevo de pruebas web: menos código de sincronización, pruebas menos frágiles y mejores
  herramientas de diagnóstico.
- Cuando se necesitan capacidades integradas: regresión visual, interceptar red, emular dispositivos, varios
  contextos aislados y ejecución en paralelo sin infraestructura extra.
- En CI, donde el trace viewer ahorra mucho tiempo al investigar una prueba que falló en otra máquina.

**¿Qué aprendí?**

- El **Page Object** paga desde el primer cambio. Al descubrir que la casilla "marcar todas" tapa su etiqueta,
  solo hubo que cambiar un localizador en un archivo y las pruebas y los pasos BDD siguieron igual.
- **La sincronización es el problema central de las pruebas E2E.** En Selenium la esperas tú; en Playwright la
  herramienta espera por ti, pero conviene entender qué está esperando.
- **Las pruebas de sistema encuentran defectos reales de la aplicación.** Escape no cancela la edición, como
  marca la especificación de TodoMVC, y el enlace del enunciado da 404. Lo que no hace la app hay que
  documentarlo, no esconderlo con una prueba a la medida.
- **El aislamiento tiene costo:** un contexto nuevo por prueba (Playwright) es más seguro que reutilizar el
  navegador (Selenium), y en esta app costó casi lo mismo.
- **BDD** sirve como capa de lenguaje de negocio encima del mismo Page Object: los pasos de behave tienen una o
  dos líneas cada uno.
