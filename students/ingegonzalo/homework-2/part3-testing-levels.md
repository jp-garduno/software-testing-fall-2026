# Estrategia de niveles de pruebas

## Pruebas unitarias

Las pruebas unitarias se enfocan en verificar funciones, métodos o componentes individuales de forma aislada. Su objetivo es asegurar que cada pieza del código funcione correctamente antes de integrarse con el resto del sistema.

### ¿Qué se prueba?

- Validación de nombres de usuario y límites de caracteres en las publicaciones.
- Funciones de procesamiento de imágenes y videos, como filtros o generación de miniaturas.
- Lógica de negocio, por ejemplo, el incremento de los contadores de "me gusta" o comentarios.

**Herramientas:** Jest, XCTest y JUnit.

**Cobertura objetivo:** Alrededor del **80 %** del código relacionado con la lógica principal.

### Casos de prueba

- Verificar que un nombre de usuario con formato válido sea aceptado.
- Confirmar que un filtro aplicado a una imagen produzca el resultado esperado.
- Comprobar que el contador de "me gusta" aumente correctamente y maneje casos límite.

**Estimación:** Aproximadamente **500 pruebas unitarias**.

## Pruebas de integración

Las pruebas de integración verifican que diferentes componentes o servicios trabajen correctamente entre sí, garantizando que el intercambio de información sea consistente.

### ¿Qué se prueba?

- La comunicación entre el servicio de publicaciones y el almacenamiento multimedia.
- La interacción entre autenticación y mensajería.
- El envío de datos del Feed hacia el sistema de recomendaciones.

**Herramientas:** Postman, Newman, RestAssured y Pytest.

**Cobertura objetivo:** Cerca del **90 %** de los contratos definidos entre servicios.

### Casos de prueba

- Una foto subida debe almacenarse correctamente y aparecer con una URL válida.
- El token generado al iniciar sesión debe permitir acceder al servicio de mensajes.
- Reportar una publicación debe actualizar correctamente su estado de visibilidad.

**Estimación:** Alrededor de **150 pruebas de integración**.

## Pruebas de sistema

Las pruebas de sistema evalúan Instagram como un producto completo, comprobando que todos sus componentes funcionen juntos y cumplan tanto los requisitos funcionales como los no funcionales.

### ¿Qué se prueba?

- Flujos completos de usuario, desde el registro hasta las notificaciones.
- Rendimiento, seguridad y compatibilidad entre plataformas.
- Consistencia de los datos entre la aplicación móvil y la versión web.

**Herramientas:** Selenium, Appium, JMeter, k6 y OWASP ZAP.

**Cobertura objetivo:** Aproximadamente el **95 %** de los casos de uso críticos.

### Casos de prueba

- Un usuario nuevo debe poder registrarse, publicar contenido y visualizarlo en todos los dispositivos.
- El sistema debe mantener tiempos de respuesta aceptables bajo una alta carga de usuarios.
- Las publicaciones de una cuenta privada no deben ser visibles para usuarios no autorizados.

**Estimación:** Cerca de **200 escenarios**.

## Pruebas de aceptación

Las pruebas de aceptación son la última etapa antes del lanzamiento y buscan confirmar que la aplicación cumple con los requisitos del negocio y las expectativas de los usuarios reales.

### ¿Qué se prueba?

- Cumplimiento de los requisitos definidos por el producto.
- Experiencia de usuarios beta con nuevas funciones.
- Cumplimiento de normativas de privacidad y requisitos legales.

**Herramientas:** TestRail, pruebas exploratorias manuales, TestFlight y Google Play Beta.

**Cobertura objetivo:** Validar el **100 %** de los criterios de aceptación antes de cada lanzamiento importante.

### Casos de prueba

- Los usuarios beta deben confirmar que las nuevas herramientas de edición de Reels son fáciles de utilizar.
- El proceso de compra en Instagram Shop debe completarse sin salir de la aplicación.
- Los usuarios europeos deben visualizar correctamente los avisos de consentimiento antes de crear una cuenta.

**Estimación:** Alrededor de **50 escenarios de aceptación** por cada ciclo de lanzamiento importante.