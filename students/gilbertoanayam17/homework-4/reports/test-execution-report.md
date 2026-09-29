# Test Execution Report

**Date**: 2026-09-23

## Test Execution Summary

Implementé la suite en los dos lenguajes, con los mismos casos en ambos.

|                | JavaScript (Jest) | Python (pytest)     |
| -------------- | ----------------- | ------------------- |
| Test Framework | Jest 29.7         | pytest + pytest-cov |
| Total Tests    | 28                | 28                  |
| Passed         | 28                | 28                  |
| Failed         | 0                 | 0                   |
| Skipped        | 0                 | 0                   |
| Duration       | 0.72 s            | 0.09 s              |

En total son 56 pruebas contando los dos lenguajes.

## Coverage Summary

|                   | JavaScript | Python                   |
| ----------------- | ---------- | ------------------------ |
| Line Coverage     | 84.8 %     | 87.7 %                   |
| Branch Coverage   | 79.8 %     | no la reporta pytest-cov |
| Function Coverage | 95.8 %     | —                        |

Comandos que usé:

```bash
npm test -- --coverage
pytest -v --cov=src --cov-report=term --cov-report=html
```

## Results by Technique

### Equivalence Partitioning (9 tests)

- ✅ EP-TA1: monto válido dentro del límite y del saldo
- ✅ EP-TA2: monto de cero
- ✅ EP-TA4: monto sobre el límite diario
- ✅ EP-TA6: monto no numérico
- ✅ EP-AT1..EP-AT3: cada tipo de cuenta aplica su límite y mínimo
- ✅ EP-AT4: tipo de cuenta desconocido
- ✅ EP-AB2: saldo inicial bajo el mínimo abre la cuenta Suspendida
- ✅ EP-PY2: beneficiario no registrado
- ✅ EP-DR1: rango de fechas válido y exportación a CSV

**Defects Found**: ninguno. Lo que sí me pasó fue que al hacer la tabla de
particiones del saldo inicial me di cuenta de que la especificación no dice qué
pasa si abres una cuenta Savings con $50, o sea por debajo del mínimo. Tuve que
decidirlo yo y lo anoté como supuesto.

### Boundary Value Analysis (7 tests)

- ✅ BV1-1: $0.00, bajo el mínimo
- ✅ BV1-2: $0.01, mínimo válido
- ✅ BV1-4: $5,000.00, exactamente en el límite
- ✅ BV1-5: $5,000.01, un centavo sobre el límite
- ✅ BV3-2: el saldo queda exactamente en el mínimo
- ✅ BV3-3: el saldo queda un centavo bajo el mínimo
- ✅ BV4-1: dos transferencias que suman exactamente el límite

**Defects Found**: **uno**. BV4-1 falló la primera vez que lo corrí. La prueba
transfiere $4,999.99 y luego $0.01, que suman justo el límite diario de $5,000 y
deberían pasar las dos. La segunda se rechazaba. Resulta que en punto flotante
`4999.99 + 0.01` da `5000.000000000001`, que es mayor que 5000. Lo arreglé
redondeando a dos decimales antes de comparar. Nunca lo habría encontrado con un
valor de en medio como $500.

### Decision Tables (7 tests)

- ✅ DT1-R1: acepta movimientos, dentro del límite y con fondos
- ✅ DT1-R2: sin fondos
- ✅ DT1-R3: sobre el límite diario
- ✅ DT1-R5: cuenta congelada
- ✅ DT2-R2: Savings paga la comisión de $5
- ✅ DT2-R3: Savings sin fondos para la comisión queda suspendida
- ✅ DT3-R6: pago con fecha futura se agenda

**Defects Found**: ninguno, pero armar DT1 me costó porque no tenía claro qué
error devolver cuando fallan dos condiciones a la vez, por ejemplo si no hay
fondos _y_ además se pasa del límite. Una prueba solo puede verificar un error, así
que definí un orden (estado, monto, límite, fondos) y lo escribí en el documento
de diseño.

### State Transitions (5 tests)

- ✅ ST1: Active → Suspended al caer bajo el mínimo
- ✅ ST2: Suspended → Active con un depósito
- ✅ ST3: Active → Frozen y de vuelta a Active
- ✅ ST5: Active → Closed
- ✅ ST12: Closed rechaza cualquier evento

**Defects Found**: ninguno.

## Screenshots

| Archivo                                  | Contenido                          |
| ---------------------------------------- | ---------------------------------- |
| `screenshots/test-results-jest.png`      | Salida de `npm test -- --coverage` |
| `screenshots/test-results-pytest.png`    | Salida de `pytest -v --cov=src`    |
| `screenshots/coverage-report-jest.png`   | Reporte HTML de Jest               |
| `screenshots/coverage-report-pytest.png` | Reporte HTML de pytest             |

## Coverage Analysis

### Qué quedó cubierto

Alrededor del 85-88 % de las líneas. Lo que sí está probado es el camino
principal del sistema: las cuatro validaciones de una transferencia (estado,
monto, límite diario y fondos), el cobro de la comisión mensual con y sin fondos,
el filtrado del historial y las transiciones de estado principales.

### Qué no quedó cubierto y por qué

Implementé un subconjunto del diseño, no todas las filas de las tablas, porque la
tarea pide mínimo 20 pruebas y me pareció mejor elegir las representativas de cada
partición. Lo que quedó sin ejecutar es:

- Algunas ramas de `payBill`: el pago inmediato, el monto inválido y el caso de
  fondos insuficientes. Solo probé el pago agendado y el beneficiario inválido.
- La exención de la comisión mensual cuando el saldo supera el umbral.
- Los montos por debajo de $0.01, que el sistema rechaza pero no probé.
- `resetDailyLimit`, que simula el corte de medianoche.

No es código muerto, simplemente no alcancé a probarlo. Si tuviera que subir la
cobertura, empezaría por `payBill`, que es la función con más ramas sin probar.

### Cómo difiere por técnica

No medí la cobertura de cada técnica por separado, pero al ver qué líneas quedaron
sin marcar sí se nota algo: las pruebas de estado son las únicas que entran a
`freeze`, `unfreeze` y `close`, y las de BVA son las únicas que llegan al límite
diario acumulado. Las de EP y las de tablas de decisión se solapan bastante, porque
las dos entran por `transfer`. Ninguna técnica sola hubiera cubierto el sistema.
