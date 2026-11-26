# Black Box Testing Analysis Report

## Executive Summary

Apliqué las cuatro técnicas de caja negra a SecureBank y obtuve 152 pruebas por lenguaje con 100% de cobertura del código bajo prueba. Para medir la efectividad real, y no solo la cobertura, introduje 15 defectos deliberados: la suite detectó los 15, y cada técnica encontró al menos uno que ninguna otra detectó.

## Technique Effectiveness

### Equivalence Partitioning

EP fue la técnica más fácil de aplicar y la que primero ordenó el problema: siete entradas, cada una con clases válidas e inválidas. Su mayor aporte fue obligarme a pensar en entradas que el enunciado ni menciona, como un monto con fracción de centavo o un beneficiario escrito en minúsculas. Detectó dos defectos que nadie más encontró (M6 y M15). Su límite es que un solo representativo por clase no distingue `>` de `>=`.

### Boundary Value Analysis

BVA fue la técnica más efectiva: detectó 9 de los 15 defectos y 6 de ellos en exclusiva. Casi todos los errores plausibles en un sistema bancario son de comparación (límite diario, saldo mínimo, umbral de exención, medianoche), y justo ahí vive BVA. También me dejó la lección más importante del ejercicio: en el mutante M6 el sistema dejó de validar fracciones de centavo y las pruebas BV46 y BV47 siguieron pasando, porque solo verificaban `success == False`, y el monto de $0.001 se rechazaba por otra razón. EP7, que sí verificaba el mensaje de error exacto, lo detectó. Un valor límite bien elegido con una aserción débil no protege nada.

### Decision Tables

Fue la técnica más difícil. La tabla del enunciado marca dos errores a la vez en algunas reglas, lo cual es imposible de implementar: el sistema devuelve uno. Tuve que definir una precedencia explícita entre estado, monto, límite, fondos y destino. Es la técnica que más confianza me dio en la lógica de negocio, porque obliga a revisar combinaciones que uno no pensaría por separado, como un pago programado exactamente para hoy (M12, detectado solo por DT).

### State Transition Testing

ST encontró el caso más interesante: una cuenta congelada cuyo saldo baja del mínimo por la comisión mensual. El enunciado solo define Frozen → Active, pero regresar a Active con saldo insuficiente sería incorrecto. Sin el modelo de estados no habría visto esa transición. Detectó en exclusiva M10 y M14.

## Coverage Comparison

| Técnica | Pruebas | Defectos detectados | Exclusivos |
| --- | --- | --- | --- |
| EP | 40 | 4 | 2 |
| BVA | 50 | 9 | 6 |
| DT | 38 | 4 | 1 |
| ST | 24 | 4 | 2 |

Hubo traslape claro en la validación básica de transferencias: cuatro defectos (M5, M8, M11 y M13) los detectaron dos o tres técnicas a la vez. Ese traslape no es desperdicio; es redundancia en la zona de mayor riesgo. Ninguna técnica cubrió concurrencia, zonas horarias (¿la medianoche de quién?), seguridad ni persistencia, porque no son visibles desde la especificación funcional.

## Real-World Application

En un proyecto real empezaría por EP para mapear entradas, porque es barata y produce el vocabulario que usan las demás técnicas. Después priorizaría BVA en todo lo que involucre dinero o límites, porque ahí se concentran los defectos. Usaría tablas de decisión solo en reglas con tres o más condiciones que interactúan, como las comisiones, y modelos de estado en cualquier entidad con ciclo de vida. La combinación que mejor funcionó fue EP + BVA para validar entradas, y DT + ST para la lógica de negocio.

## Recommendations

La próxima vez escribiría aserciones sobre el mensaje de error exacto desde el principio, no solo sobre el resultado booleano; el caso M6 demostró que la diferencia es real. Mediría la calidad de la suite con mutación automatizada (mutmut para Python, Stryker para JavaScript) en lugar de confiar en la cobertura. Como pruebas adicionales recomendaría concurrencia sobre el límite diario, pruebas de zona horaria alrededor de medianoche y la ejecución de pagos programados cuando el saldo cambió después de agendarlos.

## Lessons Learned

La lección más importante: 100% de cobertura dice qué código se ejecutó, no qué código se verificó. La cobertura fue la misma antes y después de encontrar el problema de M6; lo que cambió fue la calidad de las aserciones.
