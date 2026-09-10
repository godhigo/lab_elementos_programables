#include <stdio.h>
#include "pico/stdlib.h"

#define BUTTON 16

int main() {
    stdio_init_all();
    sleep_ms(2000); // da tiempo a abrir el monitor serial

    gpio_init(BUTTON);
    gpio_set_dir(BUTTON, GPIO_IN);
    gpio_pull_up(BUTTON);

    while (true) {
        printf("button=%d\n", gpio_get(BUTTON));
        sleep_ms(200);
    }
}