# Reflexión sobre TDD

Aplicar TDD cambió el orden en que construí el sistema de biblioteca. En lugar
de comenzar con una clase grande de `Library` y después intentar cubrirla,
empecé por comportamientos observables y pequeños: crear un libro, conocer su
disponibilidad, crear un miembro y registrar un préstamo. Ese orden hizo que
cada decisión de diseño tuviera una razón concreta: una prueba que todavía no
pasaba. También produjo una retroalimentación muy rápida. Cuando el cambio era
pequeño, un fallo indicaba con bastante precisión qué contrato faltaba o qué
regla se había entendido mal.

El ciclo que resultó más útil fue el de préstamo y devolución. La prueba de
integración mostró que disminuir copias antes de verificar el límite de un
miembro podía dejar el inventario inconsistente. La primera implementación
funcionaba en el caso feliz, pero al agregar el caso de límite alcanzado fue
necesario restaurar la copia. Sin esa prueba, este tipo de error es fácil de
ocultar porque los métodos individuales de `Book` y `Member` siguen pareciendo
correctos. TDD ayudó a convertir una condición de fallo en una propiedad del
sistema: una operación rechazada no modifica el catálogo.

Las pruebas también guiaron el diseño de las tres características avanzadas.
Para categorías de miembro, las expectativas sobre límites y tarifas llevaron
a una tabla `CATEGORY_RULES` en la entidad `Member`, en vez de dispersar
condicionales por `Library`. Para reservas, probar primero que la persona más
antigua recibe la notificación definió naturalmente una cola FIFO. Para multas,
los casos de préstamo devuelto y de fecha no vencida aclararon que sólo se deben
cobrar los préstamos activos. En los tres casos, la prueba fue una explicación
ejecutable de la regla de negocio.

La parte más difícil fue decidir el tamaño de cada paso. Al principio parecía
eficiente implementar todas las búsquedas y toda la circulación a la vez, pero
eso habría escondido errores y producido fallos difíciles de diagnosticar. Los
pasos RED mínimos requirieron disciplina: escribir una aserción que expresa una
sola idea, observar el fallo y escribir sólo el código suficiente para volver a
verde. El costo fue hacer más commits y ejecutar la suite repetidamente, pero
el costo fue pequeño porque la suite tarda mucho menos de dos segundos.

La refactorización posterior fue igual de importante que GREEN. Extraer
`_member_and_book` redujo duplicación y mantuvo consistentes los mensajes de
error. Encapsular el siguiente elemento de reserva evitó que la devolución
manipulara directamente una lista. En cada refactor ejecuté todas las pruebas,
por lo que pude mejorar legibilidad sin temer cambiar el comportamiento. Esta
seguridad es especialmente valiosa cuando una función conecta inventario,
préstamos, historial y reservas.

Si reiniciara el proyecto, conservaría los ciclos cortos y agregaría desde el
inicio una prueba para el préstamo de una persona que ya tiene el máximo
permitido. También definiría antes el tipo monetario de las multas; aquí se
usan valores `float` sencillos porque las tarifas disponibles son múltiplos de
medio dólar, pero una versión de producción usaría `Decimal`. Como mejora
futura, añadiría filtros de búsqueda, historial visible por miembro, avisos
persistentes y límites configurables por biblioteca. La base actual permite
esas extensiones porque las responsabilidades están separadas y la suite fija
el comportamiento existente.
