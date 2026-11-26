# Part 3: Testing Levels Strategy

Estrategia de pruebas para Spotify organizada por los cuatro niveles. La lógica que conecta los niveles es la pirámide de pruebas: muchas pruebas unitarias rápidas y baratas en la base, menos pruebas de integración, pocas de sistema (lentas y frágiles) y un conjunto muy acotado de aceptación enfocado en el valor de negocio.

---

## Unit Testing

**Scope**: Funciones, métodos y clases individuales, aisladas de sus dependencias mediante dobles de prueba (mocks y stubs). Sin red, sin base de datos, sin sistema de archivos. Cada prueba debe correr en milisegundos.

**What to Test**:

- **Lógica de cola de reproducción**: cálculo de la siguiente pista con modo aleatorio activo, repetición de pista, repetición de álbum y la interacción entre los tres.
- **Motor de facturación**: cálculo de prorrateo al cambiar de plan a mitad de ciclo, aplicación de descuentos de plan estudiante, cálculo de impuesto por territorio.
- **Selección adaptativa de bitrate**: dada una medición de ancho de banda y un tipo de red, decidir la calidad de audio a solicitar.
- **Contador de reproducciones**: la regla de negocio de qué constituye un *stream* válido (reproducción de al menos 30 segundos), incluyendo los casos límite de 29 y 30 segundos exactos.
- **Parseo y normalización de consultas de búsqueda**: acentos, mayúsculas, caracteres especiales y errores tipográficos.
- **Validadores de entrada**: longitud del nombre de playlist, formato de correo, fortaleza de contraseña.

**Tools**: JUnit 5 y Mockito para los servicios en Java; ScalaTest para los componentes en Scala; pytest para el pipeline de datos en Python; XCTest para iOS; JUnit y Robolectric para Android; Jest y React Testing Library para el cliente web. Cobertura medida con JaCoCo y con Istanbul.

**Coverage Goal**: 85% de cobertura de líneas a nivel global y 95% de cobertura de ramas en los módulos de facturación y de conteo de reproducciones, que son los de mayor consecuencia. La cobertura se trata como señal, no como meta: 100% de cobertura con aserciones triviales vale menos que 70% con aserciones significativas.

**Example Test Cases**:

1. `testSiguientePistaConAleatorioYRepetirAlbum`: con una cola de 10 pistas, modo aleatorio activo y repetición de álbum, al terminar la última pista la siguiente debe ser una del mismo álbum y no debe repetirse ninguna hasta agotar las diez.
2. `testProrrateoAlCambiarDePlan`: un usuario en plan individual (117 MXN/mes) que cambia a plan dúo (159 MXN/mes) el día 15 de un ciclo de 30 días debe recibir un cargo prorrateado de 21 MXN, no el precio completo del plan nuevo.
3. `testStreamValidoEnLimiteDe30Segundos`: una reproducción de 29.9 segundos no incrementa el contador de reproducciones; una de 30.0 segundos exactos sí lo hace.
4. `testBitrateBajaEnRedMovilLenta`: con un ancho de banda medido de 80 kbps sobre red móvil, el selector debe solicitar la calidad más baja disponible y nunca la calidad "muy alta".

**Estimated Number of Tests**: ~4,000 pruebas unitarias en el conjunto del backend y ~1,500 por cada plataforma cliente. Tiempo objetivo de ejecución de la suite completa por servicio: menos de 2 minutos.

---

## Integration Testing

**Scope**: La interacción entre dos o más componentes: un servicio con su base de datos, un servicio con otro servicio, el cliente con la API, y el sistema con proveedores externos (pasarela de pago, CDN, proveedor de DRM). Aquí ya hay red y persistencia reales, pero contra entornos de prueba y dobles de servicios externos.

**What to Test**:

- **Servicio de reproducción ↔ CDN**: solicitud y recepción de segmentos de audio, incluyendo el manejo de un nodo de CDN que responde con error.
- **Servicio de suscripciones ↔ pasarela de pago**: cobro exitoso, rechazo por fondos insuficientes, tiempo de espera agotado y webhook de confirmación diferida.
- **Servicio de catálogo ↔ base de datos y caché**: consistencia entre lo que devuelve Cassandra y lo que hay en Memcached tras una actualización de metadatos.
- **Productores y consumidores de Kafka**: un evento de reproducción emitido por el cliente llega al pipeline de regalías con todos sus campos y sin duplicarse.
- **Autenticación federada**: el flujo OAuth completo contra los proveedores de identidad externos.
- **Sincronización entre dispositivos**: el estado de reproducción que escribe el cliente móvil lo lee correctamente el cliente de escritorio.

