# Homework 4: Black Box Testing — SecureBank

Suite completa de pruebas de caja negra para un sistema de banca en línea. El
trabajo aplica particiones de equivalencia, análisis de valores frontera, tablas
de decisión y pruebas de transición de estado.

## Autor

Vittorio Catino — `vittorio.catino@iteso.mx`

## Requisitos

- Python 3.11 o posterior
- `pip`

## Instalación

Desde esta carpeta:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Ejecución

Todas las pruebas:

```bash
pytest -v
```

Pruebas con cobertura de líneas y ramas:

```bash
pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

El reporte HTML se abre desde `htmlcov/index.html`.

## Alcance

- Validación de transferencias por monto, saldo, límite diario y estado.
- Reglas particulares de cuentas Savings, Checking y Premium.
- Pagos de servicios y validación del beneficiario.
- Cobro y exención de cuotas mensuales.
- Rangos de fechas para el historial de movimientos.
- Transiciones entre Active, Frozen, Suspended y Closed.

## Estructura

- `design/`: diseño sistemático de las cuatro técnicas.
- `src/`: modelo observable de SecureBank.
- `tests/`: pruebas automatizadas organizadas por técnica.
- `reports/`: resultados, análisis y capturas de ejecución.

Los supuestos adoptados para resolver ambigüedades de la especificación están
documentados al inicio del diseño de pruebas.
