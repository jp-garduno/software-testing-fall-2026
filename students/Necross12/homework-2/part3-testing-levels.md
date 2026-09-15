## Pruebas unitarias

[//]: # (## Pruebas unitarias)

**Alcance **: Funciones/métodos/componentes individuales

**Qué se debe probar**:

- Funciones básicas del video (adelantar, atrasar, pausar y reproducir)
- Sanitización de los campos de formularios (verificar que todo esté en orden y cómo se procesa)
- Formato de validación

**Tools**: Git Actions, Jenkins, .test

**Coverage Goal**: 45

**Objetivo **:

1. Probar en un módulo de prueba con un video precargado
2. Probar entradas de texto y verificar que den una salida correcta (cómo se va a guardar), evitando vulneraciones
3. Función para validar la entrada de datos según el formato, como .txt, .png, .mp4

**Estimated Number of Tests**:  500

---

## Integration Testing
[//]: # (## Pruebas de integración)

**Alcance **: Módulos (secciones), APIs, bases de datos

**Qué se debe probar**:

- Login: probar iniciar sesión con diferentes usuarios, de forma correcta e incorrecta, para ver qué sucede
- Probar que el filtro arroje resultados adecuados, probando los diversos filtros con los elementos que deberían existir 
- Probar que se pueda reproducir una película de la base de datos y aplicar las funciones básicas (similar a los comandos de un bot de Discord)

**Tools**: Base de datos, agentes

**Coverage Goal**: 25

**Objetivo **:

1. Probar con la base de datos que los usuarios sean accesibles y traigan la información pertinente, probando diversas contraseñas y usuarios correctos e incorrectos
2. Probar los filtros con la base de datos, esperando un resultado en menos de 1 segundo con los 20 resultados principales que cumplan con los datos
3. Seleccionar una película aleatoria de la base de datos (puede ser por su ID) y hacer que se traiga y se abra

**Estimated Number of Tests**: 100

---
<!-- (aqui ya hay interfas) /-->
## System Testing

[//]: # (## Pruebas de sistema)

**Alcance **: Probar el sistema en partes concretas, interfaz y carga de elementos

**Qué se debe probar**:

- Sistema de registro de nuevo usuario (incluyendo el pago)
- Provocar ataques
- Seleccionar una película desde el filtro
- 
**Tools**: QA, tester, herramienta para ver mensajes en consola, agente

**Coverage Goal**: 20

**Objetivo **:

1. Verificar cómo se guarda la información desde que se presiona el botón de registrarse hasta llegar al home
2. Detectar las vulnerabilidades de la aplicación para encontrar debilidades en la forma de guardar los datos de los usuarios y de los pagos, y cerrar entradas traseras
3. En el home, seleccionar la barra de búsqueda, medir el tiempo que tarda en dar el resultado (cuando deba haberlo) y abrir el pop-up de información para reproducirla

**Estimated Number of Tests**: 20

---

## Acceptance Testing
[//]: # (## Pruebas de aceptación)

**Alcance**: Toda la aplicación

**Qué se debe probar**:

- Alfa interna
- Beta interna
- Beta externa

**Tools**: Usuarios reales, feedback y fe

**Coverage Goal**: 10 (cuando tienes el 90 % solo falta el otro 90 %)

**Objetivo **:

1. Ver cómo queda el producto final para el equipo, áreas de mejora de UX/UI, e iniciar a probar las funciones
2. El equipo de desarrollo, principalmente los testers y los de QA, busca todas las posibles mejoras y que se cumplan los requerimientos para implementar antes del lanzamiento
3. Feedback de los usuarios para mejorar los próximos features o antes del lanzamiento (ver si ya se puede lanzar o se tendrá que atrasar)

**Estimated Number of Tests**:  5