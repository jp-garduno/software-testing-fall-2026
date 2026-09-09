# Análisis de riesgos y priorización de pruebas: Instagram

## 5.1 Matriz de riesgos

| Riesgo                                                                                                               | Probabilidad | Impacto | Prioridad | Estrategia de mitigación                                                                                                                                              |
| -------------------------------------------------------------------------------------------------------------------- | ------------ | ------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Toma de control de una cuenta debido a una vulnerabilidad en la autenticación                                        | Baja         | Crítico | P0        | Realizar pruebas de seguridad en el inicio de sesión y 2FA, pruebas de penetración y limitar los intentos de inicio de sesión.                                        |
| Los mensajes directos llegan al usuario equivocado o se pierden                                                      | Baja         | Crítico | P0        | Realizar pruebas de integración y de sistema en el sistema de mensajería, incluyendo escenarios de concurrencia y condiciones de carrera.                             |
| El contenido de una cuenta privada queda expuesto a usuarios que no son seguidores                                   | Baja         | Crítico | P0        | Probar las reglas de privacidad y visibilidad, además de ejecutar pruebas de regresión sobre el control de acceso después de cada lanzamiento.                        |
| La aplicación se bloquea o presenta una fuerte disminución de rendimiento durante eventos virales o picos de tráfico | Media        | Alto    | P1        | Realizar pruebas de carga y rendimiento simulando aumentos repentinos de usuarios y validar el funcionamiento del escalamiento automático.                            |
| Fallo en el pago o cobro incorrecto durante una compra en Instagram Shop                                             | Baja         | Crítico | P0        | Realizar pruebas de integración de extremo a extremo con la pasarela de pagos y utilizar transacciones de prueba antes de cada lanzamiento.                           |
| El algoritmo de recomendaciones muestra contenido dañino o que incumple las políticas                                | Media        | Alto    | P1        | Combinar pruebas del sistema de recomendaciones con pruebas de moderación de contenido y revisiones realizadas por personas.                                          |
| La carga de fotos o videos falla o se corrompe en ciertos dispositivos o redes                                       | Media        | Medio   | P2        | Realizar pruebas de compatibilidad con diferentes dispositivos, sistemas operativos y redes, además de probar los mecanismos de reintento y manejo de errores.        |
| El texto de la interfaz se corta o el diseño se rompe en idiomas distintos al inglés                                 | Media        | Bajo    | P3        | Realizar pruebas de localización en los idiomas disponibles, prestando especial atención a palabras largas y a idiomas que utilizan escritura de derecha a izquierda. |

## 5.2 Orden de prioridad de las pruebas

1. **Pruebas de seguridad:** enfocarse primero en la autenticación, el acceso a las cuentas y la visibilidad del contenido privado. Estas pruebas ayudan a prevenir el robo de cuentas y la exposición de información, que podrían generar consecuencias legales y afectar gravemente la reputación de la plataforma.

2. **Pruebas de integración y sistema del proceso de pagos:** verificar principalmente el flujo de compra y pago de Instagram Shop. Los errores en esta área pueden provocar pérdidas económicas y afectar directamente la confianza de los usuarios.

3. **Pruebas de integración del sistema de mensajes directos:** es una función principal de Instagram, por lo que cualquier error en el envío o recepción de mensajes puede afectar inmediatamente la confianza de los usuarios.

4. **Pruebas de rendimiento y carga:** comprobar que la aplicación pueda mantenerse disponible durante momentos de tráfico elevado, como cuando una publicación o evento se vuelve viral.

5. **Pruebas del algoritmo de recomendaciones y moderación de contenido:** verificar que el contenido mostrado sea relevante y seguro, evitando que aparezcan publicaciones dañinas o que incumplan las políticas de la plataforma.

6. **Pruebas de compatibilidad:** evaluar la carga y reproducción de contenido en diferentes dispositivos, versiones de sistemas operativos y tipos de conexión. Aunque estos errores pueden afectar a muchos usuarios, normalmente tienen un impacto menor que los problemas de seguridad o pagos.

7. **Pruebas de regresión:** ejecutar pruebas sobre las funciones principales antes de cada lanzamiento para asegurarse de que los nuevos cambios o correcciones no vuelvan a introducir errores importantes.

8. **Pruebas de localización y accesibilidad:** comprobar que Instagram pueda utilizarse correctamente por personas de diferentes idiomas y necesidades. Son importantes para la inclusión y el alcance internacional, aunque representan un riesgo empresarial inmediato menor que los puntos anteriores.
