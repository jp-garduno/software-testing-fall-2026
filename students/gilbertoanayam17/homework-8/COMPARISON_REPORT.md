# Comparison Report - Selenium vs Playwright

Las dos suites prueban los mismos 15 escenarios de TodoMVC React, con los mismos nombres de prueba, el mismo navegador (Firefox), la misma ventana de 800 × 900 y la misma estructura (un page object, `test_todo_crud.py` y `test_todo_filter.py`). Como ambas están escritas en Python con pytest, lo único que cambia de una a otra es la herramienta que controla el navegador.

## 1. Execution Time Comparison

Corrí cada suite tres veces seguidas contra el sitio real, en la misma máquina (Windows 11, Python 3.14, Selenium 4.54 y Playwright 1.65) y en modo headless (`HEADLESS=1`), para que dibujar la ventana no sumara tiempo, y en la tabla dejo el promedio. Los tiempos de cada fase salen de `pytest --durations=0`.

| Metric                                    | Selenium | Playwright |
| ----------------------------------------- | -------- | ---------- |
| Total execution time                      | 9.9 s    | 10.9 s     |
| Average per test                          | 0.66 s   | 0.72 s     |
| Setup time, primer test (abre el browser) | 5.3 s    | 1.7 s      |
| Setup time, cada test siguiente           | 0.07 s   | 0.36 s     |

Esperaba que Playwright ganara con claridad, y aunque arranca tres veces más rápido, terminó un segundo más lento. Al revisar las fases encontré dos motivos.

**El aislamiento entre pruebas.** En Selenium todas las pruebas comparten una sola ventana y cada una empieza recargando la página, lo que alcanza en este caso porque la app guarda los todos solo en memoria. Playwright, en cambio, le da a cada prueba un contexto nuevo (con sus propias cookies, storage y caché), que es un aislamiento real pero cuesta unos 0.3 s más por prueba. En 14 pruebas eso suma 4.1 s, más de lo que Playwright ahorra al arrancar (3.6 s). Si la app usara localStorage, Selenium tendría que limpiarlo a mano o abrir un navegador por prueba, y con 5 s de arranque cada vez la suite pasaría de 80 s.

**La prueba que falla a propósito.** `test_cancel_edit` está marcada como `xfail` por un defecto de la app (ver la sección 4). En Selenium el assert falla al instante, mientras que el `expect()` de Playwright reintenta hasta su timeout, que bajé a 1 s para esa prueba. Sin ese segundo, las acciones y comprobaciones de las 15 pruebas toman 1.9 s en Playwright contra 2.8 s en Selenium, por lo que el trabajo dentro de cada prueba sí es más rápido con Playwright.

## 2. Code Comparison

Para el conteo, "código" excluye líneas en blanco, comentarios y docstrings.

| Archivo                            | Selenium (total / código) | Playwright (total / código)   |
| ---------------------------------- | ------------------------- | ----------------------------- |
| Page object (`pages/todo_page.py`) | 170 / 95                  | 109 / 51                      |
| `tests/test_todo_crud.py`          | 123 / 74                  | 129 / 78                      |
| `tests/test_todo_filter.py`        | 32 / 17                   | 33 / 18                       |
| Fixtures (`conftest.py`)           | 31 / 17                   | 27 / 13                       |
| Creación del navegador             | 24 / 11                   | 0 (lo hace pytest-playwright) |
| **Total**                          | **380 / 214**             | **298 / 160**                 |

**Casi toda la diferencia está en el page object.** El de Selenium necesita 12 esperas explícitas (`wait.until`), 5 imports (`By`, `Keys`, `ActionChains`, `WebDriverWait` y `expected_conditions`) y tres helpers privados, mientras que el de Playwright no tiene ninguna espera y solo importa `Page` para el type hint. Por ejemplo, borrar un todo en Selenium implica mover el puntero con `ActionChains` para que aparezca el botón, esperar a que sea visible, hacer clic y esperar a que el elemento quede obsoleto, y en Playwright son `hover()` y `click()`.

**La complejidad no está en las ramas sino en la sincronización.** La complejidad ciclomática es trivial en los dos (ningún método pasa de 2, con una suma de 25 en Selenium y 20 en Playwright). Lo difícil en Selenium es decidir, para cada acción, qué efecto visible esperar (que aumente el número de items, que cambie una clase, que un elemento desaparezca o que el campo de edición se oculte). Si una de esas condiciones está mal elegida, la prueba pasa en mi máquina y falla en CI.

**Las pruebas miden casi lo mismo.** Las de Playwright son unas líneas más largas porque `expect()` revisa un locator a la vez (en `test_complete_multiple_tasks` son tres líneas donde Selenium usa una lista por comprensión), pero a cambio cada comprobación se reintenta sola hasta que la página termina de actualizarse.

## 3. Developer Experience

