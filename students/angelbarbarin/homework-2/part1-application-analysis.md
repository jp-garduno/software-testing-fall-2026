# Part 1: Application Selection & Analysis

**Opción elegida**: Option A — aplicación existente que uso regularmente.

## Application: Spotify — Plataforma de Streaming de Audio

### Purpose

Spotify es una plataforma de streaming que da acceso bajo demanda a un catálogo licenciado de música, podcasts y audiolibros. El usuario no compra ni descarga archivos de forma permanente: paga una suscripción (o tolera anuncios) a cambio de un derecho de reproducción temporal sobre un catálogo que la empresa licencia de sellos discográficos, distribuidoras y titulares de derechos.

Esa distinción es el eje de todo el análisis de pruebas que sigue. Spotify no es una app de reproducción de archivos con una tienda encima; es un sistema de *cumplimiento de licencias en tiempo real* que además debe sonar bien. Cada reproducción tiene que ser contabilizada correctamente porque de esa contabilidad dependen las regalías que se pagan a los artistas, y cada pista tiene que estar disponible solo en los territorios donde su licencia lo permite. Un defecto en el reproductor molesta al usuario; un defecto en el conteo de reproducciones o en el geobloqueo tiene consecuencias contractuales y legales.

### Target Users

- **Oyentes gratuitos (free tier)**: acceso con anuncios, saltos limitados y sin descarga offline. Es el segmento más numeroso y el que genera la mayor carga de tráfico por usuario monetizado.
- **Suscriptores premium (individual, dúo, familiar, estudiante)**: sin anuncios, con descarga offline y audio de mayor calidad. Es el segmento que genera prácticamente todo el ingreso.
- **Artistas y sellos discográficos**: usan Spotify for Artists para subir música, revisar métricas de audiencia y verificar regalías.
- **Creadores de podcasts**: publican, monetizan e insertan anuncios dinámicos en sus episodios.
- **Anunciantes**: compran inventario publicitario segmentado por demografía, ubicación y hábitos de escucha.

### Key Features

1. **Registro y autenticación**: cuenta propia, inicio de sesión federado (Google, Facebook, Apple), y sesiones simultáneas en múltiples dispositivos.
2. **Búsqueda y navegación del catálogo**: búsqueda por canción, artista, álbum, género, letra o podcast, con autocompletado y tolerancia a errores de escritura.
3. **Reproducción de audio en streaming**: buffering adaptativo, cambio dinámico de bitrate según el ancho de banda, gapless playback y crossfade.
4. **Gestión de playlists**: creación, edición, colaboración entre usuarios, playlists públicas y privadas, y reordenamiento de pistas.
5. **Recomendaciones algorítmicas**: Discover Weekly, Release Radar, Daylist y radio por artista, generadas a partir del historial de escucha.
6. **Modo offline**: descarga cifrada de pistas para suscriptores premium, con revalidación periódica de la licencia.
7. **Facturación y suscripciones**: alta, cambio de plan, renovación automática, periodos de prueba, cancelación y reembolsos.
8. **Spotify Connect**: transferencia de la reproducción entre teléfono, computadora, bocina inteligente, consola y automóvil sin cortar el audio.
9. **Funciones sociales**: perfiles, seguimiento de amigos, sesiones grupales (Jam) y compartir en redes.
10. **Inserción de anuncios**: audio y display para usuarios del free tier, con segmentación y conteo de impresiones.

### Technology Stack

Spotify es un sistema distribuido multiplataforma. Los clientes son nativos (Swift/Objective-C en iOS, Kotlin/Java en Android), de escritorio (una capa web sobre Chromium Embedded Framework) y web (React con TypeScript). El backend es una arquitectura de microservicios escrita principalmente en Java, Scala y Python, comunicados por gRPC y por eventos sobre Apache Kafka, y desplegados en Google Cloud Platform sobre Kubernetes. La persistencia combina Cassandra y PostgreSQL, con memoria caché en Memcached. El audio se entrega por CDN con el códec Ogg Vorbis y AAC, y el contenido descargable se protege con DRM (Widevine). El pipeline de recomendaciones usa BigQuery, Apache Beam y modelos de aprendizaje automático entrenados fuera de línea.

### Critical Functions

Las funciones misión-crítica —aquellas cuya falla degrada el producto hasta hacerlo inservible o expone a la empresa legal o financieramente— son cuatro:

1. **Reproducción de audio ininterrumpida**: es *el* producto. Si el audio se corta, se salta o no arranca, nada más importa.
2. **Autenticación y gestión de sesión**: la puerta de entrada a todo lo demás y el punto donde vive la información de la cuenta.
3. **Facturación y cobro de suscripciones**: un cobro duplicado, un cobro después de cancelar o un premium que no se activa tras pagar generan pérdida de confianza, reembolsos y quejas ante reguladores.
4. **Conteo de reproducciones y control de licencias por territorio**: alimenta el pago de regalías y el cumplimiento contractual con los titulares de derechos. Es la función menos visible para el usuario y la de mayor consecuencia para el negocio.

Funciones importantes pero no críticas —recomendaciones, funciones sociales, letras sincronizadas— pueden degradarse temporalmente sin que el usuario pierda el valor central del servicio, y por eso reciben menor prioridad de prueba.
