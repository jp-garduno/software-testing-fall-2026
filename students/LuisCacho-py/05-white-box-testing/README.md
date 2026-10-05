# 05 - White Box Testing Exercises

Este directorio contiene las soluciones completas a los 4 ejercicios prácticos del módulo **05-white-box-testing** en Python para el estudiante **LuisCacho-py**.

## 📁 Estructura del Proyecto

```text
05-white-box-testing/
├── 01-calculator/
│   ├── calculator.py
│   └── test_calculator.py
├── 02-shopping-cart/
│   ├── shopping_cart.py
│   └── test_shopping_cart.py
├── 03-user-service/
│   ├── email_service.py
│   ├── user_repository.py
│   ├── user_service.py
│   └── test_user_service.py
├── 04-coverage-challenge/
│   ├── order_processor.py
│   ├── test_order_processor.py
│   └── reflection.md
└── README.md
```

---

## 📋 Resumen de los Ejercicios

### 1. Exercise 1: Calculator Unit Tests (`01-calculator/`)
- **Implementación**: Clase `Calculator` con soporte de operaciones aritméticas básicas (`add`, `subtract`, `multiply`, `divide`, `power`, `sqrt`) y las operaciones adicionales de la Parte 4 (`modulo`, `absolute`, `factorial`).
- **Pruebas**: 33 pruebas unitarias probando casos estándar, valores límite, división entre cero, números negativos y tipos inválidos.
- **Cobertura**: **100% Statements**, **100% Branches**.

### 2. Exercise 2: Shopping Cart Class Testing (`02-shopping-cart/`)
- **Implementación**: Clases `Item` y `ShoppingCart` con gestión de estado, cálculo de subtotales, descuentos porcentuales, conteo de items y manejo de duplicados.
- **Pruebas**: 34 pruebas unitarias que cubren todas las ramas condicionales de validación, adición, eliminación y cálculo de descuentos.
- **Cobertura**: **100% Statements**, **100% Branches**.

### 3. Exercise 3: User Service with Integration & Mocking (`03-user-service/`)
- **Implementación**: Capas desacopladas `user_repository.py`, `email_service.py` y `user_service.py` para registro, autenticación y notificaciones.
- **Pruebas**: 34 pruebas usando `unittest.mock.Mock` para aislar dependencias externas (base de datos y envío de correos) y pruebas de integración de flujo completo (registro seguido de login).
- **Cobertura**: **100% Statements**, **100% Branches** en todos los módulos de producción.

### 4. Exercise 4: Coverage Challenge (`04-coverage-challenge/`)
- **Implementación**: Sistema `order_processor.py` con validación exhaustiva de órdenes, items, direcciones postales estadounidenses e internacionales, recargos de envío, códigos de descuento y estimación de entrega.
- **Pruebas**: 63 pruebas unitarias y parametrizadas cubriendo caminos complejos y condiciones de borde.
- **Reflexión**: Análisis documentado en `reflection.md`.
- **Cobertura**: **100% Statements**, **99% Branches** (con la única excepción de una rama defensiva estructuralmente inalcanzable explicada en el reporte).

---

## 🚀 Ejecución de Pruebas

Para ejecutar todas las pruebas y obtener el reporte de cobertura:

```bash
cd students/LuisCacho-py/05-white-box-testing
pytest --cov=. --cov-report=term-missing --cov-branch
```

Para ejecutar un ejercicio individual:

```bash
# Ejercicio 1
pytest --cov=calculator --cov-report=term-missing --cov-branch 01-calculator/test_calculator.py

# Ejercicio 2
pytest --cov=shopping_cart --cov-report=term-missing --cov-branch 02-shopping-cart/test_shopping_cart.py

# Ejercicio 3
pytest --cov=. --cov-report=term-missing --cov-branch 03-user-service/test_user_service.py

# Ejercicio 4
pytest --cov=order_processor --cov-report=term-missing --cov-branch 04-coverage-challenge/test_order_processor.py
```
