<!--
Diseño: parte 1 (Tarea 4 - SecureBank)
Requisitos:
- Tablas EP para al menos 5 entradas con particiones válidas/inválidas
- Tablas BVA para al menos 5 límites con 4-6 valores de prueba cada uno
- Al menos 3 tablas de decisión con todas las reglas cubiertas
- Diagrama y tabla de transición de estados completos
- Al menos 8 casos de prueba de transición de estado

-->

## Equivalence Partitioning

<!-- Partición de equivalencia -->

### Input: Transfer Amount

<!-- Monto de la transferencia -->

| Partition ID | Description                        | Type     | Representative Value | Expected Result                   |
| ------------ | ---------------------------------- | -------- | -------------------- | --------------------------------- |
| EP1          | Monto válido dentro de los límites | Válido   | $500                 | La transferencia se realiza       |
| EP2          | Monto cero                         | Inválido | $0                   | Error: el monto debe ser positivo |
| EP3          | Monto negativo                     | Inválido | -$100                | Error: el monto debe ser positivo |
| EP4          | Monto excede el límite diario      | Inválido | $100,000             | Error: supera el límite diario    |
| EP5          | Monto excede el saldo disponible   | Inválido | Saldo + $1           | Error: fondos insuficientes       |

### Input: Account Type

<!-- Tipo de cuenta -->

| Partition ID | Description                  | Type     | Representative Value | Expected Result                         |
| ------------ | ---------------------------- | -------- | -------------------- | --------------------------------------- |
| EP6          | Tipo de cuenta existente     | Válido   | Ahorro               | Se acepta: cuenta de ahorro             |
| EP7          | Tipo de cuenta existente     | Válido   | Estándar             | Se acepta: cuenta corriente             |
| EP8          | Tipo de cuenta existente     | Válido   | Premium              | Se acepta: cuenta premium               |
| EP9          | Tipo de cuenta no existente  | Inválido | Otro                 | Error: tipo de cuenta no válido         |
| EP10         | Tipo de cuenta que no existe | Inválido | Business             | Error: tipo de cuenta no válido         |
| EP11         | Tipo de cuenta vacío o nulo  | Inválido | "" (vacío)           | Error: el tipo de cuenta es obligatorio |

### Input: Account Balance

<!-- Saldo de la cuenta (el mínimo depende del tipo de cuenta) -->

| Partition ID | Description                                  | Type     | Representative Value | Expected Result                                     |
| ------------ | -------------------------------------------- | -------- | -------------------- | --------------------------------------------------- |
| EP12         | Ahorro: saldo mayor o igual al mínimo ($100) | Válido   | $500                 | La cuenta se mantiene Active                        |
| EP13         | Estándar: saldo negativo                     | Inválido | -$50                 | Error: no se permite saldo negativo                 |
| EP14         | Estándar: saldo mayor o igual a $0           | Válido   | $250                 | La cuenta se mantiene Active                        |
| EP15         | Premium: saldo menor al mínimo de $10,000    | Inválido | $5,000               | La cuenta pasa a Suspended (se muestra advertencia) |
| EP16         | Premium: saldo mayor o igual a $10,000       | Válido   | $15,000              | La cuenta se mantiene Active                        |
| EP17         | Ahorro: saldo menor al mínimo de $100        | Inválido | $50                  | La cuenta pasa a Suspended (se muestra advertencia) |

### Input: Payee Information for Bill Payment

<!-- Información del beneficiario para el pago de facturas -->

| Partition ID | Description                                         | Type     | Representative Value                   | Expected Result                             |
| ------------ | --------------------------------------------------- | -------- | -------------------------------------- | ------------------------------------------- |
| EP17         | Beneficiario válido, monto > $0, fondos suficientes | Válido   | acceso: tue , monto: $100, saldo: $500 | El pago se realiza                          |
| EP18         | Beneficiario que no existe                          | Inválido | acceso: false                          | Error: beneficiario no válido               |
| EP19         | Beneficiario vacío                                  | Inválido | acceso: false                          | Error: el beneficiario es obligatorio       |
| EP20         | Monto menor o igual a cero                          | Inválido | acceso: tue, monto: $0                 | Error: el monto debe ser mayor a $0         |
| EP21         | Fondos insuficientes (monto mayor al saldo)         | Inválido | monto: $600, saldo: $500               | Error: fondos insuficientes                 |
| EP22         | Pago programado con fecha futura                    | Válido   | hoy + 7 días                           | El pago queda programado                    |
| EP23         | Pago programado con fecha pasada                    | Inválido | hoy - 1 día                            | Error: la fecha no puede estar en el pasado |

### Input: Date Range for Transaction History

<!-- Rango de fechas para el historial de transacciones -->

