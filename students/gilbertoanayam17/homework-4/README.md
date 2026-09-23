# Homework 4: Black Box Testing: SecureBank System

## Description

Suite de pruebas de caja negra para SecureBank, un sistema de banca en línea con
tres tipos de cuenta, cuatro estados y reglas de negocio acopladas (límites
diarios acumulados, saldos mínimos y comisiones mensuales con exención).

El diseño aplica las cuatro técnicas del módulo —Equivalence Partitioning,
Boundary Value Analysis, Decision Tables y State Transition Testing— y está
implementado **dos veces**: JavaScript con Jest y Python con pytest, con los
mismos casos y los mismos IDs.

|                    | JavaScript | Python |
| ------------------ | ---------- | ------ |
| Pruebas            | 28         | 28     |
| Cobertura de línea | 84.8 %     | 87.7 % |
| Cobertura de rama  | 79.8 %     | —      |

## Prerequisites

- Node.js 20+ (probado con Node 24)
- Python 3.11+ (probado con Python 3.14)

## Installation

```bash
# JavaScript
npm install

# Python
pip install -r requirements.txt
```

## Running Tests

```bash
# JavaScript
npm test                    # solo las pruebas
npm test -- --coverage      # con cobertura

# Python
pytest -v                                              # solo las pruebas
pytest -v --cov=src --cov-report=term --cov-report=html   # con cobertura
```

## Viewing the Coverage Report

```bash
# JavaScript: abre coverage/index.html
npm test -- --coverage

# Python: abre htmlcov/index.html
pytest --cov=src --cov-report=html
```

## Project Structure

```
homework-4/
├── README.md                    # este archivo
├── design/
│   └── test-design-document.md  # Parte 1: EP, BVA, tablas de decisión, estados
├── src/
│   ├── bankingSystem.js         # sistema bajo prueba (JavaScript)
│   └── banking_system.py        # sistema bajo prueba (Python)
├── tests/
│   ├── equivalencePartitioning.test.js   │  test_equivalence_partitioning.py
│   ├── boundaryValues.test.js            │  test_boundary_values.py
│   ├── decisionTables.test.js            │  test_decision_tables.py
│   ├── stateTransitions.test.js          │  test_state_transitions.py
│   └── conftest.py                       # fixtures compartidas (pytest)
├── reports/
│   ├── test-execution-report.md # Parte 3: resultados y análisis de cobertura
│   ├── analysis-report.md       # Parte 4: análisis de las técnicas
│   ├── reflection.md            # reflexión de entrega
│   └── screenshots/
├── jest.config.js               # configuración de Jest
├── pytest.ini                   # configuración de pytest
├── .pylintrc                    # configuración de pylint (justificada en el archivo)
├── package.json
└── requirements.txt
```

## What Was Tested

| Técnica                  | Pruebas (por lenguaje) | Alcance                                                                                                                 |
| ------------------------ | ---------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Equivalence Partitioning | 9                      | Una representante por partición de las 5 entradas: monto, tipo de cuenta, saldo inicial, beneficiario y rango de fechas |
| Boundary Value Analysis  | 7                      | Fronteras del límite diario, del saldo mínimo y del límite acumulado                                                    |
| Decision Tables          | 7                      | Las acciones distintas de las 3 tablas diseñadas                                                                        |
| State Transition         | 5                      | Las transiciones principales y el estado terminal                                                                       |
| **Total**                | **28**                 | 56 pruebas contando ambos lenguajes                                                                                     |

El documento de diseño tiene las tablas completas; en `tests/` implementé un
subconjunto representativo, eligiendo una prueba por cada resultado distinto. El
mínimo que pedía la tarea eran 20.

### Trazabilidad

Los IDs del documento de diseño (`EP-TA1`, `BV4-1`, `DT1-R5`, `ST12`…) aparecen en
el nombre de cada prueba, así que al correr `npm test` o `pytest -v` se ve de qué
fila del diseño viene cada una.

## Notes

- **Manejo del dinero**: los montos son números en dólares y redondeo a dos
  decimales antes de comparar. Lo agregué porque la prueba BV4-1 fallaba:
  `4999.99 + 0.01` da `5000.000000000001` y se pasaba del límite diario. Ese fue
  el único error que encontré (ver `reports/test-execution-report.md`).
- **Supuestos**: hay tres cosas que la especificación no dice y tuve que decidir
  yo. Están en la sección 0 del documento de diseño.
- **Linting**: el `.eslintrc.json` es la configuración mínima para Node y Jest.
  En `banking_system.py` hay un `pylint: disable` en la clase, porque guarda 8
  atributos y el límite por defecto son 7; está comentado ahí mismo.

## Author

Gilberto Anaya Mercado
