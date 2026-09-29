# Part 5: Risk Analysis & Test Prioritization

## 5.1 Risk Matrix

Diez riesgos identificados para Spotify, clasificados por probabilidad e impacto. La prioridad se deriva de la combinación de ambos: un riesgo de impacto crítico recibe P0 aunque su probabilidad sea baja, porque su consecuencia es inaceptable.

| **Risk** | **Likelihood** | **Impact** | **Priority** | **Mitigation Strategy** |
| --- | --- | --- | --- | --- |
| Falla en el cobro de suscripciones (cargo duplicado, cobro tras cancelar, premium no activado tras pagar) | Low | Critical | P0 | Pruebas de integración exhaustivas contra el entorno sandbox de la pasarela; pruebas unitarias con 95% de cobertura de ramas en el motor de prorrateo; conciliación automática diaria entre cobros y estados de cuenta; alerta ante cualquier discrepancia |
| Conteo incorrecto de reproducciones que distorsiona el pago de regalías | Medium | Critical | P0 | Pruebas unitarias de los valores límite del stream válido (29/30/31 s); pruebas de idempotencia del consumidor de Kafka ante reentrega de eventos; conciliación mensual del pipeline contra el reporte entregado a los sellos |
| Reproducción de contenido fuera de su territorio licenciado (fallo de geobloqueo) | Low | Critical | P0 | Pruebas de sistema por territorio con cuentas de cada mercado; validación de la licencia en el servidor y no solo en el cliente; pruebas de acceso por enlace directo y con VPN; revisión de cumplimiento con el equipo legal antes de cada liberación |
| Fuga de datos personales o de credenciales por vulnerabilidad en la API | Low | Critical | P0 | Pruebas de penetración trimestrales; escaneo automático de dependencias (SCA) en cada build; pruebas de inyección y de control de acceso en cada endpoint; revisión de seguridad obligatoria para cambios en autenticación |
| Caída o degradación severa del servicio durante un pico de tráfico (lanzamiento de álbum, Wrapped) | Medium | High | P1 | Pruebas de carga y estrés previas a cada evento previsto; pruebas de resistencia de 12 h; autoescalado verificado bajo carga; ingeniería del caos para validar la degradación controlada de servicios no críticos |
| Interrupciones y cortes de audio en redes móviles inestables | High | High | P1 | Pruebas de resiliencia con simulación de red degradada e intermitente; verificación del cambio adaptativo de bitrate; pruebas de transición Wi-Fi/datos móviles; monitoreo en producción de la tasa de errores de reproducción por región |
| Extracción no autorizada del catálogo desde el contenido descargado offline | Low | Critical | P0 | Verificación del cifrado en reposo del contenido offline; pruebas de DRM en dispositivos con acceso root; revalidación periódica de la licencia; auditoría externa de la implementación de Widevine |
| Regresión introducida por un despliegue que rompe funcionalidad existente | High | High | P1 | Suite de regresión automatizada ejecutada en cada merge; despliegue gradual con feature flags y monitoreo de métricas de salud; procedimiento de reversión probado; puertas de calidad que bloquean el merge ante fallas |
| Fallos de compatibilidad en dispositivos Android de gama baja (cierres por memoria) | High | Medium | P2 | Pruebas en granja de dispositivos reales priorizando los diez pares dispositivo/SO más comunes; perfilado de memoria en sesiones largas; presupuesto de tamaño de app y de consumo de memoria verificado en CI |
| Recomendaciones irrelevantes o repetitivas que reducen el uso y aumentan la cancelación | Medium | Medium | P2 | Pruebas basadas en propiedades del generador de playlists (longitud, diversidad, no repetición); pruebas A/B en producción; monitoreo de la tasa de guardado de canciones recomendadas y de la tasa de cancelación |
| Barreras de accesibilidad que impiden el uso con lector de pantalla | Medium | Medium | P2 | Auditoría automatizada con axe-core en CI; pruebas manuales con VoiceOver y TalkBack en cada liberación mayor; validación con usuarios con discapacidad visual en la fase beta |
| Errores de localización: precio, impuesto o formato incorrecto por mercado | Medium | Medium | P2 | Pruebas de sistema por mercado con validación del precio mostrado contra el monto cobrado; pruebas de diseño RTL; revisión de traducciones con hablantes nativos antes de la liberación |

