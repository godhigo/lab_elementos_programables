from machine import Pin 
from time import ticks_ms, ticks_diff, sleep_ms

sleep_ms(10)


button = Pin(16, Pin.IN, Pin.PULL_UP)
contador = 0
ultimo = 0

def boton_irq(pin):
    global contador, ultimo
    ahora = ticks_ms()
    if ticks_diff(ahora, ultimo) > 80:
        contador += 1
        ultimo = ahora

button.irq(trigger = Pin.IRQ_FALLING, handler = boton_irq)

while True:
    print("clicks: ", contador)
    sleep_ms(500)