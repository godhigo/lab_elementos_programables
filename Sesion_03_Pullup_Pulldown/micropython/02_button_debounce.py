from machine import Pin
from time import sleep_ms

button = Pin(16, Pin.IN, Pin.PULL_UP)
last = 1

while True:
    now = button.value()
    if last == 1 and now == 0:
        sleep_ms(30)  # debounce
        if button.value() == 0:
            print('CLICK valido')
            while button.value() == 0:  # wait for release
                sleep_ms(10)
    last = now
    sleep_ms(10)