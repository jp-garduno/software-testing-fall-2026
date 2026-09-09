# Parte 5: Riesgos y priorización

## 5.1 Risk Matrix

Estas valoraciones son hipótesis de planificación, no incidentes observados en TikTok.

**Likelihood**: Low = requiere condiciones poco habituales; Medium = plausible en uso normal; High = frecuente en las condiciones contempladas.

**Impact**: Low = molestia menor; Medium = dificultad con alternativa; High = bloqueo de un recorrido esencial o pérdida de trabajo; Critical = exposición de contenido privado o control indebido de una cuenta.

**Priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low). Todo impacto Critical recibe P0. Impacto High recibe P1 con probabilidad Medium/High y P2 con Low; impacto Medium recibe P2 y Low recibe P3. No se asignan prioridades bajas artificialmente a riesgos graves.

| Risk | Likelihood | Impact | Priority | Mitigation Strategy |
| --- | --- | --- | --- | --- |
| Acceso a video privado mediante enlace o caché | Medium | Critical | P0 | Probar autorización en API y archivo; cambiar audiencia y verificar acceso desde otras cuentas y sesiones. |
| Sesión revocada permite controlar una cuenta | Medium | Critical | P0 | Probar revocación y validación de sesión en todos los endpoints protegidos del alcance. |
| Feed no disponible bajo carga | Medium | High | P1 | Ejecutar carga sostenida y picos; comprobar errores, latencia y recuperación. |
| Pérdida o duplicación de una publicación al reintentar | High | High | P1 | Interrumpir conexiones antes y después de guardar; verificar consistencia e idempotencia. |
| Reproducción se bloquea al cambiar de red | High | High | P1 | Simular cambios de conectividad, timeouts y recuperación del reproductor. |
| Controles inaccesibles con lector de pantalla | Medium | High | P1 | Verificar nombres, foco, estados y recorridos con TalkBack y VoiceOver. |
| Cierre inesperado en un sistema soportado | Medium | High | P1 | Ejecutar recorridos esenciales en versiones límite y dispositivos de memoria reducida. |
| Búsqueda no devuelve una cuenta pública conocida | Medium | Medium | P2 | Validar búsqueda con datos controlados, coincidencias y ausencia de resultados. |
| Desalineación decorativa sin afectar controles | Medium | Low | P3 | Revisar capturas y diseño en tamaños representativos. |

## 5.2 Testing Priority Order

1. **P0 — Privacidad**: comprobar la tabla de audiencia, enlaces y cambios de permisos. Exigir cero accesos indebidos en los casos ejecutados.
2. **P0 — Sesiones**: verificar rechazo de sesiones revocadas y operaciones de otra cuenta. Un fallo bloquea la liberación.
3. **P1 — Publicación y recuperación**: probar carga interrumpida, confirmación perdida y reintentos para evitar pérdida o duplicación.
4. **P1 — Feed y reproducción**: ejecutar pruebas funcionales, carga y cambios de red con las metas de la parte 2.
5. **P1 — Accesibilidad y compatibilidad**: completar recorridos esenciales en la matriz soportada con tecnologías de asistencia.
6. **P2 — Búsqueda**: verificar resultados conocidos y mensajes de estado vacío o error.
7. **P3 — Presentación**: revisar detalles visuales que no bloquean el uso.

La regresión de privacidad acompaña cualquier cambio en publicaciones o feed. Si el tiempo se reduce, se aplazan primero las revisiones P3, nunca se omiten las comprobaciones P0 para cumplir una fecha. Las probabilidades se revisan con resultados reales y el orden se ajusta cuando aparezca nueva evidencia.
