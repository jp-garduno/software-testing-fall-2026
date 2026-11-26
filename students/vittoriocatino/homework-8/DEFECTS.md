# Defecto observado en TodoMVC React

## D1 — Escape seguido de blur conserva el texto descartado

- Aplicación: `https://todomvc.com/examples/react/dist/`.
- Reproducido en la ejecución de esta entrega con Selenium y Playwright.
- Pasos: crear `Original`, abrir edición con doble clic, reemplazar por
  `Discarded`, pulsar Escape y hacer clic en el campo de nueva tarea.
- Esperado: la tarea sigue llamándose `Original`.
- Obtenido: la tarea termina llamándose `Discarded`.
- Detalle de diagnóstico: el atributo HTML `value` vuelve a `Original`, pero
  la propiedad viva del input continúa siendo `Discarded`; al perder foco se
  confirma ese texto. Se reprodujo también fuera del Page Object.
- Pruebas: `test_cancel_edit`, una por framework. Conservan la expectativa
  correcta y llevan `xfail(strict=True, raises=AssertionError)` para que un
  error de red/localización no se oculte como defecto conocido. Si la demo se
  corrige, XPASS estricto hará fallar la suite hasta retirar la marca.
- Evidencia: `screenshots/selenium-test_cancel_edit.png` y
  `screenshots/playwright-test_cancel_edit.png`. Para ver el fallo sin marca:
  `python -m pytest -q -k cancel_edit --runxfail`.

El escenario de cancelación está implementado y se ejecuta; no se sustituye su
resultado esperado para producir un verde artificial. BDD cubre los escenarios
obligatorios del enunciado y añade guardar/limpiar completados; el defecto de
cancelación queda registrado en ambas suites de comparación.

## Diferencias respecto a ejemplos antiguos

La URL sin `/dist/` devuelve 404. Se usa la URL React enlazada actualmente en la
página oficial de TodoMVC. El contador de tareas es texto directo en
`.todo-count`, sin un elemento `strong`. Los Page Objects se adaptaron a ese
DOM. El guardado se comprueba en la lista después de Enter o blur: no se exige
persistencia después de recargar, que esta versión de la demo no proporciona
y que la tarea no solicita.
