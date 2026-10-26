# Verificación de la entrega

Comprobación realizada el 26 de octubre de 2026, con Python 3.12.14 y pytest 9.0.3.
Alcance: implementación y entrega local dentro del repositorio existente.

| Requisito | Resultado observado |
| --- | --- |
| Pruebas básicas | 53 casos |
| Pruebas de funciones avanzadas | 32 casos adicionales |
| Integración y regresiones | 20 casos adicionales |
| Suite completa | 105 aprobadas, ninguna omitida |
| Cobertura de sentencias | 100 % (154/154) |
| Cobertura de ramas | 100 % (40/40) |
| Duración de la suite (JUnit) | 0.426 s (<2 s) |
| Proceso completo, incluido arranque de Python | 2.1186 s |
| Ciclos con fallo y solución registrados | 54 pares RED/GREEN |
| Refactorizaciones verificadas | 8 |
| Commits TDD | 116, además de configuración, regresiones y documentación |
| Ciclos explicados en detalle | 5 |
| Reflexión | 609 palabras, excluyendo el título |

## Reproducir

Desde la carpeta de entrega y con las dependencias instaladas:

```powershell
.\.venv\Scripts\python.exe tools/check_quality.py
```

El programa ejecuta la suite sin cobertura y conserva el reporte JUnit. Usa el
tiempo de la suite de ese reporte para el límite de dos segundos y registra
separadamente el tiempo del proceso completo, incluido el arranque de Python.
La segunda ejecución cuenta sentencias y ramas y genera el HTML y el JSON.
Comprueba los umbrales de cobertura por separado y rechaza fallos u omisiones.
Los tiempos varían entre equipos; el arranque completo superó dos segundos
en esta máquina y se conserva ese dato en quality.json.

## Evidencias

- [Salida de las 105 pruebas](evidence/tests.txt).
- [Salida de cobertura](evidence/coverage.txt).
- [Resumen de umbrales y tiempo](evidence/quality.json).
- [Detalle de cobertura por archivo](evidence/coverage.json).
- [Registro de fases con hashes y salidas reales](evidence/tdd-runs.jsonl).
- [Informe HTML navegable](../coverage/index.html).

Los commits RED contienen las pruebas antes de su implementación. Su versión
intermedia debe fallar: ese fallo es parte del proceso solicitado. Los mensajes
de configuración, documentación y regresiones no se presentan como fases RED.
Los 116 commits del registro TDD original están limitados a esta carpeta y tienen como máximo 20 líneas
añadidas/eliminadas por commit. No se reescribió el historial del curso.

Se implementaron las tres funciones avanzadas acordadas: multas, filtros e historial.
Los bonos opcionales de JavaScript, video y cinco funciones no forman parte de esta
entrega. La reflexión es técnica y se basa en evidencias; no inventa vivencias del
estudiante. Se usa el repositorio existente según lo acordado. Esta verificación
es local y no atribuye una nota nueva al evaluador de GitHub ni realiza la entrega
en Canvas. La rama de trabajo es 4ald0/homework-06-tdd.


## Correcciones del reporte de calidad

Con la configuración del curso, Pylint 4.0.9 informa **10.00/10**, sin observaciones.
ESLint 8.57.1 informa **0 errores y 0 advertencias** en los dos archivos JavaScript:
el activo mantenido y su copia en el HTML. No se modificaron las reglas del curso,
no se añadieron exclusiones y no se deshabilitaron avisos.

Los metadatos opcionales de Book se agrupan en SearchMetadata; las propiedades
públicas siguen permitiendo leer y modificar género, año y calificación. Se mantienen
las validaciones de cantidades booleanas, fechas datetime y palabras clave inválidas.
Se eliminaron el import sin uso, las comparaciones innecesarias con listas vacías
y los avisos de diccionarios y subprocess. Hay ocho casos adicionales de regresión.

El JavaScript de coverage.py conserva filtros, ordenación, navegación y licencia.
Su copia revisada se aplica al regenerar el informe con tools/check_quality.py y
usa un nombre derivado del contenido. La regeneración se verificó repetidamente.
Playwright con Microsoft Edge comprobó el filtro book, sus totales, la opción de
ocultar cubiertos, el orden descendente, la restauración de filas y el acceso al
código de Book. La consola no registró errores ni advertencias.

- [Pylint: salida local](evidence/pylint-after.txt).
- [ESLint antes: 50 errores observados](evidence/eslint-before.json).
- [ESLint después: 0 errores y advertencias](evidence/eslint-after.json).
- [Resultados JUnit](evidence/test-results.xml).
- [Comprobaciones del navegador](evidence/browser-checks.json).
- [Procedencia y licencia del activo revisado](../tools/coverage_assets/README.md).

Para reproducir los analizadores desde esta carpeta:

```powershell
.\.venv\Scripts\python.exe -m pylint --rcfile=../../../.github/grading/pylintrc src tests tools
npm exec --yes --package=eslint@8.57.1 -- eslint . --no-eslintrc --config ../../../.github/grading/eslintrc.json --ext .js,.mjs,.cjs,.jsx
```
