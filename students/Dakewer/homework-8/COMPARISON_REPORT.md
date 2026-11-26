# Reporte comparativo: Selenium vs Playwright

## Condiciones de la medición

- Aplicación: copia local del build oficial de TodoMVC React (commit `ff43b02` de
  `tastejs/todomvc`), servida con `scripts/serve_app.py`. No se midió contra
  todomvc.com.
- Máquina: contenedor Linux con 2 CPU y 7 GB de RAM.
- Versiones: Python 3.13 + Selenium 4.54.0 + pytest 9.1.1; Node 22 + Playwright 1.63.0.
- Navegadores (headless): Selenium y "Playwright full Chromium" usan el mismo
  binario (Chrome for Testing 153.0.8010.12). El *headless shell* de este
  entorno reporta la versión 158.0.8127.36, así que esas filas no son una
  comparación con el mismo navegador.
- Los mismos 26 casos en ambas suites. 7 ejecuciones por configuración,
  intercaladas; se reporta la mediana. Trazas de Playwright desactivadas.
- Datos crudos: `results/benchmark.json`. Se reproduce con `scripts/benchmark.py`.

## 1. Tiempos de ejecución

Configuración por defecto de este repositorio, en serie:

| Metric               | Selenium (navegador nuevo por test) | Playwright (1 worker, headless shell) |
| -------------------- | ----------------------------------: | ------------------------------------: |
| Total execution time |                             25.11 s |                                9.25 s |
| Average per test     |                             0.948 s |                               0.297 s |
| Setup time (por test) |                            0.570 s |                               0.164 s |

*Setup time* es el promedio por test de todo lo previo al cuerpo del test:
navegador o contexto, carga de la página y datos iniciales de los tests de filtro.
*Total* es el tiempo de reloj del proceso completo, incluido su arranque.

Todas las configuraciones:

| Configuración | Total (s) | Min-max (s) | Promedio por test (s) | Setup por test (s) |
| --- | ---: | ---: | ---: | ---: |
| Selenium, navegador nuevo por test | 25.11 | 24.23-26.78 | 0.948 | 0.570 |
| Selenium, navegador compartido | 9.97 | 9.41-10.51 | 0.366 | 0.118 |
| Playwright, 1 worker, full Chromium | 11.97 | 11.28-12.71 | 0.392 | 0.243 |
| Playwright, 1 worker, headless shell | 9.25 | 8.94-9.66 | 0.297 | 0.164 |
| Playwright, 2 workers, headless shell | 6.77 | 6.57-7.06 | 0.403 | 0.231 |

### Interpretación

- **Con aislamiento por test y el mismo navegador**, Playwright fue unas 2.1 veces
  más rápido (11.97 s contra 25.11 s). La diferencia principal es que Selenium
  arranca un navegador por test y Playwright solo crea un contexto nuevo.
- **Selenium no es lento de por sí.** Reutilizando el navegador fue más rápido que
  Playwright con el mismo binario (9.97 s contra 11.97 s). A cambio se pierde
  aislamiento: aquí basta con recargar la página porque la app no guarda datos,
  pero en una app con cookies o `localStorage` habría que limpiarlos.
- Con 2 workers el total bajó 27 % respecto a 1 worker. Cada test fue más lento
  porque compiten por 2 CPU. Selenium también puede paralelizarse con
  `pytest-xdist`; no se midió.
- Es una suite pequeña contra un servidor local. Con red real, la latencia pesaría
  más y las diferencias relativas probablemente serían menores.

## 2. Comparación de código

Líneas de código sin blancos, comentarios ni docstrings (`scripts/count_loc.py`):

| Componente | Selenium (Python) | Playwright (JavaScript) |
| --- | ---: | ---: |
| Page object | 132 | 89 |
| Tests CRUD y edición | 101 | 131 |
| Tests de filtro | 30 | 45 |
| Configuración y fixtures | 49 | 26 |
| **Total** | **312** | **291** |

El total es parecido; cambia dónde está la complejidad:

- El page object de Selenium es 48 % más largo porque cada acción debe definir qué
  esperar (`WebDriverWait`, `StaleElementReferenceException`, `ActionChains`).
  Playwright solo necesita unas pocas llamadas a `waitFor`.
- Los tests de Playwright son más largos por la sintaxis de JavaScript
  (bloques y llaves) y porque algunas comprobaciones usan una aserción por elemento.

