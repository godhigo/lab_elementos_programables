# Práctica 4: Eventos Asíncronos, Timers e Interrupciones

## Propósito de la Sesión

La meta de esta práctica fue dejar atrás la programación secuencial clásica y dominar el diseño basado en eventos en microcontroladores. El reto consistió en eliminar las pausas que paralizan el procesador (como el comando `sleep`) mediante el uso de interrupciones físicas y temporizadores. Todo el aprendizaje se puso en práctica programando un "Juego de los Reflejos".

## Disposición del Hardware

El proyecto se simuló primero en Wokwi (usando una Raspberry Pi Pico normal) y luego se llevó al hardware real utilizando la Raspberry Pi Pico 2 W. Las conexiones se organizaron de esta manera:

*   **Indicadores Visuales:** Se utilizaron dos LEDs para las fases del juego. Un LED naranja asignado al pin GP15 y un LED rosa en el pin GP14. Ambos cuentan con su respectiva resistencia para limitar la corriente y funcionan para indicar los tiempos de espera y el momento de reaccionar.
*   **Gatillo de Acción:** Un pulsador conectado directamente al pin GP16. Para evitar el uso de más componentes físicos, se configuró su resistencia pull-up interna a través del código.

## Fundamentos Teóricos

Para lograr la asincronía, nos basamos en dos herramientas cruciales del microcontrolador:

*   **Interrupciones (IRQ):** Funcionan como una señal de emergencia del hardware. Cuando ocurre un evento físico (como presionar el botón), el procesador pausa de inmediato su tarea actual (el ciclo `while True`), atiende una función de respuesta rápida (callback), y luego retoma exactamente donde se quedó. Esto brinda una capacidad de reacción instantánea.
*   **Temporizadores (Timers):** Son módulos del chip que cuentan el paso del tiempo por su cuenta, sin distraer al cerebro principal. Con ellos, podemos programar alarmas para que una función se dispare tras cierta cantidad de tiempo (ya sea una sola vez o de forma cíclica) sin bloquear el flujo del programa.

## Obstáculos y Resoluciones

Durante el desarrollo nos topamos con dos retos principales:

*   **Rebotes Mecánicos (Bouncing):** Al presionar el botón real, las pequeñas vibraciones metálicas hacían que el microcontrolador leyera varias pulsaciones en lugar de una. Para arreglarlo, programamos un filtro de software (debounce) que ignora cualquier interrupción que suceda a menos de 80 milisegundos de la primera.
*   **Manejo de Variables:** Tuvimos problemas para actualizar los datos del juego desde adentro de las funciones que atienden las interrupciones (callbacks). Esto se corrigió declarando de manera explícita la palabra reservada `global` en Python antes de modificar dichas variables.

## Reflexión Final

Implementar timers e interrupciones cambia por completo la forma de programar sistemas embebidos. Pasar de un código que "duerme" inútilmente a una arquitectura responsiva orientada a eventos, permite que el chip realice tareas de fondo mientras está atento a su entorno. El resultado es un sistema mucho más eficiente, rápido y profesional que aprovecha al máximo sus recursos de hardware.