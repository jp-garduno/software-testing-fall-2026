## Ejercicio 04: Shipping Method Selector

### Requisitos (recordatorio)

Reglas de selección, aplicadas en orden de prioridad (la primera que aplica gana):

1. Very Heavy + Local/Regional → Freight únicamente
2. Very Heavy + National → Freight, o Ground si `cost_preference = lowest`
3. Very Heavy + International → No disponible
4. Overnight + International → No disponible
5. Overnight + (cualquier peso) + National/Local → Express
6. Lowest cost + Light + Local → Ground
7. Fastest + Light/Medium + Local/Regional → Express
8. International → Solo métodos internacionales
9. Default → Priority Mail

Deduccion: la regla 5 se extiende también a `Overnight + Regional` (no estaba explícito, pero es consistente con la intención de "entrega urgente = Express" salvo que ya aplique una regla de mayor prioridad como Very Heavy o International)

### Parte A — Tabla de decisión (22 reglas, orden de prioridad)

| Regla | Weight      | Destination   | Urgency    | Cost Pref | Acción resultante          |
| ----- | ----------- | ------------- | ---------- | --------- | ---------------------------- |
| R1    | Very Heavy  | International | -          | -         | **No disponible**            |
| R2    | Very Heavy  | Local         | -          | -         | Freight                      |
| R3    | Very Heavy  | Regional      | -          | -         | Freight                      |
| R4    | Very Heavy  | National      | -          | Lowest    | Ground                       |
| R5    | Very Heavy  | National      | -          | Balanced/Fastest | Freight               |
| R6    | -           | International | Overnight  | -         | **No disponible**            |
| R7    | -           | International | Expedited  | -         | International Express        |
| R8    | -           | International | Standard   | -         | International Standard       |
| R9    | Light/Medium/Heavy | Local  | Overnight  | -         | Express                      |
| R10   | Light/Medium/Heavy | National | Overnight | -         | Express                     |
| R11   | Light/Medium/Heavy | Regional | Overnight | -         | Express (supuesto, ver nota)|
| R12   | Light       | Local         | Standard/Expedited | Lowest | Ground                  |
| R13   | Light       | Local         | Standard/Expedited | Fastest | Express                 |
| R14   | Light       | Regional      | Standard/Expedited | Fastest | Express                 |
| R15   | Medium      | Local         | Standard/Expedited | Fastest | Express                 |
| R16   | Medium      | Regional      | Standard/Expedited | Fastest | Express                 |
| R17   | Medium      | National      | Standard   | Balanced  | Priority Mail (default)      |
| R18   | Heavy       | Regional      | Standard   | Balanced  | Priority Mail (default)      |
| R19   | Light       | National      | Expedited  | Balanced  | Priority Mail (default)      |
| R20   | Heavy       | International | Standard   | -         | International Standard       |
| R21   | Heavy       | International | Overnight  | -         | **No disponible**            |
| R22   | Very Heavy  | Local         | Overnight  | Fastest   | Freight (R2 tiene prioridad sobre R9) |
