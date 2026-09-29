## 5.1 Risk Matrix

| Risk | Likelihood | Impact | Priority | Mitigation Strategy |
|---|---|---|---|---|
| Falla en el autoguardado de un examen a mitad del intento | Medium | Critical | P0 | Pruebas de reliability simulando pérdida de conexión; autoguardado cada pocos segundos |
| Acceso indebido a calificaciones de otro alumno (falla de roles) | Low | Critical | P0 | Pruebas de seguridad exhaustivas en control de acceso por ID/rol |
| Caída del sistema durante entregas masivas (fecha límite) | Medium | Critical | P0 | Pruebas de carga/performance simulando picos de tráfico reales |
| Cálculo incorrecto del promedio de calificaciones | Low | High | P1 | Pruebas unitarias exhaustivas de la función de cálculo, incluyendo casos límite |
| Entrega de archivo corrupta por conexión cortada a mitad de la subida | Medium | High | P1 | Pruebas de reliability en el flujo de subida de archivos |
| Interfaz confusa que lleva a errores de entrega o mala lectura de calificaciones | Medium | Medium | P2 | Pruebas de usabilidad con usuarios reales (profesores y alumnos piloto) |
| Incompatibilidad con navegadores o dispositivos menos comunes | Low | Medium | P2 | Pruebas de compatibilidad cross-browser y cross-dispositivo |

## 5.2 Testing Priority Order

1. Seguridad (control de acceso por roles y permisos).
2. Reliability (autoguardado de exámenes, subida de archivos, recuperación tras caídas).
3. Performance (comportamiento del sistema durante entregas masivas y cierre de semestre).
4. Funcional / Boundary (cálculo de calificaciones, validación de archivos).
5. Usabilidad (claridad de la interfaz para alumnos y profesores).
6. Compatibilidad (navegadores y dispositivos).
7. Regresión (validación continua en cada actualización del sistema).
