# Reflexión breve

Lo más desafiante fue traducir una métrica de cobertura en pruebas que realmente comprobaran comportamiento. Alcanzar sentencias es relativamente directo, pero cubrir ramas obliga a pensar en estados terminales, entradas límite y errores de dependencias. El caso más útil fue diferenciar un error de repositorio —que detiene el flujo— de una notificación fallida —que no debe deshacer una tarea ya guardada.

Las pruebas de caja blanca difieren de las de caja negra porque aprovechan la estructura interna: conozco las transiciones permitidas, las condiciones de vencimiento y el orden entre guardar y notificar. Eso hizo posible diseñar pruebas negativas específicas, como el intento de volver de `DONE` a `IN_PROGRESS`. Sin embargo, no sustituyen la validación externa; una prueba end-to-end todavía sería necesaria para un proveedor de correo real.

Usaré cobertura en proyectos futuros como una alarma, no como una calificación. Me ayuda a detectar caminos olvidados y a decidir dónde añadir pruebas de frontera, pero una prueba que sólo ejecuta una línea sin verificar una regla no da confianza. La combinación de cobertura, nombres claros, dobles con especificación y verificaciones de interacción ofrece una señal mucho más útil sobre la calidad del sistema.
