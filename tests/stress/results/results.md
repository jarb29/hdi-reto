# Análisis de Resultados de Prueba de Stress

## 1. Tasa de Peticiones por Segundo (RPS)

- La gráfica "Total Requests per Second" muestra una tasa de solicitudes de alrededor de 0.6 RPS. Esto sugiere que el sistema está gestionando las peticiones de manera continua, aunque no a una tasa muy alta.
- Para un test de stress, esto podría indicar que la velocidad de procesamiento de las solicitudes es lenta, posiblemente debido a la carga de trabajo o a la capacidad del modelo que está ejecutándose en el endpoint.

## 2. Tiempo de Respuesta (Response Times)

- La gráfica de "Response Times" muestra tiempos de respuesta elevados, con una media de alrededor de 12064 ms y una mediana similar, lo que indica que la mayoría de las solicitudes están tardando más de 12 segundos en procesarse.

- El tiempo mínimo registrado es de 12064 ms, mientras que el máximo alcanza los 12369 ms. Esto sugiere una latencia consistente, posiblemente debido a que el modelo y los pipelines de procesamiento son pesados y llevan un tiempo considerable en completarse.
- La alta latencia podría ser un área de mejora, ya que, en aplicaciones de producción, los tiempos de respuesta menores son preferibles para brindar una experiencia de usuario adecuada.

## 3. Concurrent Users (Usuarios Concurrentes)

- En la gráfica "Number of Users", el número de usuarios se mantiene estable en 10. Este fue el pico de usuarios concurrentes configurado en el test, y el sistema fue capaz de manejar esta carga sin errores de respuesta (failures).
- El hecho de que el sistema pueda soportar 10 usuarios sin fallos es positivo, pero la latencia alta indica que podría no escalar bien con un número mucho mayor de usuarios concurrentes.

## Resumen Tabular

- En la tabla de resultados, podemos observar que se realizaron 117 peticiones en total y ninguna falló. Esto es positivo y muestra que el endpoint es robusto en cuanto a manejar solicitudes sin errores.
- El tamaño medio de respuesta es de 32 bytes, lo cual es bajo, sugiriendo que la respuesta probablemente solo contiene el resultado de la predicción y no datos adicionales.