| Partition ID | Description                             | Type     | Representative Value             | Expected Result                                              |
| ------------ | --------------------------------------- | -------- | -------------------------------- | ------------------------------------------------------------ |
| EP24         | Rango en el pasado con inicio < fin     | Válido   | inicio = hoy - 30, fin = hoy - 1 | Se muestran las transacciones de ese rango                   |
| EP25         | Rango de un solo día (inicio = fin)     | Válido   | inicio = fin = hoy               | Se muestran las transacciones de ese día                     |
| EP26         | Fecha de inicio mayor a la fecha de fin | Inválido | inicio = hoy, fin = hoy - 5      | Error: la fecha de inicio debe ser menor o igual a la de fin |
| EP27         | Fecha de inicio en el futuro            | Inválido | inicio = hoy + 1                 | Error: la fecha de inicio no puede ser futura                |
| EP28         | Fecha vacía o con formato inválido      | Inválido | "" o "31-13-2026"                | Error: formato de fecha no válido                            |

## Boundary Value Analysis

<!-- Análisis de valor límite -->

### Boundary: Transfer Amount (Checking Account - $5,000 limit)

<!-- Límite: monto de la transferencia (cuenta Estándar - límite de $5,000) -->

| Test ID | Boundary                    | Test Value | Expected Result                   |
| ------- | --------------------------- | ---------- | --------------------------------- |
| BV1     | Por debajo del mínimo       | $0.00      | Error: el monto debe ser positivo |
| BV2     | Mínimo válido               | $0.01      | La transferencia se realiza       |
| BV3     | Justo por debajo del límite | $4,999.99  | La transferencia se realiza       |
| BV4     | En el límite                | $5,000.00  | La transferencia se realiza       |
| BV5     | Justo por encima del límite | $5,000.01  | Error: supera el límite diario    |
| BV6     | Muy por encima del límite   | $10,000.00 | Error: supera el límite diario    |

### Boundary: Transfer Amount (Savings Account - $2,000 limit)

<!-- Límite: monto de la transferencia (cuenta Ahorro - límite de $2,000) -->

| Test ID | Boundary                    | Test Value | Expected Result                   |
| ------- | --------------------------- | ---------- | --------------------------------- |
| BV7     | Por debajo del mínimo       | $0.00      | Error: el monto debe ser positivo |
| BV8     | Mínimo válido               | $0.01      | La transferencia se realiza       |
| BV9     | Justo por debajo del límite | $1,999.99  | La transferencia se realiza       |
| BV10    | En el límite                | $2,000.00  | La transferencia se realiza       |
| BV11    | Justo por encima del límite | $2,000.01  | Error: supera el límite diario    |

### Boundary: Transfer Amount (Premium Account - $50,000 limit)

<!-- Límite: monto de la transferencia (cuenta Premium - límite de $50,000) -->

| Test ID | Boundary                    | Test Value | Expected Result                |
| ------- | --------------------------- | ---------- | ------------------------------ |
| BV12    | Mínimo válido               | $0.01      | La transferencia se realiza    |
| BV13    | Justo por debajo del límite | $49,999.99 | La transferencia se realiza    |
| BV14    | En el límite                | $50,000.00 | La transferencia se realiza    |
| BV15    | Justo por encima del límite | $50,000.01 | Error: supera el límite diario |

### Boundary: Account Balance vs Minimum (Savings - $100 minimum)

<!-- Límite: saldo de la cuenta vs mínimo (Ahorro - mínimo de $100) -->

| Test ID | Boundary                    | Test Value | Expected Result              |
| ------- | --------------------------- | ---------- | ---------------------------- |
| BV16    | Saldo mínimo posible        | $0.00      | La cuenta pasa a Suspended   |
| BV17    | Justo por debajo del mínimo | $99.99     | La cuenta pasa a Suspended   |
| BV18    | En el mínimo                | $100.00    | La cuenta se mantiene Active |
| BV19    | Justo por encima del mínimo | $100.01    | La cuenta se mantiene Active |

### Boundary: Account Balance vs Minimum (Checking - $0 minimum)

<!-- Límite: saldo de la cuenta vs mínimo (Estándar - mínimo de $0) -->

| Test ID | Boundary                    | Test Value | Expected Result                     |
| ------- | --------------------------- | ---------- | ----------------------------------- |
| BV20    | Muy por debajo del mínimo   | -$100.00   | Error: no se permite saldo negativo |
| BV21    | Justo por debajo del mínimo | -$0.01     | Error: no se permite saldo negativo |
| BV22    | En el mínimo                | $0.00      | La cuenta se mantiene Active        |
| BV23    | Justo por encima del mínimo | $0.01      | La cuenta se mantiene Active        |

### Boundary: Account Balance vs Minimum (Premium - $10,000 minimum)

