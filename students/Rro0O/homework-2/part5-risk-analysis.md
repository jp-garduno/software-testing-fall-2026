# Part 5: Risk Analysis & Test Prioritization

App: **Instagram**

## Matriz de Riesgos

| # | Riesgo | Probabilidad | Impacto | Prioridad | Cómo mitigarlo |
|---|--------|---------------|---------|-----------|-----------------|
| 1 | Que subir fotos/videos falle o se corrompa el contenido | Media | Crítico | **Crítica** | Muchas pruebas de integración en todo el proceso de subida; lanzamientos poco a poco; revertir automático si suben los errores; probar en varios celulares y formatos. |
| 2 | Que se filtre contenido de una cuenta privada a alguien que no debería verlo | Baja | Crítico | **Crítica** | Pruebas rigurosas de permisos; auditorías de seguridad seguido; programa de recompensas por encontrar bugs; revisión de código estricta en todo lo de privacidad. |
| 3 | Que el feed/Explorar se caiga o vaya lentísimo cuando algo se vuelve viral | Media | Alto | **Alta** | Pruebas de carga simulando picos virales; infraestructura que escale sola; que la app muestre una versión simplificada en vez de caerse por completo. |
| 4 | Que los mensajes directos se retrasen, se pierdan o lleguen desordenados | Baja | Alto | **Alta** | Pruebas de integración enfocadas en casos raros de concurrencia; monitoreo en tiempo real con alertas; respaldo en el sistema de mensajería. |
| 5 | Que la moderación deje pasar contenido malo o, al revés, quite contenido que estaba bien | Media | Alto | **Alta** | Evaluar seguido qué tan preciso es el sistema de moderación; que haya revisión humana en los casos dudosos; proceso rápido para apelar; probar bien antes de lanzar cambios al modelo. |
| 6 | Que el cobro en la Tienda de Instagram falle o cobre mal | Baja | Crítico | **Crítica** | Pruebas dedicadas del flujo de pago con ambientes de prueba de los proveedores; revisiones de que los montos cuadren; pruebas de aceptación estrictas antes de activarlo en un país nuevo. |
| 7 | Que cambios nuevos rompan la accesibilidad para gente con discapacidad | Media | Media | **Media** | Revisiones automáticas de contraste y etiquetas en cada cambio; auditorías manuales de vez en cuando; que la accesibilidad sea un requisito antes de lanzar funciones nuevas. |
| 8 | Que haya errores de traducción o de diseño en algún país/idioma específico | Media | Media | **Media** | Pruebas con pseudo-traducciones desde el desarrollo; revisión de hablantes nativos en los países más importantes; pruebas visuales en varios idiomas, incluyendo los que se leen de derecha a izquierda. |

**Cómo se midió probabilidad/impacto:** Baja / Media / Alta / Crítica, tomando en cuenta qué tan seguido pasan cosas así y qué tan grave sería (cuánta gente afecta, si se puede arreglar fácil, y si hay problemas legales o de dinero de por medio).

## Orden de prioridad para las pruebas (de más a menos urgente)

1. **Seguridad y privacidad** (riesgo #2) — un error aquí es casi imposible de arreglar después y puede meter a la empresa en problemas legales serios.
2. **Pagos en la Tienda** (riesgo #6) — implica dinero real de la gente, un error aquí cuesta mucho y quita confianza.
3. **Subida de fotos/videos** (riesgo #1) — es literalmente para lo que la gente usa la app; si falla, se detiene todo.
4. **Moderación de contenido** (riesgo #5) — hay que cuidar tanto que no se cuele contenido malo como que no se censure de más.
5. **Mensajes directos** (riesgo #4) — se usan a diario, y aunque falle poco, cuando falla la gente se enoja mucho.
6. **Picos de tráfico viral** (riesgo #3) — no pasa tan seguido, pero cuando pasa es súper visible, así que igual hay que estar preparados.
7. **Traducción/región** (riesgo #8) — afecta a países específicos, se prioriza según qué tan grande es ese mercado.
8. **Accesibilidad** (riesgo #7) — importante y hasta legal en varios lugares, pero se revisa más con auditorías periódicas que en cada lanzamiento.

**Por qué este orden:** Se prioriza primero qué tan grave sería si algo sale mal (aunque sea poco probable) y después qué tan seguido podría pasar. Por eso algo como una fuga de privacidad, aunque sea poco probable, queda arriba de un error de traducción que puede pasar más seguido pero duele mucho menos.
