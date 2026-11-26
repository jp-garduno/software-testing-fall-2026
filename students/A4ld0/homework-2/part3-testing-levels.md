# Parte 3: Estrategia por niveles

Plan para una implementación accesible al equipo en un entorno aislado. Las herramientas son opciones sujetas al lenguaje real. Los tipos indican qué se evalúa; los niveles, el alcance de los componentes involucrados.

## Unit Testing

**Scope**: Funciones o componentes aislados, con red y almacenamiento sustituidos por dobles de prueba.

**What to Test**:

- Validación de archivos y descripciones.
- Reglas de audiencia y permisos.
- Transiciones de estado de interacciones y reintentos.

**Tools**: JUnit para lógica JVM, XCTest para lógica iOS y Jest si existen componentes JavaScript.

**Coverage Goal**: Al menos 80% de ramas en el código del alcance y 100% de reglas identificadas de autorización; cobertura no equivale a ausencia de errores.

**Example Test Cases**:

1. Para un límite configurable L de tamaño, aceptar L−1 y L bytes y rechazar L+1 con error de validación.
2. Para audiencia “Solo tú”, permitir al propietario y denegar a cualquier otro identificador.
3. Procesar dos veces el mismo evento de “me gusta”: producir un único cambio de estado.

**Estimated Number of Tests**: Aproximadamente 180.

## Integration Testing

**Scope**: Interfaces entre autenticación, publicaciones, almacenamiento y feed, utilizando servicios de prueba reales y fallos controlados.

**What to Test**:

- Propagación de identidad y autorización.
- Consistencia entre metadatos y archivos.
- Contratos de respuesta y reintentos.

**Tools**: Postman/Newman para API; Testcontainers si los servicios pueden ejecutarse en contenedores.

**Coverage Goal**: Todos los contratos críticos con un caso exitoso, uno de rechazo y uno de error de dependencia.

**Example Test Cases**:

1. Crear una publicación restringida y consultarla desde otra cuenta: API y almacenamiento impiden recuperar el contenido.
2. Completar la carga del archivo: el servicio registra metadatos coherentes y el propietario puede reproducirlo.
3. Simular timeout después de guardar una publicación y repetir su identificador de operación: existe una sola publicación.

**Estimated Number of Tests**: Aproximadamente 70.

## System Testing

**Scope**: Aplicación integrada de extremo a extremo, incluidos clientes y servicios de prueba.

**What to Test**:

- Recorridos completos de usuarios.
- Rendimiento y recuperación.
- Compatibilidad, seguridad y accesibilidad.

**Tools**: Appium para móvil, Playwright para web y k6 para carga sobre el ambiente autorizado.

**Coverage Goal**: 100% de recorridos P0/P1 y ejecución de recorridos esenciales en cada configuración de la matriz soportada.

**Example Test Cases**:

1. Iniciar sesión, publicar con “Solo tú” y abrir el enlace desde otra cuenta: el propietario reproduce el video y la segunda cuenta no accede.
2. Consumir el feed durante una pérdida y recuperación de red: la aplicación informa el problema y vuelve a reproducir sin reiniciarse.
3. Ejecutar 1,000 sesiones concurrentes durante 30 minutos: errores del feed inferiores al 1%, según la meta propuesta.

**Estimated Number of Tests**: Aproximadamente 40 escenarios base; las combinaciones de dispositivos generan ejecuciones adicionales.

## Acceptance Testing

**Scope**: Validación de necesidades por representantes de espectadores, creadores, producto y privacidad.

**What to Test**:

- Publicación comprensible y confiable.
- Control efectivo de audiencia.
- Consumo accesible y manejo comprensible de errores.

**Tools**: Guiones manuales, dispositivos reales, registro de resultados y grabación de sesiones con consentimiento.

**Coverage Goal**: Todos los criterios de aceptación críticos aprobados; al menos nueve de diez participantes completan publicación y selección de audiencia sin ayuda.

**Example Test Cases**:

1. Un creador publica para sí mismo y explica quién puede verlo; la audiencia efectiva coincide con su intención.
2. Un espectador encuentra una cuenta de prueba, reproduce su video público y puede seguirla sin asistencia.
3. Una persona que utiliza lector de pantalla identifica y activa controles principales; el estado resultante se anuncia correctamente.

**Estimated Number of Tests**: Aproximadamente 12 escenarios, repartidos entre perfiles representativos.

## Ejecución y criterios de salida

Las pruebas unitarias y de integración se ejecutarían por cambio; los recorridos esenciales de sistema, por build candidato. La regresión ampliada y las sesiones de aceptación se realizarían antes de liberar.

Se requieren cuentas sintéticas con distintas audiencias, videos válidos e inválidos y una matriz de dispositivos definida antes de ejecutar. Cada fallo registra versión, datos, pasos, resultado esperado y evidencia. Una corrección requiere reejecutar el caso fallido y su regresión relacionada.

Se propone impedir la liberación con defectos P0/P1 abiertos o pruebas críticas fallidas. Los riesgos restantes requieren evaluación explícita de producto y QA. Las aproximadamente 302 pruebas base son una estimación del alcance académico, no de toda la plataforma.
