# Homework 4: Black Box Testing - SecureBank System

## Description

Conjunto completo de pruebas de caja negra para un sistema de banca en línea, usando partición de equivalencia (EP), análisis de valor límite (BVA), tablas de decisión y transición de estados.

## Prerequisites

- Node.js 22+
- Jest (se instala con `npm install`)

## Installation

```bash
npm install
```

## Running Tests

```bash
# Todas las pruebas
npm test

# Con cobertura
npm run test:coverage
```

## Viewing the Coverage Report

Después de `npm run test:coverage`, abre `coverage/lcov-report/index.html` en el navegador.

## Project Structure

- `design/` - Documento de diseño de pruebas
- `src/` - Implementación de SecureBank (`bankingSystem.js`)
- `tests/` - Pruebas automatizadas (EP, BVA, tablas de decisión, transiciones)
- `reports/` - Reporte de ejecución, análisis y capturas

## What Was Tested

- Partición de equivalencia: 6 pruebas (tipo de cuenta)
- Valores límite: 7 pruebas (montos y límites diarios)
- Tablas de decisión: 5 pruebas (validación de transferencias)
- Transición de estados: 6 pruebas (ciclo de vida de la cuenta)
- **Total**: 24 pruebas

## Author

Diego Orozco Mólgora
