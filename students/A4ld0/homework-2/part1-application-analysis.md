# Parte 1: Análisis de la aplicación

## Aplicación: TikTok

### Propósito

TikTok es una plataforma social centrada en descubrir, crear y compartir contenido audiovisual. Para este trabajo se analiza principalmente la experiencia de videos en su aplicación móvil y, como superficie complementaria, su versión web. El recorrido principal consiste en abrir la aplicación, explorar contenido, reproducir un video e interactuar con él. Otro recorrido esencial permite que un creador prepare una publicación y decida quién puede verla.

### Usuarios objetivo

La plataforma reúne espectadores que buscan entretenimiento o aprendizaje, creadores que producen contenido y comunidades que comparten intereses. También participan marcas y organizaciones que quieren comunicarse con una audiencia. Estos grupos tienen necesidades diferentes: un espectador espera reproducción fluida; un creador necesita publicar sin perder su trabajo; y una persona preocupada por su privacidad necesita comprender y controlar la visibilidad de sus publicaciones. Las restricciones aplicables a cada cuenta deben considerarse al definir los resultados esperados.

### Funciones principales

1. Registro, inicio de sesión y administración del perfil.
2. Exploración de videos mediante un feed personalizado y cuentas seguidas.
3. Reproducción de contenido y navegación entre publicaciones.
4. Creación y publicación de videos con descripción.
5. Búsqueda de contenido y cuentas.
6. Interacciones mediante comentarios, “me gusta” y seguimiento.
7. Configuración de privacidad de cuenta y publicaciones.
8. Controles de interacción, como administración de comentarios y mensajes.

Los controles de privacidad enumerados se encuentran documentados en el [centro de ayuda de TikTok](https://support.tiktok.com/en/account-and-privacy/account-privacy-settings/privacy-controls?lang=en). Los escenarios concretos deben ajustarse a las opciones habilitadas para la cuenta de prueba.

### Plataforma y tecnología

El alcance contempla clientes móviles Android e iOS, además del navegador web. No se afirma que TikTok utilice un lenguaje, framework o base de datos particular: no se dispone de evidencia sobre su implementación interna. Para planificar las pruebas se supone una arquitectura conceptual con clientes, servicios de autenticación, almacenamiento de contenido y distribución de video. Esta separación ayuda a identificar interfaces, pero no representa un diagrama confirmado de producción.

### Funciones críticas

La autenticación y la autorización son críticas porque protegen cuentas y contenido privado. La reproducción y carga del feed sostienen la experiencia principal: si fallan, el usuario no puede consumir contenido. La publicación también es esencial, especialmente ante interrupciones de red que podrían provocar pérdida o duplicación de videos.

La estrategia da máxima prioridad a impedir accesos no autorizados y a respetar la audiencia seleccionada. Después evalúa continuidad de reproducción, integridad de publicaciones e interacciones. También considera accesibilidad y facilidad de uso, ya que una función técnicamente correcta pierde utilidad cuando las personas no pueden encontrarla, entenderla o utilizarla.
