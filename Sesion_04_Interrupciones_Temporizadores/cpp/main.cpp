#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "hardware/timer.h"
#include "hardware/gpio.h"

// Definición de los mismos pines
#define LED_SIGNAL 15
#define LED_WAIT 14
#define BUTTON 16

// Estados del juego
enum State {
    STATE_WAITING = 0,
    STATE_READY = 1,
    STATE_DONE = 2
};

// Las variables globales que se modifican dentro de interrupciones deben ser "volatile"
volatile State state = STATE_DONE;
volatile uint32_t start_ms = 0;
volatile uint32_t reaction_ms = 0;
volatile bool result_ready = false;
volatile bool false_start = false;
volatile uint32_t last_irq_ms = 0;
int round_number = 0;

alarm_id_t current_alarm = 0;

// Callback del Timer (Equivalente a def show_signal(t))
int64_t show_signal(alarm_id_t id, void *user_data) {
    gpio_put(LED_SIGNAL, 1);
    gpio_put(LED_WAIT, 0);
    start_ms = to_ms_since_boot(get_absolute_time());
    state = STATE_READY;
    return 0; // Devolver 0 indica que la alarma no debe repetirse (ONE_SHOT)
}

// Equivalente a def schedule_round()
void schedule_round() {
    round_number++;
    gpio_put(LED_SIGNAL, 0);
    gpio_put(LED_WAIT, 1);
    result_ready = false;
    false_start = false;
    state = STATE_WAITING;

    uint32_t delay_ms = (rand() % 9001) + 1000; // random entre 1000 y 10000
    
    printf("\n===============================\n");
    printf("Round %d\n", round_number);
    printf("Espera la señal visual. No presiones antes.\n");
    printf("Delay aleatorio: %u ms\n", delay_ms);
    printf("=================================\n");

    // Si había una alarma previa, la cancelamos por seguridad
    if (current_alarm > 0) {
        cancel_alarm(current_alarm);
    }
    // Programamos el nuevo timer (delay_ms)
    current_alarm = add_alarm_in_ms(delay_ms, show_signal, NULL, false);
}

// Callback de la interrupción del botón (Equivalente a def button_irq(pin))
void button_irq(uint gpio, uint32_t events) {
    uint32_t now = to_ms_since_boot(get_absolute_time());

    // Debounce de 80ms
    if (now - last_irq_ms < 80) {
        return;
    }
    last_irq_ms = now;

    if (state == STATE_READY) {
        reaction_ms = now - start_ms;
        gpio_put(LED_SIGNAL, 0);
        result_ready = true;
        state = STATE_DONE;
    } 
    else if (state == STATE_WAITING) {
        // Equivalente a timer.deinit()
        if (current_alarm > 0) {
            cancel_alarm(current_alarm);
            current_alarm = 0;
        }
        false_start = true;
        result_ready = true;
        state = STATE_DONE;
    }
}

int main() {
    // Inicializar puerto serial (USB/UART)
    stdio_init_all();
    
    // Semilla para los números aleatorios
    srand(to_ms_since_boot(get_absolute_time()));

    // Configuración de Pines
    gpio_init(LED_SIGNAL);
    gpio_set_dir(LED_SIGNAL, GPIO_OUT);

    gpio_init(LED_WAIT);
    gpio_set_dir(LED_WAIT, GPIO_OUT);

    gpio_init(BUTTON);
    gpio_set_dir(BUTTON, GPIO_IN);
    gpio_pull_up(BUTTON); // Activar resistencia Pull-Up

    // Configurar interrupción (IRQ) para el botón (Trigger Falling)
    gpio_set_irq_enabled_with_callback(BUTTON, GPIO_IRQ_EDGE_FALL, true, &button_irq);

    // Pequeño delay para que dé tiempo a abrir el monitor serial
    sleep_ms(2000); 
    printf("JUEGO de LOS REFLEJOS\n");

    schedule_round();

    while (true) {
        if (result_ready) {
            if (false_start) {
                printf("SALIDA EN FALSE: presionaste antes de la señal\n");
            } else {
                printf("Tiempo de reaccion: %u ms\n", reaction_ms);
            }

            sleep_ms(1800);

            // Esperar a que suelten el botón (0 es presionado por el Pull-Up)
            while (gpio_get(BUTTON) == 0) {
                sleep_ms(10);
            }
            
            schedule_round();
        }
        
        sleep_ms(20);
    }
    
    return 0;
}