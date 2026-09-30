# Instagram

## Plataforma de redes sociales y contenido multimedia

Instagram es una aplicación de redes sociales diseñada para compartir fotos, videos y contenido de formato corto, como los Reels. Además de permitir que los usuarios publiquen contenido para sus seguidores, también ofrece mensajería privada, historias temporales, una sección de exploración basada en recomendaciones y funciones de compra integradas para que las empresas puedan vender productos directamente desde la aplicación.

## Usuarios objetivo

Los principales usuarios de Instagram son:

- Personas que comparten contenido personal.
- Creadores de contenido e influencers que buscan hacer crecer su audiencia.
- Empresas que promocionan productos mediante publicidad o Instagram Shop.
- Usuarios que consumen contenido sin publicar con frecuencia.

## Funciones principales

Entre las características más importantes de la plataforma se encuentran:

- Registro e inicio de sesión con autenticación en dos pasos.
- Gestión de perfiles de usuario.
- Publicación y edición de fotos y videos con filtros.
- Creación y visualización de Reels.
- Mensajería privada con texto, imágenes, notas de voz y mensajes temporales.
- Historias con encuestas, preguntas y otros elementos interactivos.
- Sistema de búsqueda y exploración basado en algoritmos de recomendación.
- Interacciones mediante "me gusta", comentarios, compartidos y guardados.
- Instagram Shop para realizar compras dentro de la aplicación.
- Sistema de notificaciones y herramientas para reportar o moderar contenido.

## Tecnologías utilizadas

Instagram está disponible en **iOS**, **Android** y versión **web**. Su infraestructura utiliza aplicaciones móviles nativas, React para la versión web y sistemas distribuidos de gran escala similares a los empleados por Meta, con tecnologías como **PHP/Hack**, **Python**, **GraphQL**, almacenamiento distribuido y redes de distribución de contenido (CDN). Además, emplea modelos de aprendizaje automático para personalizar el Feed, Explore y Reels.

## Funciones críticas

Existen funciones que son esenciales para el funcionamiento de la plataforma y que no deberían fallar:

- **Autenticación y seguridad:** Evita accesos no autorizados y permite recuperar cuentas de forma segura.
- **Carga y visualización de contenido:** Es el núcleo de la aplicación, por lo que cualquier falla afecta directamente su utilidad.
- **Mensajería privada:** Los mensajes deben entregarse correctamente y en el orden adecuado.
- **Feed personalizado:** Debe responder con rapidez incluso cuando millones de personas utilizan la plataforma al mismo tiempo.
- **Pagos en Instagram Shop:** Deben procesarse de forma confiable para evitar pérdidas económicas.
- **Controles de privacidad:** Deben respetar exactamente la configuración elegida por cada usuario.

## ¿Por qué es un buen caso de estudio?

Debido a que Instagram cuenta con miles de millones de usuarios y procesa interacciones en tiempo real, representa un caso de estudio muy completo para las pruebas de software. La plataforma requiere pruebas funcionales, de rendimiento, seguridad, escalabilidad y regresión para mantener la estabilidad de un servicio que se actualiza de forma continua y debe responder de manera confiable a una enorme cantidad de usuarios simultáneamente.