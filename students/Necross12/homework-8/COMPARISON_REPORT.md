# Part 4: Comparison Report — Selenium vs. Playwright

Ambas suites prueban las mismas 15 funcionalidades (creación, completado, eliminación, filtrado y edición de tareas) sobre TodoMVC React, con el mismo diseño de Page Object y escritas en JavaScript.

**Entorno:** Windows 11, Node.js 22.20.0, Chrome 158, selenium-webdriver 4.51 + Jest 30, Playwright 1.65.1. El detalle de las mediciones está en [PERFORMANCE.md](PERFORMANCE.md).

## 1. Execution Time Comparison

Promedio de varias ejecuciones locales (sin contar la primera, que siempre fue más lenta por la caché del navegador):

| Métrica                                   | Selenium                                          | Playwright                                  |
|-------------------------------------------|---------------------------------------------------|---------------------------------------------|
| Tiempo de ejecución (15 pruebas)          | ~7.0 s (~9.2 s con `npm`)                         | ~8.7 s con 2 workers / ~10.5 s con 1 worker |
| Promedio por prueba                       | ~0.47 s                                           | ~0.58 s (2 workers) / ~0.70 s (1 worker)    |
| Tiempo de configuración (mío, desarrollo) | 2.5 h                                             | 1 h                                         |
| Arranque del navegador                    | ~372 ms                                           | ~180 ms                                     |
| Resultado                                 | 15/15 (una ejecución tuvo 2 fallos intermitentes) | 15/15 en todas las ejecuciones              |

La gran discrepancia en el tiempo de configuración se debe a que ya había usado una de estas herramientas en Calidad y a que una resulta más sencilla de utilizar que la otra. Después de batallar con Selenium, Playwright me pareció mucho más fácil, tanto por sus diferencias de diseño como porque su sintaxis es más sencilla.

**¿Por qué la suite de Selenium terminó antes si Playwright es más rápido en cada operación?** Selenium reutiliza un solo navegador por archivo (`beforeAll`) y solo vuelve a navegar en cada prueba, mientras que Playwright crea un contexto nuevo por prueba y además graba una captura y una traza en cada una (`screenshot: 'on'`, `trace: 'retain-on-failure'`). En operaciones individuales Playwright fue de 1.3 a 9 veces más rápido (por ejemplo, `editTodo`: 195 ms vs. 48 ms; `getVisibleTodos`: 37 ms vs. 4 ms).

**Estabilidad:** en la primera ejecución de Selenium fallaron las dos pruebas de eliminar con `ElementNotInteractableError`: el *hover* todavía no mostraba el botón `.destroy` cuando se hizo clic. Al repetir pasaron 15/15. Playwright no tuvo ningún fallo, porque `click()` espera a que el elemento sea visible y se pueda interactuar con él.

## 2. Code Comparison

Líneas de código sin contar líneas vacías ni comentarios:

| Archivo                      | Selenium | Playwright | Diferencia |
|------------------------------|----------|------------|------------|
| Page Object (`TodoPage.js`)  | 130      | 96         | −26 %      |
| `TodoCrud.test.js`           | 97       | 89         | −8 %       |
| `TodoFilter.test.js`         | 38       | 30         | −21 %      |
| **Total**                    | **265**  | **215**    | **−19 %**  |

Las pruebas son casi idénticas; la diferencia está en el Page Object, donde Selenium necesita más pasos para lo mismo:

| Funcionalidad        | Selenium                                                                     | Playwright                                        |
|----------------------|------------------------------------------------------------------------------|---------------------------------------------------|
| Leer textos visibles | `findElements` + ciclo `for` con `findElement('label')` y `getText()`        | `locator(...).locator('label').allTextContents()` |
| Editar una tarea     | `actions().doubleClick()`, espera explícita, `Ctrl+A`, `Backspace`, escribir | `dblclick()` + `fill()`                           |
| Eliminar (hover)     | `actions().move({ origin: item }).perform()` y luego buscar `.destroy`       | `hover()` + `click()`                             |
| Esperas              | `driver.wait(until.elementLocated / elementIsVisible)` manuales              | Automáticas en cada acción                        |
| Índice inexistente   | Método auxiliar `_getTodoItem` que valida el índice                          | `nth(index)` falla con un mensaje claro           |
| Ciclo del navegador  | `Builder().build()` en `beforeAll` y `driver.quit()` en `afterAll`           | El fixture `page` lo maneja el runner             |

