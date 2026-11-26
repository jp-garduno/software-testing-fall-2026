# Análisis de cobertura

## Ejecuciones verificadas

Python 3.12.14, pytest 8.4.2, pytest-cov 7.1.0 y coverage.py 7.16.2.
La suite sin instrumentación pasó sus **112 casos en 0.75 s**. La ejecución
con cobertura de ramas, salida detallada y reportes pasó en **2.84 s**.
Los tiempos son los reportados por pytest; excluyen el arranque del proceso.

```text
pytest -q
112 passed in 0.75s

pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-report=json:reports/coverage.json
112 passed in 2.84s
```

La salida íntegra de la segunda ejecución está en `test-execution.txt`.

## Resumen

| Métrica | Requisito | Medición | Estado |
| --- | --- | --- | --- |
| Sentencias | >80% | 187/187 = 100% | Cumple |
| Ramas | >80% | 54/54 = 100% | Cumple |
| Funciones con nombre | >80% | 29/29 = 100% | Cumple |
| Líneas ejecutables | Informativa | 187/187 = 100% | Cumple |

Coverage.py representa las sentencias mediante líneas ejecutables. Las ramas
son los destinos medidos por el instrumento; no equivalen a cobertura completa
de todas las combinaciones booleanas ni de todos los caminos posibles.
`tools/report_metrics.py` calcula funciones cubiertas como cuerpos con nombre
que tienen al menos una línea ejecutada. Excluye solamente la entrada sin nombre
que representa el módulo, sin filtros de exclusión de código de producción.

## Cobertura por archivo

| Archivo | Sentencias | Ramas | Funciones |
| --- | --- | --- | --- |
| `src/task.py` | 62/62 (100%) | 16/16 (100%) | 8/8 (100%) |
| `src/task_service.py` | 104/104 (100%) | 38/38 (100%) | 12/12 (100%) |
| `src/task_repository.py` | 14/14 (100%) | 0, no aplica | 6/6 (100%) |
| `src/notification_service.py` | 7/7 (100%) | 0, no aplica | 3/3 (100%) |
| `src/__init__.py` | 0, no aplica | 0, no aplica | 0, no aplica |

## Estrategia y hallazgos

1. Las 59 pruebas parametrizadas del modelo cubren creación, tipos inválidos,
   longitudes límite, comparación de prioridades y las 16 parejas de estados.
   El reloj controlado permite probar pasado, igualdad y futuro sin esperas.
2. Los 19 casos de integración verifican flujos de creación, edición,
   finalización y archivo, unicidad, búsqueda y borrado. Se usan tanto mocks
   del repositorio como un repositorio real con almacenamiento falso.
3. Los 19 casos límite verifican edición atómica, registros ausentes, archivo
   sin cambios simultáneos, fechas inclusivas y actualización de tareas vencidas.
4. Los 15 casos de mocking comprueban valores de retorno, argumentos, orden de
   llamadas, aislamiento y fallos de base de datos, correo y SMS. Una lista de
   llamadas conjunta verifica que persistir sucede antes de notificar.

La primera ejecución completa midió 100% de cobertura pero falló una prueba:
el almacén falso copiaba profundamente también el reloj, congelando su estado
en cada registro. Se cambió por copias independientes de las tareas que
comparten el reloj inyectado. La ejecución final pasó todos los casos sin
cambiar las reglas de producción. Este hallazgo demuestra que cubrir líneas
no basta para asegurar que el comportamiento sea correcto. No se presenta una
tendencia porcentual inventada: ambas mediciones completas alcanzaron 100%.

## Caminos sin cubrir y límites

El reporte final no contiene líneas ni ramas faltantes y no se emplean
`pragma: no cover`, omisiones, xfail ni exclusiones personalizadas.
El JSON resumido conserva los conteos y listas vacías de código faltante.

La cobertura mide únicamente `src/`. No garantiza la integración con una base
de datos real, entregabilidad de mensajes, concurrencia, unicidad transaccional,
seguridad o comportamiento de un programador periódico. Los adaptadores reales
requerirían pruebas de contrato y de sistema en su infraestructura. Las funciones
generadas por dataclass no se cuentan como funciones propias instrumentadas.

Para ampliar la calidad, se podrían agregar pruebas de mutación y contratos de
adaptadores reales. El objetivo sería detectar errores nuevos, no aumentar un
porcentaje que ya alcanzó su límite.

## Capturas

- [Resumen HTML real de coverage.py](screenshots/coverage-summary.png).
- [Líneas instrumentadas del servicio](screenshots/coverage-html-report.png).
- [Salida de pytest](screenshots/test-execution.png): extracto literal del
  archivo capturado, mostrado en un navegador para obtener la imagen; no es
  una captura de una ventana de terminal. El archivo de texto conserva la
  salida completa para su revisión.
