# Verificación de la entrega

Comprobación realizada el 26 de octubre de 2026, con Python 3.12.14.
Alcance: implementación y entrega local dentro del repositorio existente.

| Requisito | Resultado observado |
| --- | --- |
| Pruebas básicas | 49 casos |
| Pruebas de funciones avanzadas | 28 casos adicionales |
| Integración y regresiones | 20 casos adicionales |
| Suite completa | 97 aprobadas, ninguna omitida |
| Cobertura de sentencias | 100 % (132/132) |
| Cobertura de ramas | 100 % (40/40) |
| Ejecución del proceso completo de pruebas | 0.9249 s (<2 s) |
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

El programa ejecuta la suite sin cobertura para medir el proceso completo y después
la ejecuta instrumentada para contar sentencias y ramas. Comprueba ambos umbrales
por separado. La segunda ejecución genera el HTML y el JSON; su sobrecoste no se
utiliza como medida de velocidad de la suite. Los tiempos varían entre equipos.

## Evidencias

- [Salida de las 97 pruebas](evidence/tests.txt).
- [Salida de cobertura](evidence/coverage.txt).
- [Resumen de umbrales y tiempo](evidence/quality.json).
- [Detalle de cobertura por archivo](evidence/coverage.json).
- [Registro de fases con hashes y salidas reales](evidence/tdd-runs.jsonl).
- [Informe HTML navegable](../coverage/index.html).

Los commits RED contienen las pruebas antes de su implementación. Su versión
intermedia debe fallar: ese fallo es parte del proceso solicitado. Los mensajes
de configuración, documentación y regresiones no se presentan como fases RED.
Los cambios TDD están limitados a esta carpeta y tienen como máximo 20 líneas
añadidas/eliminadas por commit. No se reescribió el historial del curso.

Se implementaron las tres funciones avanzadas acordadas: multas, filtros e historial.
Los bonos opcionales de JavaScript, video y cinco funciones no forman parte de esta
entrega. La reflexión es técnica y se basa en evidencias; no inventa vivencias del
estudiante. Los archivos quedan en el repositorio local: no se efectuaron push ni
entrega en Canvas y se omitió el requisito de repositorio público según lo acordado.
