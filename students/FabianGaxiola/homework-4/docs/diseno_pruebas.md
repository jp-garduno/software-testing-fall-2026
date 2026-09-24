# Diseño de pruebas

## Sistema bajo prueba

El sistema procesa solicitudes de inscripción a un curso y administra sus cambios de estado según los datos de la persona solicitante, la disponibilidad de cupo y el estado del pago.

Los estados posibles de una solicitud son:

- `PENDIENTE`
- `ACEPTADA`
- `RECHAZADA`
- `LISTA_ESPERA`
- `PAGO_PENDIENTE`
- `CANCELADA`

## Reglas de negocio

1. La edad debe estar entre 18 y 60 años, inclusive.
2. El promedio debe estar entre 70 y 100, inclusive.
3. Una solicitud con edad o promedio inválidos se rechaza.
4. Si los datos son válidos, pero `cupo_disponible` es menor o igual a cero, la solicitud pasa a `LISTA_ESPERA`, sin importar si el pago fue realizado.
5. Si los datos son válidos, hay cupo disponible y no se ha realizado el pago, la solicitud pasa a `PAGO_PENDIENTE`.
6. Si los datos son válidos, hay cupo disponible y el pago fue realizado, la solicitud es aceptada.
7. La función `procesar_inscripcion()` solo puede ejecutarse cuando la solicitud está en estado `PENDIENTE`.
8. La función `confirmar_pago()` solo puede ejecutarse cuando la solicitud está en estado `PAGO_PENDIENTE`.
9. Al confirmar un pago pendiente:
   - Si hay cupo disponible, la solicitud pasa a `ACEPTADA`.
   - Si no hay cupo disponible, la solicitud pasa a `LISTA_ESPERA`.
10. La función `liberar_cupo()` solo puede ejecutarse cuando la solicitud está en estado `LISTA_ESPERA`.
11. Al liberar un cupo, `cupo_disponible` aumenta en 1:

- Si el pago ya fue realizado, la solicitud pasa a `ACEPTADA`.
- Si el pago no ha sido realizado, la solicitud pasa a `PAGO_PENDIENTE`.

12. La función `cancelar_inscripcion()` puede cancelar una solicitud en cualquier estado excepto `CANCELADA`.
13. No se puede cancelar una solicitud que ya se encuentra en estado `CANCELADA`.

---

## 1. Particiones de equivalencia

| ID    | Entrada                                                     | Partición                                       | Resultado esperado             |
| ----- | ----------------------------------------------------------- | ----------------------------------------------- | ------------------------------ |
| PE-01 | Edad 25, promedio 85, cupo 10, pago sí, estado `PENDIENTE`  | Datos válidos, cupo disponible y pago realizado | `ACEPTADA`                     |
| PE-02 | Edad 17, promedio 85, cupo 10, pago sí, estado `PENDIENTE`  | Edad inválida menor al mínimo                   | `RECHAZADA`                    |
| PE-03 | Edad 61, promedio 85, cupo 10, pago sí, estado `PENDIENTE`  | Edad inválida mayor al máximo                   | `RECHAZADA`                    |
| PE-04 | Edad 25, promedio 69, cupo 10, pago sí, estado `PENDIENTE`  | Promedio inválido menor al mínimo               | `RECHAZADA`                    |
| PE-05 | Edad 25, promedio 101, cupo 10, pago sí, estado `PENDIENTE` | Promedio inválido mayor al máximo               | `RECHAZADA`                    |
| PE-06 | Edad 25, promedio 85, cupo 0, pago sí, estado `PENDIENTE`   | Datos válidos sin cupo                          | `LISTA_ESPERA`                 |
| PE-07 | Edad 25, promedio 85, cupo -1, pago no, estado `PENDIENTE`  | Cupo negativo, tratado como falta de cupo       | `LISTA_ESPERA`                 |
| PE-08 | Edad 25, promedio 85, cupo 10, pago no, estado `PENDIENTE`  | Datos válidos, cupo disponible y pago pendiente | `PAGO_PENDIENTE`               |
| PE-09 | Edad 17, promedio 69, cupo 10, pago sí, estado `PENDIENTE`  | Edad y promedio inválidos                       | `RECHAZADA`                    |
| PE-10 | Edad 17, promedio 85, cupo 0, pago no, estado `PENDIENTE`   | Datos inválidos con falta de cupo               | `RECHAZADA`                    |
| PE-11 | Edad 25, promedio 85, cupo 10, pago sí, estado `ACEPTADA`   | Solicitud no pendiente                          | Error `ValueError` al procesar |
| PE-12 | Edad 25, promedio 85, cupo 10, pago sí, estado `RECHAZADA`  | Solicitud no pendiente                          | Error `ValueError` al procesar |

---

## 2. Valores límite

Para los casos de edad y promedio, se asume que los valores no mostrados se mantienen válidos: promedio 85, edad 25, cupo 1, pago realizado y estado inicial `PENDIENTE`.

| ID    | Variable        | Valor probado | Resultado esperado |
| ----- | --------------- | ------------: | ------------------ |
| VL-01 | Edad            |            17 | `RECHAZADA`        |
| VL-02 | Edad            |            18 | `ACEPTADA`         |
| VL-03 | Edad            |            60 | `ACEPTADA`         |
| VL-04 | Edad            |            61 | `RECHAZADA`        |
| VL-05 | Promedio        |            69 | `RECHAZADA`        |
| VL-06 | Promedio        |            70 | `ACEPTADA`         |
| VL-07 | Promedio        |           100 | `ACEPTADA`         |
| VL-08 | Promedio        |           101 | `RECHAZADA`        |
| VL-09 | Cupo disponible |            -1 | `LISTA_ESPERA`     |
| VL-10 | Cupo disponible |             0 | `LISTA_ESPERA`     |
| VL-11 | Cupo disponible |             1 | `ACEPTADA`         |

