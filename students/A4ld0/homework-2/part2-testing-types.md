# Parte 2: Tipos de pruebas

Las categorías siguen el formato de la tarea. Regresión describe un propósito que puede abarcar ambos grupos; aquí se clasifica su suite funcional. Los umbrales son objetivos propuestos, no mediciones de TikTok.

## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Comprobar los recorridos de consumo, creación e interacción.

**Examples**:

1. Publicar un video válido: aparece una sola vez en el perfil y se reproduce.
2. Dar y quitar “me gusta”: el estado personal y el contador se actualizan sin duplicarse.
3. Desactivar comentarios: otro usuario no puede crear uno nuevo y recibe una indicación clara.

**Priority**: Critical

**Justification**: Un fallo impide las acciones que dan valor a la aplicación.

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Evaluar rapidez y estabilidad al reproducir contenido bajo carga.

**Examples**:

1. Con red de 20 Mbps y latencia de 50 ms, medir 100 inicios de video; objetivo: percentil 95 de tiempo al primer fotograma menor a 2 segundos.
2. Simular 1,000 sesiones concurrentes durante 30 minutos en pruebas; objetivo: menos de 1% de respuestas fallidas en el feed.
3. Reproducir durante 30 minutos con red estable; objetivo: tiempo total de pausas por buffering menor al 1% de la sesión.

**Priority**: High

**Justification**: Esperas y cortes afectan directamente el recorrido más frecuente. La carga se ajustaría a la capacidad del ambiente autorizado.

## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Proteger sesiones y evitar acceso a recursos sin autorización.

**Examples**:

1. Solicitar desde una segunda cuenta el identificador de un video “Solo tú”: la API rechaza el acceso y no entrega el archivo.
2. Reutilizar una sesión revocada explícitamente: el servidor exige autenticación nuevamente.
3. Introducir texto con etiquetas de script en un comentario: se muestra como texto inerte y no ejecuta código en el cliente web.

**Priority**: Critical

**Justification**: La exposición de publicaciones o el control indebido de cuentas puede causar daños difíciles de revertir.

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Verificar que espectadores y creadores comprendan los flujos esenciales.

**Examples**:

1. Pedir a diez participantes que publiquen con audiencia restringida; objetivo: al menos nueve completan la tarea sin ayuda.
2. Mostrar un fallo de carga: el participante identifica qué ocurrió y cómo reintentar.
3. Pedir que desactiven comentarios y expliquen el efecto; objetivo: al menos nueve de diez interpretan correctamente el control.

**Priority**: High

**Justification**: Una interfaz confusa puede provocar abandono o divulgación involuntaria de contenido.

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Detectar efectos secundarios de cambios sobre funciones existentes.

**Examples**:

1. Después de modificar autenticación, comprobar inicio de sesión, recuperación y cierre de sesión.
2. Después de cambiar el editor, publicar un video y verificar descripción, audio y audiencia.
3. Después de actualizar el feed, verificar que contenido privado no aparezca en una cuenta sin permiso.

**Priority**: High

**Justification**: Cambios en componentes compartidos pueden romper recorridos previamente correctos; las comprobaciones de privacidad son bloqueantes.

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Mantener los recorridos esenciales en la matriz de dispositivos soportados.

**Examples**:

1. Reproducir y publicar en las versiones mínima y más reciente de Android e iOS seleccionadas para el proyecto.
2. Abrir el perfil y reproducir videos en Chrome, Safari y Firefox de la matriz; comprobar controles y orientación.
3. Usar una pantalla pequeña y texto ampliado: el botón de audiencia sigue visible y operable.

**Priority**: High

**Justification**: Diferencias de sistema, navegador y pantalla pueden bloquear funciones para grupos completos de usuarios.

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Permitir navegación e interacción a personas con distintas capacidades.

**Examples**:

1. Con TalkBack y VoiceOver, identificar el botón “me gusta” y escuchar su estado activado o desactivado.
2. Navegar por la versión web con teclado: todos los controles tienen foco visible y no existen trampas de foco.
3. Reproducir un video de prueba con subtítulos revisados: son legibles, están sincronizados y no quedan ocultos por controles.

**Priority**: High

**Justification**: Barreras de acceso impiden utilizar la aplicación aunque sus funciones respondan correctamente.

## Test Type: Recovery Testing

**Category**: Non-Functional

**Purpose**: Evaluar recuperación frente a interrupciones sin corrupción ni duplicación de datos.

**Examples**:

1. Cortar la red durante una publicación y reintentar: queda una sola publicación completa o un error recuperable.
2. Interrumpir una confirmación de “me gusta” y repetir la petición: el estado final registra una sola interacción.
3. Simular indisponibilidad del servicio de videos: aparece un mensaje útil y la reproducción se recupera cuando vuelve el servicio.

**Priority**: High

**Justification**: Las interrupciones móviles son esperables y no deben causar pérdida silenciosa de trabajo.