En complejidad, el Page Object de Selenium tiene más ramas y estado manual (esperas, validación de índices, manejo de `WebElement`), mientras que en Playwright casi todos los métodos son de una o dos líneas porque los *locators* son perezosos y se resuelven en el momento de la acción.

## 3. Developer Experience

| Aspecto                     | Selenium    | Playwright | Notas                                                                                                                                                                                                                                   |
|-----------------------------|-------------|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Dificultad de configuración | Media       | Media-baja | Selenium necesita un runner aparte (Jest), Chrome instalado y manejar el driver a mano. Playwright trae runner, reportes y navegadores (`npx playwright install`).                                                                      |
| Espera automática           | No          | Sí         | En Selenium tuve que poner esperas explícitas, y aun así el *hover* de eliminar falló una vez. Playwright espera a que el elemento sea accionable.                                                                                      |
| Debugging                   | Baja        | Alta       | Playwright tiene reporte HTML, Trace Viewer y modo UI (`--ui`). En Selenium dependía de las capturas y de `console.log`.                                                                                                                |
| Calidad de la documentación | Media       | Alta       | La documentación de Selenium tiene pocos ejemplos en JavaScript (la mayoría están en Java/Python). La de Playwright tiene ejemplos completos en JS.                                                                                     |
| Mensajes de error           | Media-baja  | Alta       | Más que por los mensajes de error, identificaba los fallos mediante las capturas de pantalla. Selenium solo dice `element not interactable`; Playwright muestra el locator, el registro de la llamada y el valor esperado vs. recibido. |
| Soporte IDE                 | Desconocida | Media      | Contaba con la extensión de Playwright por la materia de Calidad. Para Selenium solo tuve el autocompletado normal de JavaScript.                                                                                                       |

## 4. Recommendations

- **¿Cuándo elegirías Selenium?**
  Me pareció útil para escenarios donde se necesita mayor control. Como se comentó en clase, al ser más configurable y menos rígido en su sintaxis, resulta adecuado para experimentar y plantear pruebas complejas con flexibilidad. También lo elegiría si el equipo ya usa Java/Python/C#, si se necesita un Selenium Grid o una nube de dispositivos existente, o si hay que probar navegadores que Playwright no soporta.

- **¿Cuándo elegirías Playwright?**
  Cuando requiero pruebas más sencillas en una página web, con menos requisitos o necesito avanzar más rápido y con menor carga operativa, ya que el nivel de exigencia de las pruebas no necesita ser tan estricto en esos casos. Además, por la espera automática, el aislamiento por prueba y las trazas, es la opción que elegiría para un proyecto nuevo de aplicaciones web modernas (React, SPA) y para correr en CI con varios navegadores.

- **¿Qué aprendiste?**
  Aprendí a usar mejor Selenium, ya que en la materia de Pruebas solo lo revisé por encima, y retomé el uso de Playwright, que hacía tiempo no utilizaba. También aprendí a consultar y revisar los reportes: en Calidad supe que existían porque se mencionaron en clase, pero como no los usamos y creamos los nuestros con capturas, fue un tema que apenas había tocado en ese momento; por ello, resultó valioso conocer cómo funcionan en la práctica.
  Al medir los tiempos también aprendí que la velocidad de una suite depende más de su diseño (reutilizar o aislar el navegador, paralelismo, capturas y trazas) que de la herramienta, y que sin espera automática aparecen pruebas intermitentes como la de eliminar en Selenium.
