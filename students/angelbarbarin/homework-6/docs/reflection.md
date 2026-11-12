# TDD Reflection

## Design Impact

TDD cambió el orden en que tomé decisiones. Como cada test tenía que crear sus propios objetos, me di cuenta muy pronto de que `Library` no podía llamar a `date.today()` directamente: no hay forma de probar "17 días de retraso" sin esperar 17 días. De ahí salió el parámetro `clock` inyectable y el `FakeClock` de `conftest.py`. Con las notificaciones pasó lo mismo. Para verificarlas con un `Mock`, el notificador tenía que llegar desde fuera, y cuando escribí el test sin notificador apareció de forma natural el patrón Null Object. Escribir el test primero me obligó a pensar en la clase desde el punto de vista de quien la usa, y eso produjo un diseño con menos acoplamiento del que hubiera escrito "de corrido".

## Challenges

Lo más difícil fue la disciplina de escribir **solo** el código mínimo en la fase GREEN. Por ejemplo, en `calculate_late_fee` regresé `Decimal("0")` a propósito, sabiendo que estaba incompleto. Se siente raro escribir algo "tonto", pero el siguiente test (3 días de retraso) me obligó a escribir la fórmula real, y el de la categoría FACULTY a usar la tarifa del miembro. Otro reto fue que algunos tests que se me ocurrían ya pasaban sin cambios, como "un libro con 0 copias no está disponible" justo después de implementar `is_available`. Eso no es un ciclo RED válido, así que tuve que pensar mejor qué comportamiento nuevo quería forzar en cada paso. También costó mantener los commits pequeños cuando un test requería un fixture nuevo.

## Benefits

El beneficio más claro fue encontrar un bug que probablemente no habría visto. El test `test_borrow_book_keeps_copy_when_member_reached_limit` demostró que `borrow_book` le quitaba una copia al libro antes de descubrir que el miembro ya no podía pedir más, y dejaba la librería en un estado inconsistente. Además, la suite me dio confianza para refactorizar: extraje `_lookup`, `_search`, `_ensure_can_borrow`, `CategoryRules`, `Loan.days_overdue` y `ReservationQueue` sin miedo, porque 49 tests se ejecutaban en menos de un segundo después de cada cambio. La cobertura de 100% en statements y branches no fue algo que tuviera que "perseguir" al final. Salió sola, porque cada línea de producción existe para hacer pasar algún test.

## Comparison

En la tarea 5 (white box testing) escribí los tests después del código. Ahí la pregunta era "¿qué ramas me faltan cubrir?", y varias veces terminé escribiendo tests que describían la implementación tal como estaba, incluyendo sus defectos. Con TDD la pregunta es "¿qué debe hacer el sistema?", y los nombres de los tests se leen como una especificación: `test_late_fee_uses_member_category_rate`, `test_reserve_book_rejects_book_with_copies`. Test-after es más rápido al principio, pero el costo aparece después, cuando el código ya no es fácil de probar y hay que modificarlo solo para poder testearlo.

## Future Use

Usaría TDD en lógica de negocio con reglas claras: cálculos de dinero, validaciones, permisos y máquinas de estado. Ahí cada regla se traduce directo a un test, y equivocarse es caro. También lo usaría para corregir bugs: primero un test que reproduzca el bug y luego la corrección. No lo usaría de forma estricta en prototipos o exploraciones donde todavía no sé qué quiero construir, ni en código de interfaz gráfica muy visual, donde un test escrito antes cambia con cada ajuste de diseño. En esos casos prefiero explorar primero y escribir los tests cuando el comportamiento se estabiliza.

## Learning

Me sorprendió lo mucho que los tests guían la arquitectura. No planeé desde el inicio tener `Loan`, `ReservationQueue` ni `CategoryRules`. Aparecieron durante los REFACTOR, cuando la duplicación o los diccionarios paralelos se volvieron evidentes. También me sorprendió la velocidad: inyectar el reloj y usar mocks hizo que toda la suite corriera en alrededor de 0.2 segundos. Si lo volviera a hacer, definiría antes los fixtures compartidos en `conftest.py`, porque moverlos a mitad del proyecto generó un commit de refactor más grande que los demás. También escribiría la lista de escenarios (una "test list", como propone Kent Beck) antes de empezar cada clase, para no perder ideas de casos borde mientras estoy en medio de un ciclo.
