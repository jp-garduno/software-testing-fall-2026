# Análisis de cobertura de TaskFlow

## Alcance y herramientas

Medición realizada sobre los cinco archivos de `src/` con Python 3.13.9, pytest 8.4.2, pytest-cov 7.1.0 y coverage.py 7.16.2. No se incluyen las pruebas ni el fake del repositorio en el porcentaje de producción.

Comando, ejecutado desde la carpeta de la entrega:

```powershell
.\.venv\Scripts\pytest.exe -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-report=json
```

Resultado: **124 casos aprobados**. No hay pruebas omitidas ni marcadas xfail. Una ejecución sin cobertura tomó **0.38 segundos**; la ejecución que generó inicialmente el HTML y JSON final tomó **0.97 segundos** según pytest. Son mediciones locales, no garantías de rendimiento en otros equipos.

## Resumen

| Métrica | Requisito | Medido | Resultado |
| --- | --- | --- | --- |
| Sentencias globales | >80% | 196/196 = 100% | Cumple |
| Sentencias del modelo | >80% | 82/82 = 100% | Cumple |
| Ramas globales | >80% | 66/66 = 100% | Cumple |
| Funciones implementadas | >80% | 20/20 = 100% | Cumple |
| Líneas ejecutables | Referencia | 196/196 = 100% | Sin líneas faltantes |

Con `--cov-branch`, la columna `Cover` de coverage.py combina sentencias y salidas de ramas: `(196 + 66) / (196 + 66) = 100%`. Este valor combinado no reemplaza la comprobación independiente de cada métrica.

## Desglose por archivo

| Archivo | Sentencias | Ramas | Funciones implementadas | Líneas faltantes |
| --- | --- | --- | --- | --- |
| `src/__init__.py` | 0/0 | No aplica | No aplica | Ninguna |
| `src/task.py` | 82/82 | 26/26 | 10/10 | Ninguna |
| `src/task_service.py` | 100/100 | 40/40 | 10/10 | Ninguna |
| `src/task_repository.py` | 9/9 | No aplica | Contrato | Ninguna |
| `src/notification_service.py` | 5/5 | No aplica | Contrato | Ninguna |

En estos archivos, las líneas ejecutables contabilizadas por coverage.py coinciden con sus sentencias. El módulo `__init__.py` contiene solamente documentación, por lo que no añade sentencias al denominador.

## Cálculo de funciones

El resumen de terminal de pytest-cov no tiene una columna de funciones. El JSON de la versión fijada de coverage.py sí contiene un objeto `functions` por archivo. Se cuentan las entradas con nombre y `summary.num_statements > 0`; se considera invocada una función cuando `summary.covered_lines > 0`.

El modelo aporta diez funciones: el reloj UTC, la normalización de fechas y ocho métodos explícitos. El servicio aporta diez métodos. Todas las funciones con cuerpo ejecutable fueron invocadas. No se cuentan el bloque de módulo con nombre vacío, los métodos generados por `dataclass` ni las declaraciones sin cuerpo de los contratos.

Para reproducir el conteo en PowerShell 7, después de generar `coverage.json`:

```powershell
$data = Get-Content .\coverage.json -Raw | ConvertFrom-Json -AsHashtable
foreach ($entry in $data['files'].GetEnumerator()) {
    $functions = @($entry.Value['functions'].GetEnumerator() | Where-Object {
        $_.Key -ne '' -and $_.Value['summary']['num_statements'] -gt 0
    })
    $called = @($functions | Where-Object { $_.Value['summary']['covered_lines'] -gt 0 })
    "{0}: {1}/{2} funciones" -f $entry.Key, $called.Count, $functions.Count
}
```

## Rutas y límites del alcance

No quedaron sentencias ni salidas de ramas sin ejecutar dentro del código medido. Se cubren validaciones inválidas, fechas iguales al presente, estados terminales, comparaciones de prioridad, ausencia de registros, títulos repetidos, filtros combinados y fallos de almacenamiento, correo y SMS.

Los métodos de `TaskRepository` y `NotificationService` son declaraciones `Protocol`. La configuración predeterminada de coverage.py excluye sus cuerpos declarados con `...`; no se añadieron pragmas de exclusión ni una configuración local para elevar el porcentaje. Las sentencias declarativas de esos módulos sí aparecen en el reporte. Este resultado no mide una base de datos, SMTP ni un proveedor real de SMS: esos adaptadores no forman parte de la entrega.

Una cobertura de ramas del 100% tampoco implica haber probado todas las combinaciones de condiciones o secuencias posibles. Por eso se añadieron comprobaciones de comportamiento, las 16 combinaciones de estados y pruebas independientes para cada filtro, además de mirar porcentajes.

## Estrategia de mejora observada

| Etapa ejecutada | Casos | Sentencias | Ramas |
| --- | --- | --- | --- |
| Modelo inicial completo | 52 | 81/81 | 26/26 |
| Creación, estados y notificaciones | 68 | 144/146 | 36/36 |
| Actualizaciones y filtros | 86 | 192/194 | 66/66 |
| Fallos, límites y regresiones finales | 124 | 196/196 | 66/66 |

Las dos líneas pendientes después de ampliar el servicio pertenecían al manejo del fallo de SMS. Se ejecutaron mediante `NotificationError`, verificando que el registro persistido se conserva y que queda un aviso en el log.

La inspección del reloj detectó otro problema que los porcentajes anteriores no revelaban: una tarea cargada podía usar un reloj diferente al del servicio. Primero fallaron dos pruebas de regresión; después se corrigió la revisión para evaluar el lote con una sola hora de referencia. Este cambio explica parte del aumento de sentencias del resultado final.

Como mejora futura, los adaptadores reales requerirían pruebas de contrato contra sus servicios de prueba. El siguiente paso útil sería comprobar persistencia, traducción de errores y entrega real, antes de aumentar el número de casos de forma indiscriminada.

## Evidencias visuales

Capturas pendientes de incorporación por el autor en `reports/screenshots/`:

- `test-execution.png`: suite completa aprobada.
- `coverage-summary.png`: tabla de terminal con los porcentajes.
- `coverage-html-report.png`: reporte HTML con el detalle de cobertura.

`htmlcov/`, `coverage.json` y `.coverage` se regeneran con el comando indicado y permanecen fuera de Git.
