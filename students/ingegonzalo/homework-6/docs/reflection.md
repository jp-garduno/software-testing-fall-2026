# Reflexión sobre TDD

## Impacto en el diseño

Escribir el test primero me obligó a pensar en la API antes que en la implementación. Cada test es el primer cliente del código: antes de escribir `Library.borrow_book` tuve que decidir qué devuelve, qué excepción lanza y en qué estado queda el sistema si falla. De ahí salieron decisiones concretas: errores de dominio con mensajes claros en lugar de `KeyError`, fechas inyectables (`borrow_date`, `return_date`) para probar multas sin depender de `date.today()`, y una tabla `CATEGORY_RULES` que solo apareció cuando el tercer caso (public) justificó generalizar.

## Desafíos

Lo más difícil fue la disciplina del código mínimo. Escribir `return True` en `is_available` parecía absurdo, y la tentación de poner la solución completa fue constante. También me costó decidir el tamaño de cada paso, y aceptar que los tests de caracterización pasan de inmediato, sin una fase RED real. Además, mantener más de 30 commits pequeños añade fricción cuando el tiempo es limitado.

## Beneficios

El mejor ejemplo fue la atomicidad de `borrow_book`. El test del límite alcanzado reveló que el sistema consumía una copia aunque el préstamo fallara. Al corregirlo, el nuevo orden creó el bug contrario (el miembro quedaba con un libro que no recibió), y otro test lo atrapó. Sin un test por cada escenario de fallo, habría entregado un sistema que pierde copias. Otro beneficio fue refactorizar con confianza: extraje validaciones y fusioné dos tablas en `CATEGORY_RULES` sabiendo que la suite me avisaría de inmediato si rompía algo. La cobertura alta fue una consecuencia natural, porque cada `if` existe porque un test lo pidió.

## Comparación con test-after

Cuando escribo los tests después, tiendo a confirmar lo que el código ya hace y se me escapan los caminos de error. Con TDD las ramas de error aparecen primero, porque son las que tengo que provocar para ver el test fallar. Test-after es más rápido al principio y menos interrumpido, pero los tests quedan más acoplados a la implementación y cubren menos casos límite. TDD es más lento por paso, pero se ahorra tiempo de depuración después.

## Uso futuro

Lo usaría en lógica de negocio con reglas claras, como multas, límites y validaciones, y al corregir bugs: primero un test que reproduzca el fallo y luego el arreglo. No lo aplicaría de forma estricta en prototipos exploratorios donde el diseño cambia cada hora, ni en código que es casi todo integración con servicios externos o interfaz gráfica, donde el test-first da menos retorno.

## Aprendizaje

Me sorprendió que arreglar un bug pueda crear su inverso, y que un buen test lo detecte al instante. También me sorprendió cómo la red de seguridad protege de errores propios: al migrar los tests a un fixture olvidé inyectar el parámetro, y 18 tests fallaron de inmediato señalando el problema exacto. Lo que haría distinto es escribir los tests de casos límite dentro de cada ciclo en lugar de agruparlos al final, ya que así se parecen más a un RED real, y mantener el formato de commits RED/GREEN/REFACTOR de principio a fin.