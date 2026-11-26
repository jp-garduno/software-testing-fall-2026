# Boundary Tables — Sistema de Categorización de Productos (E-commerce)

## 1. Tabla de Límites — Rangos de Precio

| Boundary (Límite)              | Valor      | Categoría Esperada |
|---------------------------------|------------|---------------------|
| Debajo del mínimo               | $0.00      | Inválido            |
| Valor negativo                  | -$0.01     | Inválido            |
| En el mínimo                    | $0.01      | Budget              |
| Justo antes del primer límite   | $10.00     | Budget              |
| En el primer límite             | $10.01     | Standard            |
| Justo después del primer límite | $10.02     | Standard            |
| Justo antes del segundo límite  | $50.00     | Standard            |
| En el segundo límite            | $50.01     | Premium             |
| Justo después del segundo límite| $50.02     | Premium             |
| Justo antes del tercer límite   | $200.00    | Premium             |
| En el tercer límite             | $200.01    | Luxury              |
| Justo después del tercer límite | $200.02    | Luxury              |
| Valor muy alto                  | $9,999.99  | Luxury              |

---

## 2. Tabla de Límites — Cantidad (Quantity Limits) por Categoría

### 2.1 Budget (rango permitido: 1–100)

| Boundary                | Cantidad | Resultado Esperado |
|--------------------------|----------|----------------------|
| Debajo del mínimo        | 0        | Inválido             |
| En el mínimo             | 1        | Válido               |
| Justo sobre el mínimo    | 2        | Válido               |
| Justo bajo el máximo     | 99       | Válido               |
| En el máximo             | 100      | Válido               |
| Sobre el máximo          | 101      | Inválido             |

### 2.2 Standard (rango permitido: 1–50)

| Boundary                | Cantidad | Resultado Esperado |
|--------------------------|----------|----------------------|
| Debajo del mínimo        | 0        | Inválido             |
| En el mínimo             | 1        | Válido               |
| Justo sobre el mínimo    | 2        | Válido               |
| Justo bajo el máximo     | 49       | Válido               |
| En el máximo             | 50       | Válido               |
| Sobre el máximo          | 51       | Inválido             |

### 2.3 Premium (rango permitido: 1–20)

| Boundary                | Cantidad | Resultado Esperado |
|--------------------------|----------|----------------------|
| Debajo del mínimo        | 0        | Inválido             |
| En el mínimo             | 1        | Válido               |
| Justo sobre el mínimo    | 2        | Válido               |
| Justo bajo el máximo     | 19       | Válido               |
| En el máximo             | 20       | Válido               |
| Sobre el máximo          | 21       | Inválido             |

### 2.4 Luxury (rango permitido: 1–10)

| Boundary                | Cantidad | Resultado Esperado |
|--------------------------|----------|----------------------|
| Debajo del mínimo        | 0        | Inválido             |
| En el mínimo             | 1        | Válido               |
| Justo sobre el mínimo    | 2        | Válido               |
| Justo bajo el máximo     | 9        | Válido               |
| En el máximo             | 10       | Válido               |
| Sobre el máximo          | 11       | Inválido             |

---

## 3. Tabla de Límites — Umbrales de Descuento por Categoría

### 3.1 Budget — 5% de descuento si cantidad ≥ 10

| Boundary                  | Cantidad | Descuento Aplicado |
|-----------------------------|----------|----------------------|
| Justo antes del umbral      | 9        | No (0%)              |
| En el umbral                | 10       | Sí (5%)               |
| Justo después del umbral    | 11       | Sí (5%)               |

### 3.2 Standard — 10% de descuento si cantidad ≥ 5

| Boundary                  | Cantidad | Descuento Aplicado |
|-----------------------------|----------|----------------------|
| Justo antes del umbral      | 4        | No (0%)              |
| En el umbral                | 5        | Sí (10%)              |
| Justo después del umbral    | 6        | Sí (10%)              |

### 3.3 Premium — 15% de descuento si cantidad ≥ 3

| Boundary                  | Cantidad | Descuento Aplicado |
|-----------------------------|----------|----------------------|
| Justo antes del umbral      | 2        | No (0%)              |
| En el umbral                | 3        | Sí (15%)              |
| Justo después del umbral    | 4        | Sí (15%)              |

### 3.4 Luxury — 20% de descuento si cantidad ≥ 2

| Boundary                  | Cantidad | Descuento Aplicado |
|-----------------------------|----------|----------------------|
| Justo antes del umbral      | 1        | No (0%)              |
| En el umbral                | 2        | Sí (20%)              |
| Justo después del umbral    | 3        | Sí (20%)              |

> **Nota:** Como el umbral mínimo de cantidad para cada categoría es 1, y el umbral de descuento de Luxury es 2, el valor "justo antes del umbral" (1) coincide con el mínimo permitido de cantidad — es un caso límite doblemente relevante (mínimo de cantidad Y sin descuento).

---

## 4. Tabla de Límites — Longitudes de Cadena (String Length)

### 4.1 Nombre del producto (3–100 caracteres)

| Boundary                | Longitud | Resultado Esperado |
|--------------------------|----------|----------------------|
| Debajo del mínimo        | 2        | Inválido             |
| En el mínimo             | 3        | Válido               |
| Justo sobre el mínimo    | 4        | Válido               |
| Justo bajo el máximo     | 99       | Válido               |
| En el máximo             | 100      | Válido               |
| Sobre el máximo          | 101      | Inválido             |
| Cadena vacía             | 0        | Inválido             |

### 4.2 Descripción del producto (10–500 caracteres)

| Boundary                | Longitud | Resultado Esperado |
|--------------------------|----------|----------------------|
| Debajo del mínimo        | 9        | Inválido             |
| En el mínimo             | 10       | Válido               |
| Justo sobre el mínimo    | 11       | Válido               |
| Justo bajo el máximo     | 499      | Válido               |
| En el máximo             | 500      | Válido               |
| Sobre el máximo          | 501      | Inválido             |
| Cadena vacía             | 0        | Inválido             |

### 4.3 SKU (exactamente 8 caracteres alfanuméricos)

| Boundary                          | Valor de Ejemplo         | Resultado Esperado |
|-------------------------------------|----------------------------|----------------------|
| Debajo de la longitud requerida     | `"ABC123"` (6 caracteres)  | Inválido             |
| Justo bajo la longitud requerida    | `"ABC1234"` (7 caracteres) | Inválido             |
| Longitud exacta                     | `"ABC12345"` (8 caracteres)| Válido               |
| Justo sobre la longitud requerida   | `"ABC123456"` (9 caracteres)| Inválido            |
| Sobre la longitud requerida         | `"ABC1234567"` (10 caracteres)| Inválido          |
| Cadena vacía                        | `""` (0 caracteres)        | Inválido             |
| Longitud correcta, carácter inválido| `"ABC-1234"` (guion)       | Inválido             |
| Longitud correcta, espacio incluido | `"ABC 1234"`               | Inválido             |
| Longitud correcta, todo numérico    | `"12345678"`                | Válido               |
| Longitud correcta, todo alfabético  | `"ABCDEFGH"`                | Válido               |

---

## Resumen de Casos Límite Clave

| # | Área                  | Total de casos límite identificados |
|---|------------------------|----------------------------------------|
| 1 | Rangos de precio        | 13                                       |
| 2 | Límites de cantidad     | 24 (6 por categoría × 4 categorías)      |
| 3 | Umbrales de descuento   | 12 (3 por categoría × 4 categorías)      |
| 4 | Longitudes de cadena    | 23                                       |
| **Total** | | **72 casos de prueba de frontera** |