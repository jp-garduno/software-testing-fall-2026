# Part 2: Testing Types Classification

Aplicación bajo prueba: **Spotify**. A continuación, diez tipos de prueba necesarios, con su categoría, propósito, ejemplos concretos, prioridad y justificación.

---

## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Verificar que cada funcionalidad se comporta según lo especificado. En Spotify esto cubre el flujo completo que recorre un usuario: autenticarse, buscar, reproducir, armar playlists y administrar su suscripción. Es la base sobre la que se apoyan todos los demás tipos.

**Examples**:

1. Un usuario premium reproduce una canción completa y el reproductor avanza automáticamente a la siguiente pista de la cola sin silencio intermedio.
2. Al agregar una canción a una playlist colaborativa, la pista aparece para los demás colaboradores y queda atribuida al usuario que la agregó.
3. Un usuario del free tier intenta el sexto salto dentro de una hora y el sistema bloquea la acción mostrando el mensaje de límite alcanzado.

**Priority**: Critical

**Justification**: Si las funciones centrales fallan, el producto no tiene valor alguno. Además, la mayoría de los tipos de prueba restantes presuponen que la funcionalidad base ya opera correctamente: no tiene sentido medir el rendimiento de una búsqueda que devuelve resultados equivocados.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Garantizar que el sistema responde con la latencia esperada y sostiene la carga en los picos de uso. Spotify tiene picos predecibles (mañanas de lunes, viernes por el lanzamiento semanal de música, y los estrenos de álbumes de artistas masivos) y picos extraordinarios como el lanzamiento anual de Spotify Wrapped, que multiplica el tráfico varias veces en pocas horas.

**Examples**:

1. El tiempo hasta el primer byte de audio (*time to first sound*) al pulsar play se mantiene por debajo de 500 ms en el percentil 95 sobre una red 4G.
2. La búsqueda devuelve resultados en menos de 300 ms con 50,000 consultas por segundo sostenidas durante 30 minutos.
3. Bajo una prueba de estrés con 10 millones de sesiones concurrentes durante el lanzamiento de Wrapped, el servicio de reproducción se degrada de forma controlada (las recomendaciones se sirven desde caché) en lugar de caer por completo.

**Priority**: Critical

**Justification**: La percepción de calidad en una app de audio es inseparable de la latencia. Un retraso de dos segundos antes de que empiece la canción se lee como "la app está rota", aunque funcionalmente todo esté correcto. Y una caída durante un lanzamiento importante tiene costo reputacional inmediato y visible en redes sociales.

---

## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Proteger las credenciales, los datos personales, los métodos de pago y —de forma igualmente importante— el propio catálogo licenciado frente a la extracción no autorizada de audio.

**Examples**:

1. Intentar inyección SQL y de comandos en el campo de búsqueda y en el nombre de playlist; el sistema debe rechazar la entrada sin exponer trazas de error del backend.
2. Verificar que un token de sesión revocado tras un cierre de sesión remoto deja de ser aceptado por la API de reproducción en menos de 60 segundos.
3. Comprobar que las pistas descargadas en modo offline permanecen cifradas en el almacenamiento del dispositivo y que no pueden reproducirse fuera de la aplicación aunque se extraiga el archivo con acceso root.

**Priority**: Critical

**Justification**: Un fallo aquí no solo daña al usuario: la extracción masiva del catálogo constituiría un incumplimiento de los contratos de licenciamiento con los sellos, con consecuencias legales que exceden cualquier bug funcional. La normativa de protección de datos (GDPR en Europa) añade exposición regulatoria por el manejo de datos personales y de hábitos de escucha.

---

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Confirmar que las tareas frecuentes se completan sin fricción, con particular atención al uso en contextos donde la atención del usuario está en otra parte: manejando, corriendo o cocinando.

**Examples**:

