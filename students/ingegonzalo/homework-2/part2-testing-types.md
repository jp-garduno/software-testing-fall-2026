# Clasificación de los tipos de pruebas

## Pruebas funcionales

Las pruebas funcionales verifican que las funciones principales de Instagram se comporten exactamente como fueron diseñadas. Como el objetivo de la aplicación es permitir que los usuarios publiquen, exploren e interactúen con el contenido, cualquier error en estas funciones afectaria con la utilidad.

### Ejemplos

- Publicar una fotos con filtro, descripción y verificar que aparezca correctamente.
- Enviar un DM con una imagen y confirmar que llegue al usuario indicado.
- Comprobar que los "me gusta", comentarios y compartidos actualicen los contadores en tiempo real.

**Prioridad:** Crítica, ya que estas acciones representan la base del funcionamiento de la plataforma.

## Pruebas de rendimiento

Este tipo de pruebas evalúa que la aplicación mantenga un buen desempeño incluso cuando millones de personas la utilizan al mismo tiempo, especialmente durante eventos virales o de gran tráfico.

### Ejemplos

- El Feed principal debe cargar en pocos segundos con una conexión 4G.
- Un Reel de 60 segundos debe procesarse y publicarse rápidamente.
- El sistema debe soportar millones de usuarios concurrentes sin degradar los tiempos de respuesta.

**Prioridad:** Crítica, porque la velocidad influye directamente en la experiencia del usuario y en su permanencia dentro de la aplicación.

## Pruebas de seguridad

Las pruebas de seguridad buscan proteger las cuentas, los mensajes privados y la información personal frente a accesos no autorizados o ataques.

### Ejemplos

- La autenticación en dos pasos debe impedir el acceso usando únicamente una contraseña robada.
- El contenido de una cuenta privada no debe ser visible para personas no autorizadas.
- Los mensajes deben viajar protegidos contra intentos de interceptación.

**Prioridad:** Crítica, ya que una vulnerabilidad puede afectar a millones de usuarios y generar problemas legales y de confianza.

## Pruebas de usabilidad

Estas pruebas comprueban que la aplicación sea fácil de entender y utilizar para personas con diferentes edades y niveles de experiencia tecnológica.

### Ejemplos

- Un usuario nuevo debe poder crear su primera publicación sin ayuda externa.
- Las funciones interactivas de las historias deben ser fáciles de encontrar.
- La navegación entre Feed, Reels, Buscar y Perfil debe resultar clara y consistente.

**Prioridad:** Alta, porque una experiencia complicada puede provocar que los usuarios abandonen la plataforma.

## Pruebas de regresión

Las pruebas de regresión verifican que las nuevas funciones o correcciones no rompan características que ya funcionaban correctamente.

### Ejemplos

- Una actualización del editor de Reels no debe afectar la publicación de fotos.
- Una corrección en las notificaciones no debe impedir el envío de mensajes.
- Un cambio en el algoritmo de recomendaciones no debe provocar fallos en la sección Explorar.

**Prioridad:** Crítica, debido a que Instagram recibe actualizaciones constantes y es necesario evitar que reaparezcan errores corregidos anteriormente.

## Pruebas de compatibilidad

Estas pruebas aseguran que Instagram funcione correctamente en diferentes dispositivos, sistemas operativos y navegadores.

### Ejemplos

- La aplicación debe verse correctamente en versiones recientes y anteriores de iOS y Android.
- La reproducción de videos debe adaptarse a distintas resoluciones y tamaños de pantalla.
- La versión web debe funcionar de forma estable en Chrome, Safari, Firefox y Edge.

**Prioridad:** Alta, ya que la plataforma tiene usuarios con una gran variedad de dispositivos.

## Pruebas de accesibilidad

El objetivo es garantizar que personas con discapacidades visuales, auditivas, motoras o cognitivas puedan utilizar la aplicación siguiendo estándares como WCAG.

### Ejemplos

- Los lectores de pantalla deben identificar correctamente botones e imágenes con texto alternativo.
- Todos los elementos interactivos deben poder utilizarse con teclado o controles adaptados.
- Los colores de la interfaz deben mantener un contraste suficiente para facilitar la lectura.

**Prioridad:** Media, porque aunque no afecta a todos los usuarios por igual, es fundamental para ofrecer una experiencia inclusiva y cumplir con requisitos legales.

## Pruebas del sistema de recomendaciones

Instagram depende de algoritmos que deciden qué contenido aparece en el Feed, Explorar y Reels, por lo que también es necesario evaluar la calidad de esas recomendaciones.

### Ejemplos

- El contenido recomendado debe reflejar los intereses reales del usuario.
- El contenido reportado debe dejar de recomendarse en un tiempo razonable.
- El algoritmo debe evitar mostrar repetidamente las mismas publicaciones.

**Prioridad:** Alta, ya que estas recomendaciones influyen directamente en el tiempo que los usuarios pasan dentro de la aplicación y en su confianza en la plataforma.