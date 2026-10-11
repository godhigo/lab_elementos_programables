# Práctica 7: Conversión ADC, Acondicionamiento de Señal y Monitor Inteligente

## Propósito de la Sesión

El objetivo de esta práctica fue implementar un sistema de lectura analógica robusto utilizando el Convertidor Analógico-Digital (ADC) de la Raspberry Pi Pico. Más allá de simplemente leer un valor crudo, el reto consistió en acondicionar la señal mediante un filtro de software (promedio móvil) para eliminar el ruido eléctrico, escalar los datos a valores comprensibles (voltaje y porcentaje), y utilizar esta información para controlar un panel de alertas visuales categorizado por niveles de criticidad.

## Disposición del Hardware

Para el circuito de monitoreo, los componentes se distribuyeron y conectaron de la siguiente manera:

*   **Sensor Analógico (Potenciómetro):** Su señal de lectura se conectó al pin GP26, el cual corresponde al canal ADC0 del microcontrolador.
*   **Indicador de Estado NORMAL:** Un LED conectado al pin GP13.
*   **Indicador de Estado WARNING:** Un LED conectado al pin GP14.
*   **Indicador de Estado ALARM:** Un LED conectado al pin GP15.

*Nota:* Para facilitar el manejo por software, los pines de los LEDs se agruparon lógicamente dentro de un diccionario (colección de datos), vinculando su nombre de estado directamente con su pin físico correspondiente.

## Lógica de Operación y Procesamiento

El sistema no confía en lecturas aisladas, ya que las señales analógicas suelen tener pequeñas variaciones o "ruido". El flujo de procesamiento sigue estos pasos:

1.  **Muestreo y Filtrado (Promedio Móvil):** El microcontrolador toma una lectura cruda (de 0 a 65535) cada 100 milisegundos. Esta lectura se guarda en un historial que almacena únicamente las últimas 10 muestras. El sistema calcula el promedio de esta ventana de datos, suavizando la señal y evitando saltos erráticos.
2.  **Conversión a Escalas Reales:** El valor promediado se transforma matemáticamente a su equivalente en voltaje (de 0.0 a 3.3 V) y a una escala porcentual (0.0% a 100.0%) redondeada a un decimal para mayor precisión lógica.
3.  **Clasificación por Umbrales:** Dependiendo del porcentaje filtrado, el sistema clasifica la situación en tres posibles estados:
    *   **NORMAL:** Porcentaje menor a 50%.
    *   **WARNING:** Porcentaje igual o mayor a 50%, pero menor a 75%.
    *   **ALARM:** Porcentaje igual o mayor a 75%.

## Manejo de Estados y Seguridad del Hardware

El código incorpora prácticas de programación orientadas a la eficiencia y la seguridad física:

*   **Detección de Transiciones:** El sistema tiene "memoria" del estado en el que se encuentra. En lugar de mandar encender o apagar los LEDs constantemente, el programa detecta cuándo ocurre un cambio real (por ejemplo, pasar de NORMAL a WARNING). Solo en ese momento exacto actualiza los pines y emite una alerta visual en la consola, optimizando el procesamiento.
*   **Gestión Segura (Try/Finally):** El ciclo infinito de monitoreo está envuelto en un bloque de control de excepciones. Si el usuario interrumpe la ejecución (mediante `Ctrl+C` / `KeyboardInterrupt`) o si ocurre un error inesperado, el programa garantiza que todos los LEDs se apaguen de forma automática antes de detenerse, evitando que el hardware se quede energizado sin supervisión.

## Reflexión Final

Esta sesión demostró que leer un sensor analógico es solo el primer paso; el verdadero trabajo del microcontrolador es procesar e interpretar esa información. La implementación de un filtro de promedio móvil mejoró drásticamente la estabilidad del sistema, y el uso de estructuras de datos (como diccionarios) junto con rutinas de apagado seguro, dio como resultado un monitor inteligente que combina un código limpio, funcional y protector del hardware físico.