**Leyenda**
**Likelihood**: Low / Medium / High
**Impact**: Low / Medium / High / Critical
**Priority**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

### Distribución de los riesgos

| **Prioridad** | **Cantidad** | **Criterio de asignación** |
| --- | --- | --- |
| P0 | 5 | Impacto crítico: consecuencia legal, financiera o contractual irreversible |
| P1 | 3 | Alta probabilidad y alto impacto sobre la experiencia central del producto |
| P2 | 4 | Impacto medio, degradan el producto sin impedir su uso |
| P3 | 0 | No se identificaron riesgos de esta categoría en el alcance analizado |

---

## 5.2 Testing Priority Order

Orden de las actividades de prueba derivado directamente de la matriz anterior. El criterio es simple: primero lo que puede causar daño irreversible, después lo que degrada la experiencia central, y al final lo que afecta funciones secundarias.

1. **Pruebas del flujo de facturación y suscripciones** (P0) — pruebas unitarias de prorrateo, impuestos y descuentos, más pruebas de integración contra la pasarela de pago cubriendo cobro exitoso, rechazo, tiempo de espera agotado y webhook diferido. Es el punto donde un defecto se traduce directamente en dinero mal cobrado.

2. **Pruebas del pipeline de conteo de reproducciones y regalías** (P0) — valores límite del stream válido, idempotencia ante reentrega de eventos y conciliación del reporte. Es el defecto más caro y menos visible del sistema.

3. **Pruebas de licenciamiento y geobloqueo por territorio** (P0) — validación en servidor, acceso por enlace directo y comportamiento con VPN, ejecutadas por cada mercado relevante.

4. **Pruebas de seguridad sobre autenticación, API y contenido offline** (P0) — inyección, control de acceso, revocación de sesión, cifrado en reposo del contenido descargado y escaneo de dependencias.

5. **Pruebas de regresión automatizadas de los flujos críticos** (P1) — ejecutadas en cada merge sobre las cinco plataformas. Es la actividad de mayor frecuencia y mejor retorno sobre la automatización.

6. **Pruebas funcionales de reproducción de audio** (P1) — cola, aleatorio, repetición, gapless, crossfade y Spotify Connect. El corazón del producto.

7. **Pruebas de resiliencia ante redes inestables y modo offline** (P1) — pérdida de conexión, transición entre redes, degradación de bitrate y respaldo con contenido descargado.

8. **Pruebas de rendimiento, carga y estrés** (P1) — previas a cada evento de tráfico previsto y como corrida de resistencia periódica.

9. **Pruebas de compatibilidad en la matriz de dispositivos** (P2) — priorizando los pares dispositivo/sistema operativo que cubren el 80% de la base instalada, con atención especial a Android de gama baja.

10. **Pruebas de accesibilidad** (P2) — auditoría automatizada en CI y validación manual con lectores de pantalla en cada liberación mayor.

11. **Pruebas de localización e internacionalización** (P2) — precio, impuesto, formatos y diseño RTL por mercado.

12. **Pruebas de usabilidad y de calidad de las recomendaciones** (P2) — sesiones con usuarios reales y validación estadística del generador de playlists, complementadas con experimentación A/B en producción.

### Justificación del orden

Las primeras cuatro actividades corresponden a los riesgos P0 y comparten una característica: su consecuencia no es reversible con un parche. Un cobro incorrecto ya ocurrió, una regalía mal contada ya se pagó, una pista reproducida fuera de territorio ya incumplió el contrato, y unos datos filtrados ya salieron. Las actividades 5 a 8 protegen la experiencia central —que la música suene, siempre, sin cortes— que es el valor por el que el usuario paga. Las últimas cuatro atienden riesgos que degradan el producto y erosionan la retención con el tiempo, pero que no impiden usarlo ni exponen a la empresa de forma inmediata.

Este orden también refleja el principio de agrupamiento de defectos de la Parte 4: los módulos de pago, sincronización offline y Spotify Connect concentran históricamente la mayor densidad de defectos, y aparecen en los primeros siete lugares de esta lista.
