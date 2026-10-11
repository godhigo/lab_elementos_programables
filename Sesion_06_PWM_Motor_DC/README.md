# Práctica 6: Control Avanzado de Motor DC con PWM y Puente H L298N

## Propósito de la Sesión

El objetivo de esta práctica fue lograr el control total sobre un motor de corriente continua (DC), manejando tanto su sentido de giro como su velocidad. Para ello, se utilizó la técnica de Modulación por Ancho de Pulsos (PWM) generada por el microcontrolador, en conjunto con un módulo de potencia Puente H (L298N). Además, se implementaron por software características de seguridad y confort, como rampas de aceleración suave, compensación de la "zona muerta" del motor y bloqueos de seguridad al cambiar la dirección de giro.

## Disposición del Hardware

Las conexiones principales entre el microcontrolador (Raspberry Pi Pico) y los actuadores se organizaron de la siguiente manera, evitando el uso de tablas:

*   **Señales de Control (Puente H L298N):**
    *   Dirección 1 (IN1): Conectada al pin GP2.
    *   Dirección 2 (IN2): Conectada al pin GP3.
    *   Velocidad (ENA): Conectada al pin GP4. Este pin recibe la señal PWM configurada a 150 Hz.
*   **Motor DC:** Conectado a las terminales de salida del L298N.
*   **Componentes Adicionales (Diagrama):** El esquema interactivo incluye un potenciómetro en el pin GP26 y tres botones tácticos (GP14, GP15, GP16) destinados a funciones manuales de "Adelante", "Reversa" y "Paro", aunque el código principal fue diseñado para ejecutar rutinas de automatización y estrés de forma autónoma.

## Lógica de Operación y Control

El código base se estructuró para superar los problemas físicos comunes al trabajar con motores, implementando las siguientes soluciones:

1.  **Vencer la Inercia y la Zona Muerta:** Los motores reales no giran si reciben muy poca energía. Para solucionar esto, se estableció un ciclo de trabajo mínimo (35%). Además, cuando el motor arranca desde cero, el código aplica un "empujón" inicial (Kick) mandando el 100% de la energía durante 150 milisegundos para romper la inercia estática antes de estabilizarse en la velocidad deseada.
2.  **Transiciones Suaves (Rampas):** Para evitar tirones bruscos mecánicos y picos de corriente, se desarrolló la función `ramp_to`. Esta rutina incrementa o disminuye la velocidad en pasos de 10% con pausas de 80 ms, logrando aceleraciones y desaceleraciones progresivas.
3.  **Seguridad al Invertir el Giro:** Cambiar repentinamente de "Adelante" a "Reversa" mientras el motor gira a máxima velocidad puede dañar el puente H o la mecánica. El software incluye un enclavamiento de seguridad que obliga al sistema a bajar la velocidad a 0% usando una rampa, detenerse por completo durante 800 ms, y solo entonces invertir la polaridad de los pines IN1 e IN2.

## Fases de Demostración

El programa ejecuta un ciclo infinito compuesto por dos retos principales para validar la robustez del sistema:

*   **Prueba de Niveles (DO 04):** El motor acelera suavemente hacia adelante, estacionándose temporalmente en distintos umbrales de velocidad (30%, 60%, 90% y 100%). Cada nivel se mantiene durante 1.5 segundos antes de pasar al siguiente. Al finalizar, desacelera suavemente hasta detenerse.
*   **Secuencia de Desafío (RETO 06):** Inicia acelerando de 0 a 100% hacia adelante, mantiene esa velocidad punta, y luego realiza una inversión segura para acelerar en reversa hasta el 80%. Finalmente, desacelera a 0% para reiniciar el ciclo completo tras una pausa de descanso.

## Reflexión Final

Esta práctica ilustra claramente la diferencia entre simplemente mandar voltaje a un actuador y controlarlo de forma inteligente. El uso del puente H resolvió la inversión de giro y el manejo de potencia, pero fue la programación de rampas, el "kick" de arranque y los tiempos muertos de seguridad lo que transformó un comportamiento errático en un sistema suave, predecible y profesional.