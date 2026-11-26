# TDD Reflection

## 1. Design Impact

Lo que más cambió fue el orden en que aparecieron las decisiones. En lugar de diseñar las clases completas al principio, cada atributo y cada método llegó cuando una prueba lo pidió. `total_copies`, por ejemplo, no existió hasta que una prueba exigió rechazar la devolución de una copia que nunca se prestó. Hacer la prueba primero también me obligó a pensar en cómo se usa cada clase antes de pensar en cómo funciona por dentro: por eso `Library` recibe un reloj y un notificador en el constructor. Si hubiera escrito el código primero, seguramente habría llamado a `date.today()` directamente y después habría tenido que buscar la forma de probarlo. Con TDD, la necesidad de controlar el tiempo en una prueba produjo un diseño con dependencias inyectadas sin que fuera una decisión aparte.

## 2. Challenges

Lo más difícil fue resistir la ganas de escribir de más en la fase GREEN. Sabía que `is_available()` iba a comparar copias con cero, y aun así la regla pedía empezar con `return True`. Al principio se sintió artificial; tuvo sentido cuando la siguiente prueba rompió ese valor falso y quedó claro que cada caso de la regla tenía una prueba que lo respaldaba. También costó elegir el tamaño de cada paso: si la prueba es muy ambiciosa, el GREEN deja de ser pequeño. Y hubo un reto más práctico: el hook de Conventional Commits del repositorio rechazaba los mensajes `RED:` y `GREEN:`, así que tuve que aprender a saltar solo ese hook sin desactivar los demás.

## 3. Benefits

El beneficio más concreto fue un bug que la prueba encontró antes de que existiera en desarrollo. `borrow_book` tomaba la copia del estante antes de revisar el límite del miembro, de modo que un préstamo rechazado dejaba el libro con una copia menos. La prueba `test_should_keep_copy_on_shelf_when_member_is_at_limit` lo mostró con un `assert 0 == 1`, y de ahí salió una regla que apliqué en todo el sistema: validar todas las precondiciones antes de modificar estado. El otro beneficio fue la confianza para refactorizar: cambié el `list` de reservas por un `deque` y extraje `_first_in_line` sin problema, porque 56 pruebas tardaban menos de un segundo en confirmar que nada se había roto.

## 4. Comparison

En la tarea 5 trabajé al revés: el código ya existía y las pruebas se escribieron después, guiadas por el reporte de cobertura para encontrar líneas y ramas sin probar. Ese enfoque es útil para auditar código, pero las pruebas terminan describiendo la implementación. Con TDD las pruebas describen comportamientos, y sus nombres (`should_hold_returned_copy_for_first_member_in_line`) se leen como una especificación. Lo curioso es que aquí nunca perseguí la cobertura y terminó en 100% de sentencias y de ramas, simplemente porque no existe código que no haya pedido alguna prueba.

## 5. Future Use

Usaría TDD en lógica de negocio con reglas claras: cálculos de multas, validaciones, colas, permisos, cualquier cosa donde un error cueste dinero o datos. También para corregir bugs: escribir primero la prueba que reproduce el error. No lo usaría para explorar una interfaz gráfica o hacer un prototipo cuyo objetivo es descubrir qué se necesita, ni para scripts desechables, donde las pruebas serían trabajo perdido. En esos casos prefiero explorar primero y aplicar TDD cuando el diseño se estabiliza.

## 6. Learning

Me sorprendió que refactorizar las pruebas fuera tan importante como refactorizar el código. Extraer `make_book` y `make_library` hizo que cada prueba mostrara solo el dato relevante, y eso facilitó escribir las siguientes. También me sorprendió lo útil que es un `Mock`: con `assert_called_once_with("M2", ISBN)` verifiqué en una línea que se avisa una sola vez y que se respeta el orden FIFO. Si lo hiciera de nuevo, escribiría al inicio una lista de pruebas pendientes por clase, para no improvisar el siguiente paso, y pensaría antes en las categorías de miembro: agregarlas al final obligó a cambiar el constructor de `Member` cuando ya había varias pruebas que dependían de él (aunque fueron esas mismas pruebas las que protegieron el cambio).
