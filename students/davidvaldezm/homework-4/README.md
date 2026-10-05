# Homework 4: SecureBank - pruebas de caja negra

**Autor:** David Valdez (`davidvaldezm`). Implementación: Python 3.11+ y pytest.

Suite de 125 casos independientes para particiones de equivalencia (38), valores límite (37), tablas de decisión (38) y transiciones de estado (12). Sistema de referencia en memoria construido a partir del enunciado; no se conecta a cuentas reales.

## Instalación y ejecución

Desde `students/davidvaldezm/homework-4`:

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html --cov-report=json:reports/coverage.json --junitxml=reports/results.xml
```

Abrir `htmlcov/index.html` para la cobertura interactiva. `pytest.ini` configura los imports y el descubrimiento. No hace falta red, base de datos ni variables secretas para ejecutar pruebas.

```sh
python -m pip install pylint==4.0.9 black==26.5.1
python -m pylint src tests
python -m black --check src tests
python -m pytest tests/test_boundary_values.py -v
```

## Documentación y evidencia

- [Diseño y trazabilidad](design/test-design-document.md): contrato, ocho fronteras, tres tablas de decisión y diagrama Mermaid.
- [Reporte de ejecución](reports/test-execution-report.md): resultados reales, cobertura por técnica, mutaciones y capturas.
- [Análisis comparativo](reports/analysis-report.md): 500-700 palabras.
- [Reflexión](reports/reflection.md): 200-300 palabras; borrador técnico para revisión del autor.
- `reports/results.xml`, `reports/test-output.txt`, `reports/coverage.json`: evidencia de ejecución.
- `reports/mutations.json`: cinco fallos sembrados en copias temporales; el código entregado no contiene esas mutaciones.
- `reports/pdf/`: exportaciones imprimibles.
- `src/`: modelo de referencia con Decimal y reloj inyectable.
- `tests/`: cuatro archivos de técnicas y fixtures independientes.

## Automatización

El workflow `.github/workflows/davidvaldezm-homework-4.yml` ejecuta pytest, cobertura de ramas, Black y Pylint en Python 3.11 y 3.12. Publica reportes como artefactos y exige cobertura >=90%. El workflow oficial del curso calcula la calificación al añadir `homework` al PR. No se modifica su fórmula ni sus verificaciones.

La configuración Pylint conserva todas las categorías de diagnóstico; ajusta el máximo de atributos para el agregado bancario y el máximo de argumentos para las tablas parametrizadas. La única supresión localizada permite que el reloj de pruebas tenga un solo método público.

## Alcance y limitaciones

125 casos pasan; el reporte incluye métricas exactas. La cobertura de código no equivale a cobertura de requisitos completa. No se implementan autenticación, base de datos, concurrencia, liquidación externa ni ejecución automática en segundo plano. Los pagos programados se procesan mediante `process_scheduled`. Los supuestos sobre igualdad de umbrales, UTC, errores y estados se declaran en el diseño.

Bonus incorporado: CI y diagrama visual. Se eligió una sola implementación Python para mantener un contrato claro y comprobable; no se solicita el bonus de doble lenguaje.

La etiqueta de esta entrega es `hw4-final-davidvaldezm`: `hw4-final` ya existía en el repositorio compartido y se conserva intacta.

En Windows, el lanzador general de pre-commit se bloqueó al ejecutar sus wrappers `.exe`. Se ejecutaron directamente los módulos de validación de archivos, JSON, YAML, conflictos, claves privadas y finales de línea, además de Black, Pylint y Prettier. No se afirma que el comando general `pre-commit run` haya completado.