**Tools**: Testcontainers para levantar Cassandra, PostgreSQL y Kafka reales en contenedores efímeros; WireMock para simular la pasarela de pago y demás servicios externos; Pact para pruebas de contrato dirigidas por el consumidor entre clientes y servicios; REST Assured y Postman/Newman para las pruebas de API; Spring Boot Test para el arranque de contexto parcial.

**Coverage Goal**: 100% de las integraciones críticas cubiertas (pago, reproducción, autenticación, emisión de eventos de regalías) y un contrato Pact verificado para cada par consumidor-productor en producción. No se mide cobertura de líneas en este nivel: se mide cobertura de *interfaces*.

**Example Test Cases**:

1. `testCobroRechazadoNoActivaPremium`: cuando la pasarela de pago responde con rechazo por fondos insuficientes, la cuenta permanece en free tier, se registra el intento fallido y se dispara el correo de reintento; ninguna pista se descarga en calidad premium.
2. `testEventoDeReproduccionLlegaAlPipelineDeRegalias`: al reproducir una pista 45 segundos, se publica exactamente un evento en el tópico de Kafka con el identificador de pista, el territorio, el tipo de cuenta y la duración; el consumidor de regalías lo procesa sin duplicar el conteo aunque el evento se reentregue.
3. `testFallbackDeCDNCaido`: si el nodo de CDN primario devuelve 503, el cliente solicita el segmento al nodo secundario y la reproducción continúa sin interrupción audible.
4. `testInvalidacionDeCacheTrasCambioDeMetadatos`: al corregir el nombre de un artista en el catálogo, la consulta siguiente devuelve el nombre nuevo y no el valor cacheado.

**Estimated Number of Tests**: ~900 pruebas de integración, más ~120 contratos Pact. Tiempo objetivo de ejecución: menos de 20 minutos en paralelo.

---

## System Testing

**Scope**: El sistema completo desplegado en un entorno equivalente a producción, probado de extremo a extremo desde la interfaz del usuario. Incluye tanto los flujos funcionales completos como los atributos no funcionales del sistema en conjunto: rendimiento, seguridad, compatibilidad y resiliencia.

**What to Test**:

- **Recorridos completos del usuario**: registro → búsqueda → reproducción → creación de playlist → descarga offline → cancelación de suscripción.
- **Escenarios multidispositivo**: iniciar la reproducción en el teléfono y transferirla a la computadora con Spotify Connect.
- **Comportamiento bajo carga**: pruebas de carga, de estrés y de resistencia (*soak*) sobre el sistema completo.
- **Seguridad a nivel de sistema**: pruebas de penetración, escaneo de vulnerabilidades y verificación del cifrado del contenido offline.
- **Resiliencia**: ingeniería del caos, apagando servicios y nodos para observar la degradación.
- **Matriz de compatibilidad**: ejecución de los flujos críticos en la granja de dispositivos.

**Tools**: Appium para automatización móvil multiplataforma; Playwright para el cliente web; BrowserStack o Firebase Test Lab como granja de dispositivos reales; k6 y Apache JMeter para carga; OWASP ZAP y Burp Suite para seguridad; Chaos Monkey para inyección de fallas; axe-core y Lighthouse para accesibilidad; Grafana y Prometheus para observar el sistema durante las corridas.

**Coverage Goal**: 100% de los flujos críticos de negocio automatizados y ejecutados en cada candidato a liberación, sobre los diez pares dispositivo/sistema operativo más representativos de la base instalada. Objetivos no funcionales: p95 de tiempo hasta el primer sonido por debajo de 500 ms, tasa de error por debajo de 0.1% bajo carga pico, cero vulnerabilidades críticas o altas abiertas.

**Example Test Cases**:

1. `testRecorridoCompletoDeSuscripcion`: un usuario nuevo se registra, inicia periodo de prueba, reproduce una canción sin anuncios, descarga una playlist, cancela la suscripción, y al terminar el periodo pagado la app vuelve a mostrar anuncios y las descargas quedan inaccesibles.
2. `testTransferenciaEntreDispositivos`: con la misma cuenta activa en teléfono y escritorio, transferir la reproducción desde el minuto 1:30 de una pista; el escritorio continúa dentro de un margen de un segundo y el teléfono pasa a modo de control remoto.
3. `testCargaPicoDeLanzamiento`: simular 5 millones de usuarios concurrentes reproduciendo el mismo álbum recién lanzado durante una hora; el p95 de latencia de reproducción se mantiene bajo 800 ms y ningún servicio crítico supera 80% de uso de CPU.
4. `testGeobloqueoDeContenido`: con una cuenta cuyo territorio es México, acceder por enlace directo a una pista licenciada solo para Estados Unidos; la pista aparece no reproducible y ninguna petición de audio llega al CDN.
5. `testResistenciaDeSesionLarga`: una sesión de reproducción continua de 12 horas no presenta fugas de memoria, no degrada la latencia y no provoca el cierre de la aplicación.