La misma acción, borrar una tarea:

```python
# Selenium
item = self._item(index)
ActionChains(self.driver).move_to_element(item).perform()
button = item.find_element(*self.ITEM_DESTROY)
self.wait.until(EC.element_to_be_clickable(button)).click()
self.wait.until(EC.staleness_of(item))
```

```javascript
// Playwright
const todo = this.item(index);
await todo.hover();
await todo.locator('.destroy').click();
```

## 3. Experiencia de desarrollo

Escala de 1 (peor) a 5 (mejor). Las notas son una valoración, no una medición.

| Aspect                | Selenium | Playwright | Notes |
| --------------------- | :------: | :--------: | ----- |
| Setup difficulty      | 3 | 4 | Selenium exige que chromedriver coincida con Chrome (en el entorno usado había un driver 147 para un Chrome 153 y se instaló uno compatible). Playwright instala navegadores acordes a su versión. |
| Auto-waiting          | 2 | 5 | En Selenium las esperas son explícitas. Playwright espera a que el elemento sea accionable y reintenta las aserciones. |
| Debugging             | 3 | 5 | Playwright guarda traza, captura y contexto al fallar. En Selenium la captura al fallar se programó en `conftest.py`. |
| Documentation quality | 4 | 5 | Ambas son completas; la de Playwright está más centrada en un flujo recomendado. |
| Error messages        | 2 | 5 | Ver ejemplos abajo. |
| IDE support           | 4 | 4 | Ambos tienen autocompletado; Playwright ofrece además una extensión oficial para VS Code. |

### Mensajes de error reales

Se provocó el mismo fallo (un elemento que no existe) en ambos.

Selenium, `WebDriverWait` sin `message=`:

```text
selenium.common.exceptions.TimeoutException: Message:
Stacktrace:
#0 0x55629b4cf3da <unknown>
```

Playwright:

```text
TimeoutError: locator.click: Timeout 3000ms exceeded.
Call log:
  - waiting for locator('.does-not-exist')
```

El de Selenium no dice qué se buscaba; conviene pasar siempre `message=` a
`until()`. En comparaciones de valores, `pytest` sí muestra un diff claro.

## 4. Recomendaciones

### Cuándo elegir Selenium

- El equipo ya tiene suites, infraestructura (Selenium Grid) o experiencia en él.
- Se necesita un estándar W3C (WebDriver) o un lenguaje que Playwright no soporta,
  como Ruby.
- Hay que probar en navegadores reales de proveedores o dispositivos remotos que
  solo exponen WebDriver.

### Cuándo elegir Playwright

- Proyecto nuevo de aplicación web moderna.
- Importan el tiempo de CI y la paralelización integrada.
- Se quieren trazas, regresión visual e interceptación de red sin añadir
  librerías.

### Lo aprendido

1. **`clear()` de Selenium puede tener efectos secundarios.** En este campo de
   edición quita el foco, la app interpreta que se guardó un texto vacío y
   **borra la tarea**. Se resolvió seleccionando el texto y escribiendo encima.
2. **El selector del ejemplo `text=Active` es ambiguo.** Con una tarea llamada
   "Active task", `page.click("text=Active")` pulsó esa tarea y no el filtro: la
   URL no cambió y seguían visibles 2 elementos. Se usa `a[href="#/active"]`.
3. **Una prueba puede encontrar un defecto real.** El build probado no atiende la
   tecla Escape: el editor sigue abierto y, al perder el foco, guarda el texto que
   se quería descartar. La especificación de TodoMVC pide descartar los cambios.
   El test se conserva y se marca como fallo esperado
   (`screenshots/02-defect-escape-keeps-editor-open.png`).
4. **`toHaveText` normaliza espacios**, así que no sirve para comprobar el
   recorte de texto; se compara el contenido exacto.
5. **Una comparación justa requiere igualar condiciones.** El resultado cambia
   según se reutilice o no el navegador y qué binario se use.

## Anexo: bonus

- **Regresión visual:** 5 capturas de referencia en
  `playwright/tests/visual/`. Pasaron 25 de 25 en 5 repeticiones. Al cambiar el
  color del título, la prueba falló con 1412 píxeles distintos
  (`screenshots/07-visual-regression-diff.png`).
- **Métricas de rendimiento:** ver `PERFORMANCE_REPORT.md`.