<!-- Límite: saldo de la cuenta vs mínimo (Premium - mínimo de $10,000) -->

| Test ID | Boundary                    | Test Value | Expected Result              |
| ------- | --------------------------- | ---------- | ---------------------------- |
| BV24    | Muy por debajo del mínimo   | $5,000.00  | La cuenta pasa a Suspended   |
| BV25    | Justo por debajo del mínimo | $9,999.99  | La cuenta pasa a Suspended   |
| BV26    | En el mínimo                | $10,000.00 | La cuenta se mantiene Active |
| BV27    | Justo por encima del mínimo | $10,000.01 | La cuenta se mantiene Active |

### Boundary: Monthly Fee Waiver Threshold (Savings - waived if balance > $1,000)

<!-- Límite: exención de cuota mensual (Ahorro - se exonera si el saldo > $1,000) -->

| Test ID | Boundary                            | Test Value | Expected Result         |
| ------- | ----------------------------------- | ---------- | ----------------------- |
| BV28    | Justo por debajo del umbral         | $999.99    | Se cobra la cuota de $5 |
| BV29    | En el umbral (no es mayor a $1,000) | $1,000.00  | Se cobra la cuota de $5 |
| BV30    | Justo por encima del umbral         | $1,000.01  | Cuota exonerada ($0)    |
| BV31    | Muy por encima del umbral           | $2,000.00  | Cuota exonerada ($0)    |

### Boundary: Monthly Fee Waiver Threshold (Checking - waived if balance > $5,000)

<!-- Límite: exención de cuota mensual (Estándar - se exonera si el saldo > $5,000) -->

| Test ID | Boundary                            | Test Value | Expected Result          |
| ------- | ----------------------------------- | ---------- | ------------------------ |
| BV32    | Justo por debajo del umbral         | $4,999.99  | Se cobra la cuota de $10 |
| BV33    | En el umbral (no es mayor a $5,000) | $5,000.00  | Se cobra la cuota de $10 |
| BV34    | Justo por encima del umbral         | $5,000.01  | Cuota exonerada ($0)     |
| BV35    | Muy por encima del umbral           | $10,000.00 | Cuota exonerada ($0)     |

### Boundary: Daily Limit (cumulative amount sent today)

<!-- Límite: límite diario (monto acumulado enviado hoy) -->

| Test ID | Account  | Already Sent Today | New Transfer | Total      | Expected Result                |
| ------- | -------- | ------------------ | ------------ | ---------- | ------------------------------ |
| BV36    | Ahorro   | $1,500.00          | $500.00      | $2,000.00  | La transferencia se realiza    |
| BV37    | Ahorro   | $1,500.00          | $500.01      | $2,000.01  | Error: supera el límite diario |
| BV38    | Estándar | $4,000.00          | $1,000.00    | $5,000.00  | La transferencia se realiza    |
| BV39    | Estándar | $4,000.00          | $1,000.01    | $5,000.01  | Error: supera el límite diario |
| BV40    | Premium  | $40,000.00         | $10,000.00   | $50,000.00 | La transferencia se realiza    |
| BV41    | Premium  | $40,000.00         | $10,000.01   | $50,000.01 | Error: supera el límite diario |

## Decision Tables

<!-- Tablas de decisión -->

### Decision Table 1: Transfer Validation

<!-- Tabla de decisión 1: validación de transferencias -->

| Condition                    | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
| ---------------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| ¿fondos suficientes?         | Y      | Y      | Y      | Y      | N      | N      | N      | N      |
| ¿Dentro del límite diario?   | Y      | Y      | N      | N      | Y      | Y      | N      | N      |
| ¿La cuenta está activa?      | Y      | N      | Y      | N      | Y      | N      | Y      | N      |
| **Acción**                   |
| La transferencia tiene éxito | X      |        |        |        |        |        |        |        |
| Error: Fondos insuficientes  |        |        |        |        | X      | X      | X      | X      |
| Error: excede el límite      |        |        | X      |        |        |        | X      |        |
| Error: Cuenta congelada      |        | X      |        | X      |        | X      |        | X      |

### Decision Table 2: Monthly Fee Processing

<!-- Tabla de decisión 2: procesamiento de la cuota mensual -->

| Condition                    | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5   | Rule 6   | Rule 7   | Rule 8   | Rule 9  | Rule 10 | Rule 11 | Rule 12 |
| ---------------------------- | ------ | ------ | ------ | ------ | -------- | -------- | -------- | -------- | ------- | ------- | ------- | ------- |
| ¿Tipo de cuenta?             | Ahorro | Ahorro | Ahorro | Ahorro | Estándar | Estándar | Estándar | Estándar | Premium | Premium | Premium | Premium |
| ¿Mayor al limite minimo?     | Y      | Y      | N      | Y      | Y        | N        | Y        | Y        | N       | Y       | Y       | N       |
| ¿Mayor al limite de interes? | Y      | N      | N      | Y      | N        | N        | Y        | N        | N       | Y       | N       | N       |
| **Acción**                   |
| Cobrar                       |        | X      |        |        | X        |          |          | X        |         |         | X       |         |
| No cobrar                    | X      |        |        | X      |          |          | X        |          |         | X       |         |         |
| Suspendido                   |        |        | X      |        |          | X        |          |          | X       |         |         | X       |

