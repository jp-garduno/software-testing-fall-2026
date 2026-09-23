# Diseño de pruebas

## Sistema bajo prueba

El sistema procesa solicitudes de inscripción a un curso.

### Reglas de negocio

1. La edad debe estar entre 18 y 60 años.
2. El promedio debe estar entre 70 y 100.
3. Debe existir al menos un cupo disponible.
4. El pago debe estar realizado para aceptar una inscripción.
5. Las solicitudes válidas sin cupo pasan a lista de espera.
6. Las solicitudes válidas con cupo pero sin pago quedan en pago pendiente.
7. Una solicitud procesada no puede procesarse nuevamente.

---

## 1. Particiones de equivalencia

| ID | Entrada | Partición | Resultado esperado |
|---|---|---|---|
| PE-01 | Edad 25, promedio 85, cupo 10, pago sí | Datos válidos | ACEPTADA |
| PE-02 | Edad 17 | Edad inválida menor al mínimo | RECHAZADA |
| PE-03 | Edad 61 | Edad inválida mayor al máximo | RECHAZADA |
| PE-04 | Promedio 69 | Promedio inválido menor al mínimo | RECHAZADA |
| PE-05 | Promedio 101 | Promedio inválido mayor al máximo | RECHAZADA |
| PE-06 | Cupo 0, pago sí | Sin cupo | LISTA_ESPERA |
| PE-07 | Cupo 10, pago no | Pago no realizado | PAGO_PENDIENTE |

---

## 2. Valores límite

| ID | Variable | Valor probado | Resultado esperado |
|---|---|---:|---|
| VL-01 | Edad | 17 | RECHAZADA |
| VL-02 | Edad | 18 | ACEPTADA |
| VL-03 | Edad | 60 | ACEPTADA |
| VL-04 | Edad | 61 | RECHAZADA |
| VL-05 | Promedio | 69 | RECHAZADA |
| VL-06 | Promedio | 70 | ACEPTADA |
| VL-07 | Promedio | 100 | ACEPTADA |
| VL-08 | Promedio | 101 | RECHAZADA |
| VL-09 | Cupo | -1 | LISTA_ESPERA |
| VL-10 | Cupo | 0 | LISTA_ESPERA |
| VL-11 | Cupo | 1 | ACEPTADA |

---

## 3. Tabla de decisión

| Regla | Datos válidos | Hay cupo | Pago realizado | Resultado |
|---|---|---|---|---|
| TD-01 | Sí | Sí | Sí | ACEPTADA |
| TD-02 | Sí | Sí | No | PAGO_PENDIENTE |
| TD-03 | Sí | No | Sí | LISTA_ESPERA |
| TD-04 | Sí | No | No | LISTA_ESPERA |
| TD-05 | No | Sí | Sí | RECHAZADA |
| TD-06 | No | No | No | RECHAZADA |

---

## 4. Transiciones de estado

| ID | Estado inicial | Evento | Estado final esperado |
|---|---|---|---|
| TE-01 | PENDIENTE | Datos válidos, cupo y pago | ACEPTADA |
| TE-02 | PENDIENTE | Datos válidos, cupo y sin pago | PAGO_PENDIENTE |
| TE-03 | PAGO_PENDIENTE | Confirmar pago con cupo | ACEPTADA |
| TE-04 | PENDIENTE | Datos válidos sin cupo | LISTA_ESPERA |
| TE-05 | LISTA_ESPERA | Liberar cupo con pago | ACEPTADA |
| TE-06 | LISTA_ESPERA | Liberar cupo sin pago | PAGO_PENDIENTE |
| TE-07 | ACEPTADA | Cancelar inscripción | CANCELADA |
| TE-08 | ACEPTADA | Procesar nuevamente | Error |
| TE-09 | ACEPTADA | Confirmar pago | Error |
| TE-10 | ACEPTADA | Liberar cupo | Error |
| TE-11 | CANCELADA | Cancelar nuevamente | Error |
