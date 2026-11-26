# Análisis de cobertura — TaskFlow

## Resumen de ejecución

Comando ejecutado el 19 de octubre de 2026:

```powershell
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html:htmlcov --cov-report=xml:coverage.xml
```

Resultado: **48 passed in 1.55s**. El informe HTML se genera en `htmlcov/index.html`; el workflow de CI lo conserva como artefacto descargable para no versionar archivos derivados.

## Cobertura global

| Métrica | Umbral | Alcanzado | Estado |
| --- | ---: | ---: | --- |
| Sentencias | >85% | 100% | ✅ |
| Ramas | >80% | 99% | ✅ |
| Funciones | >90% | 100% | ✅ |
| Líneas | >85% | 100% | ✅ |

## Cobertura por archivo

| Archivo | Sentencias | Ramas | Líneas |
| --- | ---: | ---: | ---: |
| `src/task.py` | 100% | 99% | 100% |
| `src/task_service.py` | 100% | 99% | 100% |
| `src/task_repository.py` | 100% | 100% | 100% |
| `src/notification_service.py` | 100% | 100% | 100% |
| **Total** | **100%** | **99%** | **100%** |

Las dos clases de frontera tienen métodos abstractos marcados como contrato sin cobertura (`pragma: no cover`): no poseen una implementación que se deba ejecutar. Se prueban indirectamente con `Mock(spec=TaskRepository)` y `Mock(spec=NotificationService)`, lo que evita que el servicio invoque métodos inexistentes.

## Ramas parcialmente contadas

No hay líneas sin ejecutar. Coverage.py marca dos ramas parciales: la salida temprana de las condiciones compuestas de `Task.update_details` y `TaskService.update_task`. Son efectos de evaluación de cortocircuito: una prueba puede alcanzar el mismo resultado semántico sin recorrer cada combinación interna de valores opcionales. Las pruebas cubren tanto actualizar campos como no modificar los no proporcionados, y cubren título duplicado, mismo título y ausencia de título. Por ello el riesgo residual es despreciable y las métricas superan holgadamente el objetivo.

## Estrategia aplicada

1. Se identificaron las decisiones del modelo: validación, transición, archivado, vencimiento y comparación de prioridad.
2. Se añadieron valores frontera: longitudes 0/2/3/100/101, fecha pasada/actual/futura y cada estado del ciclo.
3. Se diseñaron flujos de servicio positivos y negativos: creación, avance completo, archivado, edición, búsqueda y vencimiento.
4. Se inyectaron mocks para simular duplicados, tareas ausentes, fallo de base de datos y fallos de correo/SMS sin dependencias reales.
5. La ejecución de cobertura guió los casos finales hasta no dejar sentencias ni líneas descubiertas.

Los reportes HTML y XML se regeneran reproduciblemente con el comando anterior y CI los adjunta a cada ejecución.
