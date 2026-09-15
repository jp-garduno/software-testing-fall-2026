## 1. Testing Shows Presence of Defects

[//]: # (## 1. Las pruebas muestran la presencia de defectos.)

**Aplicado**
Las pruebas pueden demostrar que existen errores, pero no pueden probar que no existen. Por lo cual se deben establecer pruebas realistas y específicas para comprobar el comportamiento de la app.

**Estrategia**
- Dar prioridad a las áreas críticas
- Supervisar las funciones del MVP
- Realizar encuestas de satisfacción a los usuarios (para monitorear la satisfacción)

---

## 2. Exhaustive Testing is Impossible

[//]: # (## 2. Es imposible realizar pruebas exhaustivas.)

**Aplicado**
Probarlo todo no es factible, excepto en casos triviales. Por lo cual nos vamos a centrar en la función de riesgo y en el MVP.

**Estrategia**
- Revisar que se puedan realizar correctamente las funciones del MVP
- Probar diversas intervenciones externas de datos (para detectar vulnerabilidades y proteger datos)
- Dejar en segundo plano lo que no le dé experiencia directa al usuario ni genere valor

---

## 3. Early Testing

[//]: # (## 3. Pruebas tempranas)

**Aplicado**
Comience las pruebas lo antes posible en el ciclo de vida del desarrollo de software. Probar los requisitos, el diseño y el código mientras se desarrolla la app, y no solo antes de que la plataforma se lance.

**Estrategia**
- Probar el código cuando se termine un módulo.
- Probar cómo interactúa el código entre sí.
- Hacer pruebas alfa y beta para saber cómo va la app, y no esperar hasta el feedback final

---
## 4. Defect Clustering
<!-- ## 4. Agrupación de defectos -->

**Aplicado**
Un número reducido de módulos contiene la mayoría de los defectos (regla 80/20). Centrar las pruebas en los módulos de alto riesgo.

**Estrategia**
- Revisar constantemente los módulos que contienen el MVP y las transacciones bancarias
- No dejar elementos importantes a la vista (como el .env)
- Traer ojos nuevos, sin visión de túnel, para buscar cosas que no se hayan visto

---

## 5. Pesticide Paradox
<!-- ## 5. La paradoja de los plaguicidas -->

**Aplicado**
Repetir las mismas pruebas no encontrará nuevos defectos. Por lo cual, para una plataforma con tantas funciones como Netflix, es importante actualizar y renovar las pruebas periódicamente, sobre todo las de elementos vitales.

**Estrategia**
- Modificar las pruebas del código cuando se agregue algo nuevo al módulo, o algo que lo afecte.
- Modificar las pruebas conforme a cómo se está usando la app normalmente (encontrar fallos en lo real y no en lo teórico).
- Ver interacciones reales con el código, y no código prehecho (para evitar que se desarrolle código pensando en cómo resolver la prueba y no el problema)

---
## 6. Testing is Context Dependent
<!-- ## 6. Las pruebas dependen del contexto. -->

**Aplicado**
Las pruebas se deben adaptar a la plataforma (es decir, Netflix) y no al revés.

**Estrategia**
- Ver el feedback del usuario para atacar asperezas o errores
- Pensar en cómo solucionar el código y no en resolver las pruebas
- Adaptar las pruebas a las necesidades reales del cliente y no solo a lo teórico (adaptación)

---
## 7. Absence of Errors Fallacy
<!-- ## 7. Falacia de ausencia de errores -->

**Aplicado**
Un software libre de errores es inútil si no satisface las necesidades del usuario. Por lo cual es más importante que Netflix satisfaga las necesidades de sus usuarios, a que no tenga errores pero sea inutilizable (o que nunca salga).

**Estrategia**
- Revisar el feedback constante de los usuarios
- Centrarse en las partes que den valor al producto y dejar las otras en segundo plano
- Si algo no se puede corregir (y no es vital), siempre existirá otro sprint.