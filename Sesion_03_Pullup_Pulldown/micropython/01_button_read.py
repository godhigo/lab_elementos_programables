from machine import Pin
from time import sleep_ms

# Boton con pull-up interno: libre = 1, presionado = 0
button = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    print(button.value())
    sleep_ms(200)