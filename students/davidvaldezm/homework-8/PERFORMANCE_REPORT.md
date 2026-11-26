# Métricas de rendimiento de la interfaz (bonus C)

Cinco sesiones independientes de Selenium, Chrome for Testing 142.0.7444.61, Windows 11.
Misma URL de React documentada en el README. Datos completos en
[performance.json](reports/submitted/performance.json).

`python scripts/performance.py` abre un navegador limpio por muestra. Mide con `perf_counter`
la navegación hasta que el campo de creación está visible y tres operaciones con sincronización
contra el estado resultante. También obtiene `domContentLoadedEventEnd` de Navigation Timing.
La creación/cierre del proceso Chrome queda fuera de estas latencias de interacción.

| Métrica | Mediana | Mínimo | Máximo |
| --- | ---: | ---: | ---: |
| Navegar y esperar campo visible | 277.84 ms | 256.34 ms | 359.50 ms |
| Crear tarea y verificar lista | 132.60 ms | 129.39 ms | 150.87 ms |
| Completar y verificar checkbox | 221.41 ms | 220.10 ms | 247.71 ms |
| Eliminar y verificar ausencia | 419.34 ms | 406.30 ms | 431.80 ms |
| DOMContentLoaded desde inicio de navegación | 138.30 ms | 118.20 ms | 182.40 ms |

Eliminar incluye el movimiento del ratón para revelar el botón; no debe interpretarse como
tiempo de procesamiento interno de la aplicación. Las operaciones incluyen comunicaciones
WebDriver, renderizado y verificaciones, por lo que tampoco representan exclusivamente CPU React.
Navigation Timing mide otro intervalo y no se suma al tiempo de navegación de Selenium.

Cinco muestras permiten describir esta ejecución; no justifican percentiles de cola ni un SLA.
No se aplicaron umbrales arbitrarios a CI por variación de red o del runner. Estos datos miden
latencia de interfaz, no carga concurrente, throughput, tiempo de backend ni capacidad del servicio.
La comparación de suites Selenium/Playwright está en `COMPARISON_REPORT.md`.