---

## 3. Tabla de decisión

La validación de datos tiene prioridad sobre el cupo y el pago. La falta de cupo tiene prioridad sobre el pago.

| Regla | Datos válidos | Hay cupo (`cupo_disponible > 0`) | Pago realizado | Resultado esperado |
| ----- | ------------- | -------------------------------- | -------------- | ------------------ |
| TD-01 | Sí            | Sí                               | Sí             | `ACEPTADA`         |
| TD-02 | Sí            | Sí                               | No             | `PAGO_PENDIENTE`   |
| TD-03 | Sí            | No                               | Sí             | `LISTA_ESPERA`     |
| TD-04 | Sí            | No                               | No             | `LISTA_ESPERA`     |
| TD-05 | No            | Sí                               | Sí             | `RECHAZADA`        |
| TD-06 | No            | Sí                               | No             | `RECHAZADA`        |
| TD-07 | No            | No                               | Sí             | `RECHAZADA`        |
| TD-08 | No            | No                               | No             | `RECHAZADA`        |

---

## 4. Transiciones de estado

| ID    | Estado inicial   | Evento                                                       | Estado final esperado |
| ----- | ---------------- | ------------------------------------------------------------ | --------------------- |
| TE-01 | `PENDIENTE`      | Procesar con datos válidos, cupo disponible y pago realizado | `ACEPTADA`            |
| TE-02 | `PENDIENTE`      | Procesar con datos válidos, cupo disponible y sin pago       | `PAGO_PENDIENTE`      |
| TE-03 | `PENDIENTE`      | Procesar con datos válidos y sin cupo, con pago realizado    | `LISTA_ESPERA`        |
| TE-04 | `PENDIENTE`      | Procesar con datos válidos y sin cupo, sin pago realizado    | `LISTA_ESPERA`        |
| TE-05 | `PENDIENTE`      | Procesar con edad o promedio inválido                        | `RECHAZADA`           |
| TE-06 | `PAGO_PENDIENTE` | Confirmar pago con cupo disponible mayor que cero            | `ACEPTADA`            |
| TE-07 | `PAGO_PENDIENTE` | Confirmar pago sin cupo disponible                           | `LISTA_ESPERA`        |
| TE-08 | `LISTA_ESPERA`   | Liberar cupo con pago ya realizado                           | `ACEPTADA`            |
| TE-09 | `LISTA_ESPERA`   | Liberar cupo sin pago realizado                              | `PAGO_PENDIENTE`      |
| TE-10 | `ACEPTADA`       | Cancelar inscripción                                         | `CANCELADA`           |
| TE-11 | `PENDIENTE`      | Cancelar inscripción                                         | `CANCELADA`           |
| TE-12 | `PAGO_PENDIENTE` | Cancelar inscripción                                         | `CANCELADA`           |
| TE-13 | `LISTA_ESPERA`   | Cancelar inscripción                                         | `CANCELADA`           |
| TE-14 | `RECHAZADA`      | Cancelar inscripción                                         | `CANCELADA`           |
| TE-15 | `ACEPTADA`       | Procesar nuevamente                                          | Error `ValueError`    |
| TE-16 | `PAGO_PENDIENTE` | Procesar nuevamente                                          | Error `ValueError`    |
| TE-17 | `LISTA_ESPERA`   | Procesar nuevamente                                          | Error `ValueError`    |
| TE-18 | `ACEPTADA`       | Confirmar pago                                               | Error `ValueError`    |
| TE-19 | `PENDIENTE`      | Confirmar pago                                               | Error `ValueError`    |
| TE-20 | `ACEPTADA`       | Liberar cupo                                                 | Error `ValueError`    |
| TE-21 | `PENDIENTE`      | Liberar cupo                                                 | Error `ValueError`    |
| TE-22 | `CANCELADA`      | Cancelar nuevamente                                          | Error `ValueError`    |

---

## 5. Casos especiales identificados

| ID    | Caso                                                     | Comportamiento esperado                                                                  |
| ----- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| CE-01 | Procesar una solicitud en estado distinto de `PENDIENTE` | Se lanza `ValueError` con el mensaje `Solo se pueden procesar solicitudes pendientes`    |
| CE-02 | Confirmar pago fuera del estado `PAGO_PENDIENTE`         | Se lanza `ValueError` con el mensaje `Solo se puede confirmar el pago pendiente`         |
| CE-03 | Liberar cupo fuera del estado `LISTA_ESPERA`             | Se lanza `ValueError` con el mensaje `Solo se puede liberar cupo para lista de espera`   |
| CE-04 | Cancelar una solicitud ya cancelada                      | Se lanza `ValueError` con el mensaje `La inscripción ya está cancelada`                  |
| CE-05 | Liberar cupo cuando `cupo_disponible` es 0               | El cupo aumenta a 1 y la solicitud cambia a `ACEPTADA` o `PAGO_PENDIENTE`, según el pago |
| CE-06 | Confirmar pago cuando `cupo_disponible` es 0 o negativo  | El pago se registra como realizado y la solicitud cambia a `LISTA_ESPERA`                |
