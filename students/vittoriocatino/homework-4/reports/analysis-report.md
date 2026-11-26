# Análisis de efectividad de las pruebas de caja negra

## Resumen ejecutivo

La suite de SecureBank combinó cuatro técnicas de caja negra para convertir
reglas de negocio en 73 verificaciones reproducibles. El resultado final fue de
73 pruebas aprobadas y 100% de cobertura de líneas y ramas. Más importante que
el porcentaje, la combinación permitió revisar entradas, umbrales, reglas
simultáneas y secuencias de estados desde perspectivas complementarias.

## Efectividad de las técnicas

### Particiones de equivalencia

Las particiones fueron la técnica más sencilla para iniciar porque permitieron
separar rápidamente entradas válidas e inválidas: montos positivos, tipos de
cuenta reconocidos, beneficiarios vacíos y rangos de fechas invertidos. Fueron
eficientes para cubrir categorías amplias con pocos representantes y ayudaron a
definir claramente qué acepta la interfaz pública. Su limitación es que un solo
representante no revela por sí mismo errores situados exactamente en un límite.

### Valores frontera

El análisis de frontera encontró la mayor cantidad de problemas potenciales.
Las expresiones “mínimo $100” y “exenta si el saldo es mayor que $1,000” parecen
simples, pero cambian completamente en valores como $99.99, $100, $1,000 y
$1,000.01. Esta técnica evitó dos errores comunes: aceptar una transferencia de
$0 y usar `>=` para una exención definida con `>`. Fue fácil proponer valores,
pero exigió cuidar que saldo, monto y límite no interfirieran entre sí.

### Tablas de decisión

Las tablas fueron la técnica más difícil porque varias condiciones pueden
fallar simultáneamente. Para producir resultados deterministas fue necesario
documentar la prioridad de validación: estado, límite y fondos en transferencias;
beneficiario, monto y fondos en pagos. Las tablas dieron la mayor confianza en
las reglas de negocio, ya que recorrieron las ocho combinaciones de cada regla
de tres condiciones y evidenciaron cualquier acción faltante o contradictoria.

### Transiciones de estado

Las pruebas de estado aportaron una dimensión que las otras técnicas no cubren:
el historial. Un mismo depósito tiene distinto efecto en Active, Suspended y
Closed. Verificar que Closed sea terminal y que una cuenta suspendida vuelva a
Active al restaurar el mínimo previene defectos graves que no serían visibles
al probar operaciones aisladas. El diagrama Mermaid también facilitó detectar
eventos inválidos, como congelar dos veces o intentar reabrir una cuenta cerrada.

## Comparación de cobertura

| Técnica | Pruebas | Enfoque principal | Riesgo mejor cubierto |
|---|---:|---|---|
| Particiones | 17 | Clases válidas e inválidas | Validación de entradas |
| Fronteras | 21 | Valores adyacentes a umbrales | Errores `>` frente a `>=` |
| Decisiones | 21 | Combinaciones de condiciones | Prioridad y reglas incompletas |
| Estados | 14 | Secuencias y eventos | Operaciones ilegales por estado |

Existió solapamiento intencional: el límite de transferencia aparece en EP,
BVA y la tabla de decisiones. Esa redundancia no es desperdicio; confirma la
misma regla a nivel de categoría, borde e interacción. En cambio, ninguna de
estas pruebas sustituye seguridad, concurrencia, rendimiento, persistencia o
integración con una red bancaria. La cobertura estructural del modelo llegó a
100%, pero no implica cobertura completa del producto real.

## Aplicación profesional

En un proyecto real empezaría con particiones para acordar el contrato de cada
API y después priorizaría BVA en montos, fechas y límites, porque los defectos
financieros suelen concentrarse en bordes. Usaría tablas de decisión junto con
analistas de negocio para revisar políticas complejas antes de programarlas, y
modelos de estado para cuentas, pagos programados y procesos antifraude. La
mejor combinación es EP más BVA para datos, y decisiones más estados para
comportamiento.

## Recomendaciones y lecciones aprendidas

En una siguiente iteración agregaría propiedades generativas para muchos montos,
pruebas de zona horaria alrededor de medianoche y escenarios concurrentes que
intenten consumir el límite diario al mismo tiempo. También pediría requisitos
explícitos sobre redondeo, prioridad de errores, beneficiarios válidos y cobro de
cuotas en cuentas Frozen. La principal lección es que diseñar primero reduce
supuestos ocultos: las tablas obligan a explicar qué debe pasar antes de que el
código convierta una ambigüedad en un defecto.