1. Un usuario nuevo consigue reproducir su primera canción en menos de tres interacciones desde la pantalla inicial, sin ayuda externa.
2. Los controles de reproducción (play, pausa, siguiente) tienen un área táctil de al menos 44×44 puntos y se accionan correctamente con el pulgar en una sola mano.
3. Un grupo de diez usuarios encuentra la opción de descargar una playlist para escucharla sin conexión sin recurrir al buscador de la app ni a documentación.

**Priority**: High

**Justification**: La barrera de cambio a un servicio competidor es prácticamente nula: la música es la misma en todas las plataformas y la suscripción se cancela en dos clics. La experiencia de uso es, en la práctica, el diferenciador del producto. No la clasifico como crítica solo porque un problema de usabilidad rara vez impide por completo el uso del servicio.

---

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Asegurar que cada despliegue no rompa funcionalidad que ya operaba. Spotify libera cambios de forma continua sobre decenas de microservicios y varias plataformas cliente simultáneamente, así que el riesgo de romper algo lateral es permanente.

**Examples**:

1. Ejecutar la suite completa de flujos críticos (login, búsqueda, reproducción, pago) en cada merge a la rama principal, en las cinco plataformas soportadas.
2. Tras una refactorización del motor de recomendaciones, verificar que Discover Weekly sigue generándose cada lunes y que no incluye canciones ya marcadas como "no me gusta".
3. Después de corregir un defecto de crossfade, reejecutar el conjunto de pruebas de reproducción para confirmar que el gapless playback y el modo aleatorio siguen intactos.

**Priority**: Critical

**Justification**: Con despliegues diarios y una base de código compartida entre equipos, la regresión es el modo de falla más probable de todos. Es también el tipo de prueba con mejor retorno sobre la automatización: se ejecuta cientos de veces al mes.

---

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Verificar el comportamiento correcto en la enorme matriz de dispositivos, sistemas operativos, navegadores y hardware de audio donde Spotify se ejecuta: teléfonos Android de gama baja, iPhones, escritorio en Windows, macOS y Linux, navegadores, bocinas inteligentes, consolas, relojes y sistemas de infoentretenimiento automotriz.

**Examples**:

1. La app se instala y reproduce audio correctamente en Android 10 sobre un dispositivo con 2 GB de RAM, sin cierres por falta de memoria durante una sesión de 30 minutos.
2. La transferencia de reproducción por Spotify Connect desde un iPhone hacia una bocina de terceros conserva la posición exacta de la pista con un margen menor a un segundo.
3. El reproductor web funciona en las dos versiones más recientes de Chrome, Firefox, Safari y Edge, incluyendo la reproducción de contenido protegido por DRM.

**Priority**: High

**Justification**: Una porción significativa de la base de usuarios está en dispositivos Android de gama media y baja en mercados emergentes, que es justamente donde menos se prueba y donde más falla. Ignorar esta matriz significa que el producto funciona bien solo para quien lo desarrolla.

---

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Garantizar que personas con discapacidad visual, motriz o auditiva puedan usar la aplicación, cumpliendo con WCAG 2.1 nivel AA y con la legislación aplicable en los mercados donde opera.

**Examples**:

1. Toda la interfaz de reproducción es navegable y operable con VoiceOver (iOS) y TalkBack (Android), y cada control anuncia su etiqueta y su estado actual.
2. El contraste de texto sobre fondo cumple una relación mínima de 4.5:1 en el tema oscuro, incluidos los nombres de artista en gris sobre las tarjetas de álbum.
3. Todos los flujos principales se completan usando únicamente el teclado en el cliente web, con un indicador de foco visible en cada paso.

**Priority**: High

**Justification**: Una aplicación de audio tiene una proporción de usuarios con discapacidad visual mayor que el promedio de las apps: el producto no depende de la vista. Además existe obligación legal en varios mercados (ADA en Estados Unidos, European Accessibility Act), lo que convierte un fallo de accesibilidad en riesgo de litigio y no solo en un problema de calidad.

---

## Test Type: Localization and Internationalization Testing

**Category**: Non-Functional

