# Part 2: Testing Types Classification

App: **Instagram**

Para cada tipo de prueba pongo: categoría, para qué sirve, ejemplos, qué tan urgente es y por qué.

---

## 1. Pruebas Funcionales

- **Categoría:** Funcional
- **Para qué sirve:** Checar que las cosas hagan lo que se supone que deben hacer.
- **Ejemplos:**
  1. Subir una foto con texto y hashtags y que aparezca bien en el feed.
  2. Mandar un DM y que le llegue al otro, con su "visto" correcto.
  3. Darle "Seguir" a alguien y que el contador de seguidores se actualice al toque.
- **Prioridad:** Crítica
- **Por qué:** Si esto falla, la app básicamente no sirve para nada. Es lo primero que la gente usa.

## 2. Pruebas de Desempeño (Performance)

- **Categoría:** No funcional
- **Para qué sirve:** Ver qué tan rápido responde la app y si aguanta mucha gente usándola al mismo tiempo.
- **Ejemplos:**
  1. Que el feed cargue en 1-2 segundos con datos móviles normales.
  2. Que un Reel empiece a reproducirse casi al instante al hacer scroll.
  3. Que la app no se caiga cuando millones de personas la usan a la vez (por ejemplo, durante una final de futbol).
- **Prioridad:** Crítica
- **Por qué:** Con tantísimos usuarios, hasta un segundo de más en cargar hace que la gente se desespere y deje de usarla.

## 3. Pruebas de Seguridad

- **Categoría:** No funcional
- **Para qué sirve:** Encontrar huecos que alguien podría usar para robar info o meterse donde no debe.
- **Ejemplos:**
  1. Que alguien que no te sigue no pueda ver los posts de tu cuenta privada.
  2. Que si cierras sesión, ese "token" ya no sirva para nada.
  3. Meter código raro (inyecciones) en la biografía o en comentarios para ver si algo se rompe.
- **Prioridad:** Crítica
- **Por qué:** Ahí hay fotos, mensajes y datos personales de más de mil millones de personas. Una falla de seguridad es un desastre.

## 4. Pruebas de Usabilidad

- **Categoría:** No funcional
- **Para qué sirve:** Ver qué tan fácil es usar la app sin que te tengas que romper la cabeza.
- **Ejemplos:**
  1. Que alguien nuevo encuentre solito el botón para subir una foto.
  2. Que hacer tu cuenta privada tome máximo 3 toques.
  3. Que alguien que usa lector de pantalla pueda entender el feed gracias al texto alternativo de las imágenes.
- **Prioridad:** Alta
- **Por qué:** Aunque todo funcione bien "por dentro", si es confuso de usar la gente se va a otra app.

## 5. Pruebas de Regresión

- **Categoría:** Funcional
- **Para qué sirve:** Asegurar que lo nuevo que agregan no rompa lo que ya funcionaba.
- **Ejemplos:**
  1. Después de actualizar el editor de Reels, checar que subir fotos normales siga funcionando.
  2. Después de una actualización de mensajes, que los chats grupales viejos no pierdan su historial.
  3. Después de cambiar el algoritmo de Explorar, que el feed normal de la gente que sigues no se vuelva loco.
- **Prioridad:** Crítica
- **Por qué:** Instagram lanza cambios todo el tiempo, casi a diario. Sin esto es facilísimo romper algo sin darse cuenta.

## 6. Pruebas de Compatibilidad

- **Categoría:** No funcional
- **Para qué sirve:** Ver que la app funcione igual de bien en distintos celulares, pantallas y navegadores.
- **Ejemplos:**
  1. Que los Reels se vean bien tanto en un iPhone nuevo como en un Android viejito.
  2. Que los stickers de las Stories no se vean chuecos en pantallas de distinto tamaño.
  3. Que Instagram desde el navegador funcione igual en Chrome, Safari y Firefox.
- **Prioridad:** Alta
- **Por qué:** Hay muchísimos tipos de celulares distintos usando la app, sobre todo Android, y si no probamos en varios se nos puede ir gente.

## 7. Pruebas de Accesibilidad

- **Categoría:** No funcional
- **Para qué sirve:** Que la app la puedan usar personas con alguna discapacidad (visual, motriz, auditiva).
- **Ejemplos:**
  1. Que los botones de like, comentar y compartir tengan etiquetas para lectores de pantalla.
  2. Que el texto en las Stories tenga buen contraste sobre la foto de fondo.
  3. Que los videos tengan subtítulos disponibles.
- **Prioridad:** Media
- **Por qué:** Es importante y hasta obligatorio por ley en varios países, pero suele afectar a menos gente que un bug funcional grande.

## 8. Pruebas de Idioma/Región (Localización)

- **Categoría:** No funcional
- **Para qué sirve:** Checar que la app se vea y funcione bien en distintos idiomas y países.
- **Ejemplos:**
  1. Que el texto traducido no se salga de los botones (por ejemplo, en alemán las palabras son largas).
  2. Que las horas ("hace 2h") se muestren correctas según tu zona horaria e idioma.
  3. Que las reglas de contenido cambien según las leyes de cada país.
- **Prioridad:** Media
- **Por qué:** Instagram se usa en más de 100 países, así que esto importa, pero un bug de traducción no es tan grave como uno de seguridad.

## 9. Pruebas de Carga / Estrés

- **Categoría:** No funcional
- **Para qué sirve:** Ver qué tan lejos aguanta la app antes de romperse cuando hay un montón de gente conectada a la vez.
- **Ejemplos:**
  1. Simular 10 veces el tráfico normal cuando algo se vuelve viral y ver cuántos errores salen.
  2. Meter muchísimas subidas de fotos/videos al mismo tiempo y ver cómo se comporta.
  3. Probar qué pasa cuando alguien con millones de seguidores hace un post y se mandan millones de notificaciones de golpe.
- **Prioridad:** Alta
- **Por qué:** Los picos virales pasan seguido y sin avisar, y si la app se cae en ese momento es muy visible y le pega a la reputación.

## 10. Pruebas de Moderación de Contenido

- **Categoría:** Funcional (con un lado de calidad)
- **Para qué sirve:** Checar que el sistema que revisa el contenido detecte lo que sí viola las reglas, sin quitar cosas que están bien.
- **Ejemplos:**
  1. Que contenido claramente prohibido (violento, etc.) se detecte y se quite solo.
  2. Que contenido normal (por ejemplo, algo educativo) no se marque por error como prohibido.
  3. Que la moderación funcione bien en distintos idiomas y culturas, no solo en inglés.
- **Prioridad:** Alta
- **Por qué:** Si falla puede dejar pasar cosas malas o, al revés, censurar cosas que no debía, y ambas cosas generan mucho enojo de los usuarios.