| Aspect                | Selenium | Playwright | Notes                                                                                                                                                                                                           |
| --------------------- | -------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setup difficulty      | Fácil    | Fácil      | Selenium Manager descargó geckodriver y hasta Firefox (no lo tenía instalado) sin que yo hiciera nada. Playwright pide un paso más (`playwright install firefox`) y usa su propio build de Firefox              |
| Auto-waiting          | No tiene | Sí         | 12 esperas explícitas en un page object contra ninguna en el otro, y los asserts de Selenium tampoco esperan                                                                                                    |
| Debugging             | Regular  | Muy bueno  | En Selenium cuento con el stack trace y los screenshots que yo guarde. Playwright agrega `--headed`, `--slowmo`, `PWDEBUG=1` (inspector paso a paso) y el trace viewer con `--tracing on`                       |
| Documentation quality | Buena    | Muy buena  | La oficial de Selenium es buena, pero al buscar ejemplos aparecen muchos con la API vieja (`find_element_by_id`), que ya no existe en Selenium 4. La de Playwright trae cada ejemplo en Python, JS, Java y .NET |
| Error messages        | Regular  | Muy bueno  | Un `TimeoutException` de `WebDriverWait` llega con el mensaje vacío si no se le pasa uno. Playwright dice qué esperaba, qué encontró y cuántas veces lo reintentó (ejemplo abajo)                               |
| IDE support           | Buena    | Buena      | Las dos tienen type hints completos. Playwright además incluye `playwright codegen`, que graba lo que hago en el navegador y genera el código                                                                   |

La diferencia en los mensajes de error se ve bien con la misma prueba fallida (`test_cancel_edit` corrida con `--runxfail`). Selenium solo reporta el assert de Python.

```text
    assert not todo_page.is_editing(0)
E   assert not True
E    +  where True = is_editing(0)
```

Playwright, en cambio, muestra el locator, el valor que encontró, los reintentos y hasta el texto que tenía el campo (salida recortada).

```text
    expect(todo_page.edit_input).to_be_hidden(timeout=1000)
E   AssertionError: Locator expected to be hidden
E   Actual value: visible
E   Call log:
E     - Expect "to_be_hidden" locator(".todo-list li .edit") with timeout 1000ms
E       9 × locator resolved to <input type="text" class="edit" value="Buy bread" .../>
E   Aria snapshot:
E   - textbox "Edit todo": Buy cake
```

## 4. Recommendations

### When would you choose Selenium?

Lo elegiría cuando el proyecto ya tiene una suite o una infraestructura de Selenium (por ejemplo, un Selenium Grid o un proveedor de navegadores en la nube), cuando el equipo programa en un lenguaje que Playwright no soporta (como Ruby, que tiene bindings oficiales de Selenium pero no de Playwright), o cuando hace falta probar en el navegador de marca tal como lo instala el usuario, incluido Safari real con safaridriver, ya que Playwright prueba Firefox y WebKit con builds propios. También lo usaría si después se van a reutilizar los conocimientos con Appium para apps móviles.

### When would you choose Playwright?

Para casi cualquier proyecto nuevo de una app web moderna. Desde mi punto de vista, lo que más pesa no es la velocidad sino la confiabilidad, ya que el auto-waiting elimina la mayor fuente de pruebas intermitentes, y el aislamiento por contexto evita que una prueba herede datos de otra. A esto se suman el trace viewer, la intercepción de red y el cambio de navegador con un solo flag (`--browser webkit`), que en Selenium requieren configuración o herramientas aparte.

### What did you learn?

- **Una prueba E2E puede encontrar defectos reales.** Esta versión de TodoMVC ignora la tecla Escape, así que el campo de edición sigue abierto y, al perder el foco, guarda el texto que se quería descartar, aunque la especificación de TodoMVC pide descartarlo. Dejé `test_cancel_edit` con `xfail(strict=True)` en ambas suites, de modo que documenta el defecto sin romper la suite y, si algún día lo corrigen, la prueba falla para avisar que hay que quitar la marca.
- **El entorno también cambia.** La URL del enunciado (`/examples/react/`) ahora responde 404 y la app vive en `/examples/react/dist/`, por lo que dejé la URL en una sola constante por page object. Además, con una ventana de 899 px o más, la barra lateral "learn" se carga después de la página y empuja la app 300 px a la derecha, lo que puede hacer que un clic caiga en el lugar equivocado. Con una ventana de 800 px eso nunca pasa.
- **Cada herramienta tiene sus trampas.** En Selenium, `WebElement.clear()` le quita el foco al campo, y en esta app perder el foco guarda la edición (con el texto vacío, borra el todo), por lo que para reemplazar texto usé Ctrl+A. En Playwright, `to_have_text()` normaliza los espacios, así que para comprobar que la app recorta el texto tuve que comparar el contenido exacto.
- **Compartir el navegador es una decisión, no un detalle.** Que todas las pruebas de Selenium compartan una ventana funciona aquí solo porque la app no guarda nada entre recargas. Considero que este tipo de supuesto debe quedar escrito junto al fixture, como lo dejé en `selenium/conftest.py`, porque es justo lo primero que se rompe cuando la app cambia.