**Purpose**: Validar que la aplicación funciona correctamente en los más de 180 mercados donde opera: idiomas, alfabetos, monedas, formatos de fecha, impuestos locales y —el punto más delicado— restricciones de catálogo por territorio.

**Examples**:

1. Con la interfaz en árabe, el diseño se invierte correctamente (RTL) y los controles de reproducción mantienen su orden lógico de avance y retroceso.
2. El precio de la suscripción se muestra en la moneda local con el impuesto correspondiente aplicado (por ejemplo, IVA de 16% en México) y coincide con el monto efectivamente cobrado.
3. Una pista licenciada únicamente para Estados Unidos aparece atenuada y no reproducible para una cuenta cuyo territorio de facturación es México, incluso si se accede mediante un enlace directo compartido.

**Priority**: High

**Justification**: El tercer ejemplo no es un problema cosmético de traducción: reproducir contenido fuera de su territorio licenciado es un incumplimiento contractual directo con el titular de los derechos. Ese solo caso justifica la prioridad alta de todo el tipo.

---

## Test Type: Reliability and Resilience Testing

**Category**: Non-Functional

**Purpose**: Comprobar que la aplicación se comporta de forma predecible ante condiciones adversas: redes intermitentes, pérdida total de conexión, cambio de Wi-Fi a datos móviles, batería baja, o caída de un servicio del backend.

**Examples**:

1. Al perder la conexión a mitad de una canción, el cliente continúa reproduciendo desde el búfer y, si la conexión no vuelve, cambia de forma automática a las pistas descargadas sin cerrar la aplicación.
2. Durante un cambio de Wi-Fi a red móvil, la reproducción no se interrumpe y el bitrate se ajusta a la baja de manera transparente.
3. Con el servicio de recomendaciones caído (probado mediante inyección de fallas), la pantalla de inicio se sirve desde caché y la reproducción sigue disponible: la degradación es parcial, no total.

**Priority**: High

**Justification**: La escucha ocurre en movimiento —metro, coche, gimnasio— donde la red es intermitente por definición. La resiliencia ante la mala conectividad no es un caso extremo, es la condición normal de operación de una parte importante de las sesiones.

---

## Test Type: API and Contract Testing

**Category**: Functional

**Purpose**: Verificar que los contratos entre los microservicios del backend, y entre el backend y los clientes, se respetan tanto en la respuesta correcta como en el manejo de errores y en la evolución de versiones. Aplica también a la API pública que consumen desarrolladores externos.

**Examples**:

1. El endpoint que devuelve una playlist responde con el esquema acordado y mantiene la compatibilidad hacia atrás cuando se agrega un campo nuevo; los clientes de versiones anteriores lo ignoran sin fallar.
2. Ante una petición con un token expirado, la API devuelve 401 con el cuerpo de error documentado, y no un 500 genérico que el cliente no sabe interpretar.
3. Se ejecutan pruebas de contrato dirigidas por el consumidor (Pact) entre el cliente móvil y el servicio de catálogo, de modo que un cambio incompatible en el productor rompa la build del productor antes de llegar a producción.

**Priority**: High

**Justification**: En una arquitectura de microservicios, el punto de falla más común no está dentro de cada servicio sino en la frontera entre ellos. Las pruebas de contrato detectan esas rupturas en integración continua, semanas antes de que se manifiesten como un defecto de sistema difícil de diagnosticar.

---

## Resumen de prioridades

| Tipo de prueba | Categoría | Prioridad |
| --- | --- | --- |
| Functional Testing | Funcional | Critical |
| Performance Testing | No funcional | Critical |
| Security Testing | No funcional | Critical |
| Regression Testing | Funcional | Critical |
| Usability Testing | No funcional | High |
| Compatibility Testing | No funcional | High |
| Accessibility Testing | No funcional | High |
| Localization / i18n Testing | No funcional | High |
| Reliability and Resilience Testing | No funcional | High |
| API and Contract Testing | Funcional | High |
