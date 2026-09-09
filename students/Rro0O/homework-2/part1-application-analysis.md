# Part 1: Application Selection & Analysis

## App elegida: Instagram

**Tipo:** App real que ya existe y todos usamos.

## De qué se trata

Instagram es la app donde subes fotos y videos para que tus amigos (o el mundo entero, si tu cuenta es pública) los vean. Además de eso tiene Stories (fotos/videos que se borran en 24 horas), Reels (videos cortitos al estilo TikTok), mensajes directos para chatear, y hasta una parte de compras donde puedes ver y comprar productos de marcas y creadores. La usa muchísima gente: gente normal, influencers, negocios chicos y marcas grandes.

## Quién la usa

- **Gente normal (13 años en adelante):** suben fotos de su vida y siguen a amigos, familia y cuentas que les gustan.
- **Creadores de contenido / influencers:** buscan hacer crecer su audiencia y ganar dinero con marcas o con las herramientas que Instagram les da.
- **Negocios y marcas:** usan cuentas de negocio para anunciarse y vender directo desde la app.
- **Anunciantes:** pagan por anuncios que aparecen en el feed, stories, reels, etc.

## Funciones principales (al menos 5)

1. **Publicar en el feed** — subes foto o video con texto, hashtags, ubicación y puedes etiquetar a otras cuentas.
2. **Stories** — fotos/videos que duran solo 24 horas, con stickers, encuestas, música, etc.
3. **Reels** — videos cortos verticales que se recomiendan solos según lo que a ti te gusta.
4. **Mensajes directos (DM)** — chats uno a uno o en grupo, con texto, fotos, notas de voz y videollamadas.
5. **Explorar** — una pestaña que te muestra contenido de cuentas que no sigues, basado en tus gustos.
6. **Tienda de Instagram** — puedes ver y comprar productos directo desde posts o reels.
7. **Live** — transmitir en vivo con comentarios y reacciones en tiempo real.

## Con qué está hecha (lo que se sabe públicamente)

- **Apps móviles:** nativas para iOS y Android, pensadas para funcionar bien hasta en celulares viejos o con internet lento.
- **Servidores:** una mezcla de tecnologías (Python, C++, Java, y cada vez más Rust) porque manejan una cantidad brutal de tráfico.
- **Bases de datos:** varias combinadas, unas para guardar info y otras para que todo cargue rápido (cache).
- **Manejo de fotos/videos:** infraestructura propia para comprimir y repartir el contenido rápido en todo el mundo.
- **Inteligencia artificial:** modelos que deciden qué te muestran en el feed/explorar/reels, y que ayudan a detectar contenido que no debería estar ahí.

## Lo más importante que no puede fallar

- **Iniciar sesión y seguridad de la cuenta** — login, verificación en dos pasos, recuperar tu cuenta si la pierdes.
- **Subir contenido y que se vea bien** — que las fotos/videos suban rápido y se vean bien sin importar el celular o la conexión.
- **Que el feed/explorar/reels te muestren cosas relevantes** — si el algoritmo falla, la gente deja de usar la app.
- **Que los mensajes lleguen** — en tiempo real y sin perderse.
- **Privacidad y moderación** — bloquear, reportar, y quitar contenido que no debería estar.
- **Pagos en la tienda** — que cobren bien y no haya errores con el dinero.
- **Notificaciones** — que avisen a tiempo sin ser molestas.

Instagram es un buen ejemplo para esta tarea porque tiene de todo: mensajería en tiempo real, algoritmos, fotos/videos pesados, pagos y millones de usuarios al mismo tiempo. Así que se pueden aplicar prácticamente todos los tipos y niveles de pruebas que vimos en clase.