### Decision Table 3: Bill Payment Validation

<!-- Tabla de decisión 3: validación del pago de facturas (u otra a tu elección) -->

| Condition            | R1  | R2  | R3  | R4  | R5  | R6  | R7  | R8  | R9  | R10 | R11 | R12 | R13 | R14 | R15 | R16 |
| -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ¿Cuenta activa?      | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | N   | N   | N   | N   | N   | N   | N   | N   |
| ¿Monto correcto?     | Y   | Y   | Y   | Y   | N   | N   | N   | N   | Y   | Y   | Y   | Y   | N   | N   | N   | N   |
| ¿Fondos suficientes? | Y   | Y   | N   | N   | Y   | Y   | N   | N   | Y   | Y   | N   | N   | Y   | Y   | N   | N   |
| ¿Fecha valida?       | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   |
| **Acción**           |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| Cobrar               | X   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| No cobrar            |     | X   | X   | X   | X   | X   | X   | X   | X   | X   | X   | X   | X   | X   | X   | X   |

## State Transition Testing

<!-- Pruebas de transición de estados -->

### State Transition Diagram

<!-- Diagrama de transición de estados -->

```
[Activo]        --(Balance < Minimum)-->   [Suspendido]
[Activo]        --(Freeze request)-->      [Congelado]
[Activo]        --(Close request)-->       [Cerrado]
[Suspendido]    --(Deposit restores)-->    [Activo]
[Suspendido]    --(Close request)-->       [Cerrado]
[Congelado]     --(Unfreeze approved)-->   [Activo]
[Congelado]     --(Close request)-->       [Cerrado]
```

<!--
Activo → Congelado: Por solicitud del cliente o detección de fraude
Activo → Suspendido: El saldo cae por debajo del mínimo
Suspendido → Activo: Equilibrio restablecido por encima del mínimo
Cualquier estado → Cerrado: A petición del cliente
-->

### State Transition Table

<!-- Tabla de transición de estados -->

| Current State | Event                              | Next State | Action/Output                      |
| ------------- | ---------------------------------- | ---------- | ---------------------------------- |
| Activo        | El saldo cae por debajo del mínimo | Suspendido | Enviar notificación de advertencia |
| Activo        | Solicitud de congelación           | Congelado  | Bloquear todas las transacciones   |
| Activo        | Cerrar solicitud                   | Cerrado    | Declaración final generada         |
| Suspendido    | El depósito restablece el saldo    | Activo     | Eliminar restricciones             |
| Suspendido    | Cerrar solicitud                   | Cerrado    | Declaración final generada         |
| Congelado     | Aprobado para descongelar          | Activo     | Restaurar el acceso completo       |
| Congelado     | Cerrar solicitud                   | Cerrado    | Declaración final generada         |
| Cerrado       | Cualquier evento                   | Cerrado    | Error: Cuenta cerrada no cambia    |

### State Transition Test Cases

<!-- Casos de prueba de transición de estados -->
<!-- TODO: al menos 8 casos (ST1..ST8+) -->

| ID  | Estado inicial | Estado final | Válido   | Descripción                                                                                         |
| --- | -------------- | ------------ | -------- | --------------------------------------------------------------------------------------------------- |
| ST1 | Activo         | Suspendido   | Válido   | Cuando el saldo baja del límite establecido, la cuenta se suspende.                                 |
| ST2 | Activo         | Congelado    | Válido   | Cuando se detecta actividad sospechosa o posible fraude.                                            |
| ST3 | Activo         | Cerrado      | Válido   | La cuenta puede cerrarse desde este estado.                                                         |
| ST4 | Suspendido     | Activo       | Válido   | Es posible reactivar la cuenta una vez que el saldo alcanza o supera el monto mínimo.               |
| ST5 | Suspendido     | Cerrado      | Válido   | La cuenta puede cerrarse desde este estado.                                                         |
| ST6 | Congelado      | Activo       | Válido   | Se puede reactivar la cuenta si se comprueba que no hubo fraude.                                    |
| ST7 | Congelado      | Cerrado      | Válido   | La cuenta puede cerrarse desde este estado.                                                         |
| ST8 | Cerrado        | Activo       | Inválido | No es posible salir del estado de cierre; equivale a un estado de pozo (o sumidero) en un autómata. |
