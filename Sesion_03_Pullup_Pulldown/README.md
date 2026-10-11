# Práctica 3: Control GPIO, Resistencias Internas y Semáforo Interactivo

## Propósito del Proyecto

El objetivo principal fue desarrollar un flujo completo de entrada, procesamiento y salida utilizando la Raspberry Pi Pico 2 W. La tarea consistió en leer la señal de un pulsador aprovechando su resistencia pull-up interna, mitigar el efecto de rebote mecánico (debounce) mediante código, y utilizar esta señal para iniciar la secuencia de un semáforo (vehicular y peatonal) asegurando condiciones de seguridad. Este montaje fue validado tanto en MicroPython y el simulador Wokwi, como en C/C++ utilizando el Pico SDK sobre la placa física.

## Conexiones del Hardware

Para el circuito, evitamos el uso de tablas y organizamos las conexiones de la siguiente manera:

*   **Semáforo Vehicular:** 
    *   Luz Roja: Conectada al pin GP15.
    *   Luz Amarilla: Conectada al pin GP14.
    *   Luz Verde: Conectada al pin GP13.
*   **Semáforo Peatonal:**
    *   Luz Roja: Conectada al pin GP12.
    *   Luz Verde: Conectada al pin GP11.
*   **Pulsador:** Conectado al pin GP16.

*Nota de montaje:* Cada uno de los LEDs está protegido por una resistencia de 330 ohmios conectada a tierra (GND). En el caso del pulsador, una de sus terminales va directa al pin GP16 y la otra a GND; no requiere resistencia física externa gracias a que se habilitó la función de pull-up por software (`gpio_pull_up()` o `Pin.PULL_UP`). Existe un diagrama interactivo disponible en el archivo `wokwi/diagram.json`.

## Lógica de Operación

El comportamiento del sistema se divide en cuatro etapas principales:

1.  **Estado Base (Reposo):** Los vehículos tienen luz verde y los peatones luz roja. Es el estado predeterminado.
2.  **Fase de Advertencia:** La luz vehicular cambia a amarillo por 1.5 segundos, mientras que la peatonal se mantiene en rojo.
3.  **Paso Peatonal:** Los vehículos se detienen frente a la luz roja y los peatones reciben luz verde durante 4 segundos.
4.  **Aviso de Cierre:** El semáforo vehicular sigue en rojo, pero la luz verde de los peatones comienza a parpadear, indicando que el tiempo de cruce está por terminar. Tras esto, el sistema vuelve al Estado Base.

Al oprimir el botón, se ejecuta la función `crossing_sequence()`, la cual maneja la transición automática por todas estas fases. Para mejorar la lectura del código y prevenir errores lógicos, se utilizaron funciones semánticas como `cars_go()` o `pedestrians_go()`, evitando la asignación manual de ceros y unos. 

**Regla de Seguridad Crítica:** Es imperativo que la luz verde de los autos y la de los peatones nunca se enciendan simultáneamente. Esto se logró controlando todos los pines a través de una única función maestra (`set_lights()`), evitando cambios aislados en el estado de los LEDs.

## Manejo de Señales: Pull-up Interno

Se optó por activar el pull-up interno en el pin GP16. Cuando un pin de lectura no tiene nada conectado, su estado queda "flotante" y puede arrojar lecturas erróneas. Al usar la resistencia pull-up, forzamos un valor lógico de 1 por defecto. Al presionar el botón y cerrar el circuito hacia tierra (GND), el valor cae a 0. En resumen: **Botón suelto = 1**, **Botón presionado = 0**.

## Validaciones

Durante el desarrollo se superaron las siguientes etapas:

*   Confirmación de la lectura del botón en MicroPython (`01_button_read.py`), verificando los estados 1 y 0.
*   Implementación de código anti-rebote (debounce) en MicroPython (`02_button_debounce.py`), logrando registrar un único evento válido por pulsación, incluso al dejar el botón presionado.
*   Ejecución exitosa del ciclo completo del semáforo en MicroPython y el entorno Wokwi (`03_semaforo_peatonal.py`).
*   Verificación de la lectura del botón en el entorno de C/C++ (`cpp/button_read/`), obteniendo resultados idénticos a Python.
*   Despliegue final de la secuencia completa en C/C++ utilizando el microcontrolador físico (`cpp/traffic_light/`), confirmando la seguridad del sistema y el correcto comportamiento al mantener presionado el pulsador.

## Aprendizajes Clave

Esta práctica demostró la importancia de no dejar pines de entrada "flotando". Quedó comprobado que, sin habilitar el pull-up interno, las lecturas del pin GP16 serían inestables; configurarlo garantizó un 1 constante que se transforma en 0 de manera predecible al presionar. 

Por otro lado, la necesidad del "debounce" quedó muy clara: sin una pequeña pausa de 30 ms para validar el estado del mecanismo, una sola pulsación física se registraba como múltiples toques, descontrolando la ejecución del programa. Finalmente, desarrollar el mismo proyecto en MicroPython y luego en C++ resultó de gran utilidad para contrastar y separar la lógica general del hardware de la sintaxis específica de cada lenguaje.