**Estimated Number of Tests**: ~250 escenarios de sistema automatizados, más ~15 escenarios de carga y ~30 de seguridad ejecutados por ciclo de liberación. Tiempo objetivo: menos de 4 horas en paralelo para la suite funcional.

---

## Acceptance Testing

**Scope**: Validación de que el sistema entregado satisface las necesidades reales del negocio y de los usuarios, y que cumple los requisitos contractuales, legales y regulatorios. La pregunta que responde este nivel no es "¿está bien construido?" sino "¿construimos lo correcto?".

**What to Test**:

- **Criterios de aceptación de cada historia de usuario**, escritos con las partes interesadas antes del desarrollo y expresados en lenguaje de negocio.
- **Pruebas alfa**: uso interno por empleados (*dogfooding*) antes de cualquier exposición externa.
- **Pruebas beta**: liberación gradual a un porcentaje de usuarios reales mediante *feature flags*, con recolección de métricas y retroalimentación.
- **Aceptación contractual y de cumplimiento**: exactitud del reporte de regalías frente a los sellos, respeto de las ventanas de exclusividad, conformidad con GDPR (exportación y borrado de datos personales).
- **Aceptación operativa**: que el equipo de operaciones cuente con alertas, tableros y procedimientos de reversión antes de la liberación.

**Tools**: Cucumber y SpecFlow para escenarios en Gherkin legibles por el negocio; TestRail para la gestión de casos manuales exploratorios; plataformas de beta (TestFlight en iOS, Google Play Beta en Android); herramientas de *feature flag* y experimentación (Confidence, LaunchDarkly) para el despliegue gradual; encuestas in-app y analítica de producto para las señales de aceptación.

**Coverage Goal**: 100% de los criterios de aceptación de las historias de la liberación verificados y firmados por el dueño de producto; 100% de los requisitos de cumplimiento normativo validados por el equipo legal; ninguna liberación al 100% de usuarios sin haber pasado por una fase beta con al menos 1% del tráfico y métricas de salud estables durante 72 horas.

**Example Test Cases**:

1. `Escenario: Un usuario premium escucha sin anuncios` — **Dado** que tengo una suscripción premium activa, **cuando** reproduzco cinco canciones consecutivas, **entonces** no se inserta ningún anuncio de audio ni visual en ningún momento.
2. `Escenario: Exportación de datos personales bajo GDPR` — **Dado** que soy un usuario en la Unión Europea, **cuando** solicito la descarga de mis datos, **entonces** recibo un archivo completo con mi historial de escucha, playlists y datos de cuenta dentro de los 30 días naturales que exige el reglamento.
3. `Escenario: Reporte de regalías correcto` — **Dado** un mes de reproducciones registradas, **cuando** el sello discográfico consulta su reporte, **entonces** el número de reproducciones por pista y territorio coincide exactamente con el conteo del pipeline de eventos, sin diferencias tolerables.
4. `Escenario: Respeto de ventana de exclusividad` — **Dado** un álbum con exclusividad de 14 días para suscriptores premium, **cuando** un usuario del free tier intenta reproducirlo el día 10, **entonces** se le ofrece la promoción de suscripción y la reproducción no inicia.

**Estimated Number of Tests**: ~200 escenarios de aceptación automatizados en Gherkin, más una fase beta por cada liberación mayor con un mínimo de 10,000 usuarios participantes.

---

## Resumen comparativo de los cuatro niveles

| Nivel | Quién lo ejecuta | Cuándo | Cantidad estimada | Tiempo de la suite |
| --- | --- | --- | --- | --- |
| Unit | Desarrollador | En cada commit | ~10,000 | < 2 min por servicio |
| Integration | Desarrollador / QA | En cada merge a main | ~900 + 120 contratos | < 20 min |
| System | QA | En cada candidato a liberación | ~250 + carga y seguridad | < 4 h |
| Acceptance | Producto / negocio / usuarios beta | Antes de liberar a producción | ~200 + fase beta | días |
