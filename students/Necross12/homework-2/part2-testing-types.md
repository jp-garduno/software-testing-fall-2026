# Pruebas 
## Test Type: Pruebas de humo

**Categoría**: Funcional

**Objetivo**:
Revisar que el núcleo más básico de la de la aplicación funcionó de manera adecuada y esperada, antes de seguir.

**Ejemplos**:

1. Poner en pausa/reproducir un video precargado
2. Seleccionar adelantar, atrasar o poner un minuto específico
3. Cambiar pista de audio y/o activar subtítulos

**Prioridad**: Crítica

**Justificación**:
Ya que representan las funciones básicas y más esperables de la app, las cuales deberían poder lograrse sin mucho esfuerzo con un archivo de prueba, pero si fallan, afectarían de forma grave y directa la experiencia del usuario.

---

## Test Type: Prueba de usabilidad

**Categoría**: No funcional


**Objetivo**:
Al ser una plataforma familiar que apunta a todo público, es necesario que sea fácil de usar e interactuar con ella, de modo que tanto niños como adultos no tengan problemas al utilizarla y puedan seguir dentro del ecosistema.


**Ejemplos**:


1. Probar el happy path desde el ingreso de sesión hasta ver una película/serie específica, con personas de edades variadas.
2. Seleccionar un grupo de prueba para ver qué interfaz les resulta más atractiva (ya que, al ser una app de público general, es importante ser del agrado de la mayoría de personas).
3. Accesibilidad: Dentro de sus ajustes, incluye un gran número de ajustes para dar una mejor experiencia como:
* modo infantil (solo elementos de público general o menor).
* Filtros para personas daltónicas o con problemas de visión
* Compatibilidad con lectores de pantalla y descripciones de audio
  Por lo cual estas medidas de accesibilidad tienen que ser probadas.


**Prioridad**: Media

**Justificación**:
Netflix es una aplicación con un público objetivo muy amplio, desde niños de 12 años hasta personas de 50 años, que ven como mínimo una película o capítulo de serie por semana. Por lo tanto, la usabilidad es algo vital para destacarse en el mercado y poder atraer y retener a más gente, haciendo que la app se vea bien y se sienta bien al ser usada.

---

## Test Type: Rendimiento

**Categoría**: No funcional

**Objetivo**:
Ya que la app maneja archivos pesados, como puede ser el video 4K o renderizar múltiples datos a la vez, es importante poder optimizar estos elementos para que carguen a la mejor rápida posible y le den al usuario una sensación de fluidez.

**Ejemplos**:

1. Carga progresiva del archivo (cargar el video lo suficiente para poder reproducirlo progresivamente mientras se esté reproduciendo a la calidad solicitada, y que guarde el suficiente retroceso para poder retroceder sin cargar todo de nuevo).
2. Poder cargar la información de las películas en la barra de búsqueda sin retraso (ya que cuenta con más de 7000 títulos), deben cargar correctamente en la barra de búsqueda, ya sea que se busque actor, título, género o cualquier otro campo que esté como metadata; es importante que traiga la respuesta rápidamente.
3. Que se reflejen rápidamente las transacciones, por ejemplo el pago de la membresía, para poder tener acceso a la cuenta lo más rápido posible y así que el usuario tenga una buena experiencia al usar la plataforma y no se estrese por la lentitud del pago.

**Prioridad**: Alta

**Justificación**:
En el caso del video y el pago, es sumamente importante que sean rápidos, ya que uno repercute en la experiencia del MVP y en qué tan confiable le parece la página, mientras que entre más tarde en reflejarse la compra, más expectativa negativa se puede generar. Por otro lado, la carga de datos también es importante para la página, pero no es tan vital (yo la pondría en medio).

---

## Test Type: Seguridad

**Categoría**: No funcional

**Objetivo**:
Ya que se manejan datos sensibles, como datos de tarjeta de crédito/débito o información privada de los usuarios (nombre, cumpleaños y dirección), proteger la información es vital para evitar cualquier problema de filtración de datos, al igual que proteger el contenido para evitar problemas de copyright en el futuro.

**Ejemplos**:

1. Revisar que los permisos estén bien configurados y que no cualquier persona pueda acceder a páginas que requieran ser administrador o superadministrador, sino solo el rango adecuado.
2. Intentar atacar el sistema para obtener datos, como lo haría un hacker.
3. Protección de propiedad intelectual: evitar que las personas puedan extraer los vídeos o tomar capturas de pantalla en el sitio.


