# Analisis

## Matris

| **Riesgo**                                           | **Probabilidad** | **Impacto** | **Prioridad** | **Como solucionarlo**                                                                                                                                                                                                      |
|------------------------------------------------------|------------------|------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Fuga de datos de usuarios                            | Bajo             | Critico    | P0            | Hacer pruebas constantes de seguridad y revisar riesgos.                                                                                                                                                                   |
| Lag en el video por picos de usuarios                | Alto             | Alto       | P1            | Escalar automáticamente los servidores para sobrepasar los picos.                                                                                                                                                          |
| Fallo en el estado de dispositivos conectados        | Medio            | Medio      | P2            | Hacer que los dispositivos envíen su estado constantemente mientras estén conectados, para evitar conexiones fantasma y que otros usuarios no puedan conectarse (me ha pasado).                                            |
| Carga de datos incorrecta en regiones específicas    | Bajo           | High       | P1            | Tener una forma de sortear la VPN (que encripta la IP) para evitar que se libere contenido no disponible en cierta zona, y evitar problemas con los derechos de autor o que pase por accidente por una mala configuración. |
| Problemas de acceso a las bases de datos de usuario  | Bajo             | Critica    | P1            | Respaldar la información en otros servidores para que, si uno falla, no afecte tanto (como la caída de AWS).                                                                                                               |
| Inconsistencia de UI                                 | Medium           | Medio      | P2            | Hacer pruebas en la mayoría de sistemas y navegadores, y probar en diferentes periféricos.                                                                                                                                 |

## Top
1. Fuga de datos de usuarios  
2. Problemas de acceso a las bases de datos de usuario
3. Carga de datos incorrecta en regiones específicas
4. Lag en el video por picos de usuarios
5. Fallo en el estado de dispositivos conectados
6. Inconsistencia de UI    