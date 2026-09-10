#include <stdio.h>
#include <stdlib.h>
#include "pico/stdlib.h"
#include "pico/cyw43_arch.h"

const uint32_t flash_const = 0x12345678;
uint32_t global_counter = 0;

int main() {
    stdio_init_all();
    sleep_ms(3000);

    uint32_t stack_value = 0xABCDEF01; 
    uint8_t *heap_buffer = (uint8_t *)malloc(1024);

    if (heap_buffer == NULL) {
        printf("Error al asignar memoria\n");
        return 1;
    }

    printf("flash const:  %p\n", (void *)&flash_const);
    printf("global:       %p\n", (void *)&global_counter);
    printf("stack value:  %p\n", (void *)&stack_value);
    printf("heap ptr:     %p\n", (void *)heap_buffer); 

    free(heap_buffer);
    while (true) sleep_ms(1000);
}