**Prioridad**: Alta

**Justificación**:
Los problemas legales que pueden surgir por una mala seguridad son muy graves, desde incumplimiento de contrato hasta demandas colectivas por la filtración, por lo cual es muy importante evitar tener problemas en el futuro contando con una estructura sólida.
---

## Test Type: Regresión

**Categoría**: Funcional

**Objetivo**:
Es importante corregir los errores, pero también lo es que esos cambios realizados en el código no generen problemas a futuro ni afecten funciones del módulo que ya funcionaban correctamente.

**Ejemplos**:

1. Volver a hacer las pruebas de humo en las funciones/módulos correspondientes (con o sin modificaciones, dependiendo del caso).
2. Hacer la prueba individual de la función/módulo modificado.
3. Revisar las funciones o módulos que usaban anteriormente este elemento para corregir los errores y volver a probarlos.

**Prioridad**: Alta

**Justificación**:
Es importante que, cuando se corrija algo, quede bien hecho, ya que si termina teniendo problemas sería similar a nunca haberlo corregido. Además, si se manda a corregir, primero se prioriza lo más importante, por lo cual le doy prioridad alta, ya que lógicamente primero se atiende lo más relevante.

---

## Test Type: Aceptación

**Categoría**: Funcional

**Objetivo**:
Es importante saber si nuestra app es aceptada por nuestro público de prueba, además de que el equipo de QA y los testers realicen todo el recorrido; esto con el fin de ver la aceptación del producto, conocer la opinión de la gente al respecto y detectar dónde se puede mejorar.

**Ejemplos** (al menos 3):

1. Alfa interna, para ver cómo se va desarrollando el proyecto.
2. Beta interna, para ver cómo se ha desarrollado la aplicación por completo, con la ayuda de testers, y observar cómo se comporta el proyecto ante posibles errores futuros.
3. Beta cerrada externa, probar con personas que encajen en nuestro esquema de cliente final para conocer sus opiniones y poder hacer cambios (si es necesario) con base en el feedback, ajustando el desarrollo según nuevas perspectivas o hallazgos.

**Prioridad**: Crítica

**Justificación**:
Es sumamente importante ver cómo reacciona la gente a la aplicación y que esta funcione como se tiene planeado, ya que una app que no cumpla con las expectativas de nuestro público nunca va a funcionar; asimismo, una aplicación que no funcione como conjunto, sino solo en parte, tampoco podrá retener al público.

---

## Test Type: Compatibilidad

**Categoría**: No funcional

**Objetivo**:
Estas pruebas buscan comprobar la portabilidad del programa en diversos sistemas y entornos, lo cual es importante para Netflix, ya que es una plataforma disponible en casi todos los equipos modernos.

**Ejemplos**:

1. Probar la plataforma en diversos navegadores (Chrome, Opera, Safari).
2. Probar la plataforma en diferentes equipos (PlayStation 5, Switch 2, Xbox Series S).
3. Probar Netflix en celulares de diversas categorías (iOS, Android, gama alta, media y baja).

**Prioridad**: Media-Alta

**Justificación**:
Es importante que la plataforma funcione en todos los dispositivos que dice soportar, pero es más importante dar prioridad a los elementos que las personas usarán con mayor frecuencia, como computadoras, celulares y/o smart TV, y dejar en segundo plano los menos relevantes, como consolas de videojuegos, smartwatches o un refrigerador.

---

## Test Type: Integración

**Categoría**: Funcional

**Objetivo**:
Es necesario que los módulos funcionen de forma conjunta, ya que resulta inútil que funcionen de manera individual (como los de seguridad, usuario, reproducción de series y/o películas, manejo de la base de datos ...) si no pueden funcionar en conjunto.

**Ejemplos**:

1. Hacer login con varias cuentas y diferentes permisos, y verificar que las funciones de bloqueo de página por rol estén activas y funcionen correctamente, además de probar el bloqueo regional.
2. Que aparezca de forma correcta, según el tipo de membresía, la opción de calidad máxima y/o los anuncios.
3. Que el usuario cree una cuenta nueva, realice el pago inicial y sea redirigido a la página principal sin fuga de información ni inconvenientes.

**Prioridad**: Alta

**Justificación**:
Porque si los módulos funcionan bien de manera individual, deberían poder funcionar también en conjunto para realizar las acciones esperadas por los usuarios, como ver una serie o iniciar sesión sin verse afectados por errores imprevistos o fallas en la lógica.