# Informe de análisis de pruebas de caja blanca

## Resumen ejecutivo

Esta entrega construye TaskFlow como un sistema deliberadamente pequeño, pero con suficientes decisiones internas para evaluar pruebas de caja blanca de forma realista. La suite final contiene 48 casos y alcanza 100% de sentencias y líneas, además de 99% de ramas. Las métricas se obtuvieron ejecutando pytest-cov sobre el paquete `src`; no se incluyen módulos de terceros ni artefactos generados.

## Logro de métricas de cobertura

La estrategia más efectiva fue leer el flujo de control antes de añadir casos. En el modelo, cada condición se convirtió en una pregunta comprobable: título vacío, demasiado corto o demasiado largo; fecha vencida, actual o futura; transición hacia adelante, hacia archivado y hacia atrás; y tarea terminada o archivada frente a una fecha ya vencida. Los parámetros hacen visible que las pruebas no se limitan al caso feliz. Para el servicio, los casos cubren creación, actualización, archivado, búsqueda y detección de vencimientos. La parte más difícil fue la interacción entre campos opcionales de `update_task`; varias combinaciones de cortocircuito pueden producir el mismo efecto. Aun así, se cubrieron los resultados relevantes: sin título, mismo título, título de otra tarea y título válido.

## Retos al alcanzar cobertura alta

El principal reto fue evitar elevar la cobertura con pruebas frágiles que dependieran de la hora real o del orden de ejecución. La detección de vencimiento acepta un reloj explícito, así que los casos usan una fecha fija para comprobar los tres estados posibles. También resultó importante separar un error de persistencia de un fallo de notificación: si guardar falla, no debe enviarse correo; si el proveedor de correo falla después de guardar, la tarea sigue siendo válida. Esa diferencia requiere preparar el estado del mock y verificar qué llamadas sí ocurrieron y cuáles no. Cerca de 100%, el retorno marginal baja: coverage.py conserva dos ramas parciales debidas a cortocircuitos de argumentos opcionales, aunque todas las líneas y resultados de negocio ya están cubiertos.

## Beneficios de los mocks

Los mocks convierten repositorio y notificaciones en fronteras explícitas. Esto permitió probar duplicados, tareas inexistentes, una base de datos caída y proveedores SMS o SMTP caídos en milisegundos y sin infraestructura. Además de entregar valores controlados, los mocks verifican colaboración: `save` recibe la tarea creada, el correo de estado contiene el cambio correcto y un error de base de datos impide notificar. Sin mocks se necesitarían una base de datos y credenciales, las pruebas serían lentas y una falla externa ocultaría errores de reglas de negocio. El coste es que un mock no confirma la compatibilidad con un proveedor real; esa integración corresponde a una capa end-to-end distinta.

## Cobertura y calidad

No perseguí 100% como objetivo aislado. Una prueba útil describe una regla observable y fallaría si esa regla cambiara incorrectamente. Los contratos abstractos se excluyen de ejecución porque no contienen lógica; usar casos artificiales para invocar `NotImplementedError` mejoraría una cifra sin aportar confianza. Mantener 99% de ramas junto con 100% de líneas es una señal más honesta que inflar el conjunto con pruebas de implementación. El equilibrio consiste en usar cobertura para descubrir caminos olvidados y después exigir que cada caso tenga un riesgo, decisión o colaboración que justificar.

## Lecciones aprendidas

La lección central es que la caja blanca empieza con un mapa de decisiones, no con una herramienta de porcentaje. Ver los predicados internos reveló casos que una especificación superficial omite: estado terminal, identidad al renombrar y persistencia antes de notificar. En un proyecto futuro definiría esas fronteras inyectables desde el principio y ejecutaría cobertura en cada cambio. Así las métricas permanecen como retroalimentación temprana y las pruebas conservan independencia, velocidad y significado.
