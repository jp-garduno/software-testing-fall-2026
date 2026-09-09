# Part 3: Testing Levels Strategy

App: **Instagram**

---

## 1. Pruebas Unitarias

**De qué se trata:** Probar piezas chiquitas de código por separado — una función, un botón, una utilería — sin depender de nada más alrededor. Por ejemplo: la función que valida el texto de una publicación, la que comprime una imagen, o un componente visual solito.

**Ejemplos de casos:**
1. Que si escribes una descripción de más de 2,200 caracteres, la app la rechace con el error correcto.
2. Que el contador de seguidores muestre "1.5M" en vez de "1500000".
3. Que la función que comprime imágenes deje el archivo del tamaño esperado sin que se vea horrible.
4. Que el contador de 24 horas de una Story avise correctamente cuando ya se venció.

**Herramientas recomendadas:**
- iOS: XCTest
- Android: JUnit + Mockito / Espresso
- Backend: pytest (si usan Python)
- Web: Jest + React Testing Library

**Cobertura estimada:** Como 75-85% de la lógica de negocio (validaciones, formateos, cálculos). La parte visual se cubre menos aquí porque se prueba más en los otros niveles.

---

## 2. Pruebas de Integración

**De qué se trata:** Ver que las distintas partes de la app se lleven bien entre sí — por ejemplo, que el celular hable bien con el servidor cuando subes una foto, o que el sistema de mensajes avise bien al sistema de notificaciones.

**Ejemplos de casos:**
1. Al subir una foto, que todo el proceso (subir → procesar → guardar → mostrar) termine con la foto visible y con un link válido.
2. Que cuando llega un mensaje nuevo, se dispare la notificación push correspondiente.
3. Que el sistema de Explorar junte bien la info de tus gustos y te regrese una lista de posts ordenada.
4. Que al comprar algo en la Tienda, se conecte bien con el sistema de pagos y quede confirmada la orden.

**Herramientas recomendadas:**
- Postman / Newman para probar las APIs
- Pact para probar que el celular y el servidor "hablen el mismo idioma"
- Ambientes de prueba con servicios simulados para no depender de todo en producción

**Cobertura estimada:** Como 60-70% de las conexiones importantes entre servicios, priorizando lo que tiene que ver con publicar, mensajes y pagos por encima de cosas menos críticas como analíticas internas.

---

## 3. Pruebas de Sistema

**De qué se trata:** Probar la app completa, de principio a fin, como la usaría alguien de verdad, en un ambiente parecido a producción.

**Ejemplos de casos:**
1. Un usuario nuevo se registra, sube foto de perfil, sigue a 3 cuentas y ve el feed lleno correctamente.
2. Alguien publica un Reel, aparece en su perfil, entra a Explorar y los likes/comentarios se actualizan en vivo.
3. Alguien reporta un post, entra a revisión, y si aplica se elimina y se le avisa a quien reportó.
4. Todo el flujo de comprar algo: ver la tienda, agregar al carrito, pagar y recibir confirmación.

**Herramientas recomendadas:**
- Appium (para celular) o las suites nativas de iOS/Android
- Selenium/Playwright para la versión web
- Cuentas de prueba con datos ya preparados para no empezar de cero cada vez

**Cobertura estimada:** Cubrir automatizados los 15-20 flujos más importantes (registro, publicar, story, reel, DM, seguir, comprar, reportar), y completar con pruebas manuales exploratorias para casos raros o funciones nuevas.

---

## 4. Pruebas de Aceptación

**De qué se trata:** El último filtro antes de lanzar algo: confirmar que lo que se construyó de verdad cumple lo que el negocio y los usuarios esperaban.

**Ejemplos de casos:**
1. Un grupo de usuarios beta prueba las nuevas herramientas de edición de Reels y confirma que sí son útiles antes de lanzarlas a todos.
2. El equipo de negocio confirma que el flujo de compra cumple las metas de ventas antes de activarlo en un país nuevo.
3. Un grupo de personas con discapacidad confirma que la app es usable con lector de pantalla antes de lanzar un cambio.
4. Se lanza un nuevo algoritmo de feed solo a una parte de los usuarios (A/B testing) y se acepta el cambio completo solo si mejora sin generar quejas.

**Herramientas recomendadas:**
- Sistemas de "feature flags" para activar cosas poco a poco
- TestFlight (iOS) y pruebas cerradas de Play Console (Android) para programas beta
- Dashboards de analítica para medir si se cumplen las metas antes de lanzar a todos

**Cobertura estimada:** Prácticamente el 100% de las funciones nuevas grandes pasan por este proceso escalonado (primero equipo interno, luego beta, luego poco a poco a todos) antes de un lanzamiento completo.
