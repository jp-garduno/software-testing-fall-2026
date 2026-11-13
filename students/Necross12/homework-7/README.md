# Homework 7: Data-Driven Test Suite

Suite de pruebas data-driven para un sistema de pedidos e-commerce, hecha con **JavaScript + Jest**.

## Ejercicios extras (bonus)

- **A (generación de datos):** `test_data/generateOrders.js` crea 100 pedidos válidos con Faker en `test_data/100PruebasAlAzar.csv`.
- **C (validación de datos):** `test_data/validateTestData.js` + `test_data/runValidation.js` revisan los CSV y el JSON de clientes (campos requeridos, tipos, número de línea o de caso).

## Prerrequisitos

- Node.js 22+

## Instalación

```bash
npm install
```

## Comandos

```bash
npm test                  # correr todas las pruebas
npm run test:coverage     # pruebas con tabla de cobertura en la terminal
npm run test:docs         # genera el reporte HTML en coverage/index.html
npm run test:results      # guarda la salida detallada en test_results.txt
npm run test:validate     # valida los archivos de datos (CSV y JSON)
npm run test:generate     # regenera test_data/100PruebasAlAzar.csv con datos nuevos
```

Para abrir el reporte de cobertura desde la raíz:

```bash
# Windows
Start-Process coverage/index.html

# macOS
open coverage/index.html
```

## Cobertura

| Archivo                | Sentencias | Ramas  | Funciones | Líneas |
|------------------------|------------|--------|-----------|--------|
| **All files**          | 98.51%     | 98.03% | 100%      | 98.36% |
| `customerValidator.js` | 100%       | 100%   | 100%      | 100%   |
| `orderCalculator.js`   | 96.66%     | 96.07% | 100%      | 95.91% |

213 pruebas en 5 suites, todas pasan.

## Estructura del proyecto

```
homework-7/
├── coverage/
├── src/
│   ├── orderCalculator.js
│   └── customerValidator.js
├── tests/
│   ├── orderCalculator.test.js
│   ├── customerValidator.test.js
│   ├── orderTraditional.test.js
│   ├── orderDataDriven.test.js
│   └── integration.test.js
├── test_data/
│   ├── orderCalculations.csv
│   ├── 100PruebasAlAzar.csv
│   ├── customerValidation.json
│   ├── orderWorkflows.json
│   ├── generateOrders.js
│   ├── validateTestData.js
│   └── runValidation.js
├── README.md
├── COMPARISON_REPORT.md
├── TEST_DATA_SPEC.md
├── test_results.txt          (lo genera npm run test:results)
└── package.json
```

## Documentación

- [`TEST_DATA_SPEC.md`](TEST_DATA_SPEC.md): formato de los datos de prueba y reglas asumidas.
- [`COMPARISON_REPORT.md`](COMPARISON_REPORT.md): pruebas tradicionales vs. data-driven.

## Autor

Diego Orozco Mólgora - Software Testing Fall 2026
