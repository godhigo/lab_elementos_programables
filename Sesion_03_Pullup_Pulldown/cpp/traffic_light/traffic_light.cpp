#include <stdio.h>
#include "pico/stdlib.h"

#define CAR_RED    15
#define CAR_YELLOW 14
#define CAR_GREEN  13
#define PED_RED    12
#define PED_GREEN  11
#define BUTTON     16

void set_lights(bool car_r, bool car_y, bool car_g, bool ped_r, bool ped_g) {
    gpio_put(CAR_RED,    car_r);
    gpio_put(CAR_YELLOW, car_y);
    gpio_put(CAR_GREEN,  car_g);
    gpio_put(PED_RED,    ped_r);
    gpio_put(PED_GREEN,  ped_g);
}

void cars_go()               { set_lights(0, 0, 1,   1, 0); }
void cars_prepare_to_stop()  { set_lights(0, 1, 0,   1, 0); }
void pedestrians_go()        { set_lights(1, 0, 0,   0, 1); }

void crossing_sequence() {
    printf("S1 TRANSICION: autos amarillo, peaton rojo\n");
    cars_prepare_to_stop();
    sleep_ms(1500);

    printf("S2 CRUCE: autos rojo, peaton verde\n");
    pedestrians_go();
    sleep_ms(4000);

    printf("S3 FIN: peaton verde parpadea\n");
    for (int i = 0; i < 4; i++) {
        gpio_put(PED_GREEN, !gpio_get(PED_GREEN));
        sleep_ms(300);
    }

    printf("S0 REPOSO: autos verde, peaton rojo\n");
    cars_go();
}

int main() {
    stdio_init_all();
    sleep_ms(2000);

    gpio_init(CAR_RED);    gpio_set_dir(CAR_RED, GPIO_OUT);
    gpio_init(CAR_YELLOW); gpio_set_dir(CAR_YELLOW, GPIO_OUT);
    gpio_init(CAR_GREEN);  gpio_set_dir(CAR_GREEN, GPIO_OUT);
    gpio_init(PED_RED);    gpio_set_dir(PED_RED, GPIO_OUT);
    gpio_init(PED_GREEN);  gpio_set_dir(PED_GREEN, GPIO_OUT);

    gpio_init(BUTTON);
    gpio_set_dir(BUTTON, GPIO_IN);
    gpio_pull_up(BUTTON);

    cars_go();
    printf("Sistema listo. S0 REPOSO: autos verde / peaton rojo\n");

    while (true) {
        if (gpio_get(BUTTON) == 0) {
            sleep_ms(30); // debounce
            if (gpio_get(BUTTON) == 0) {
                printf("CLICK valido: peaton solicito cruce\n");
                crossing_sequence();

                while (gpio_get(BUTTON) == 0) { // wait for release
                    sleep_ms(10);
                }
            }
        }
        sleep_ms(10);
    }
}