from machine import Pin, Timer
from time import ticks_ms, ticks_diff, sleep_ms

naranja = Pin(15, Pin.OUT)
rosa = Pin(14, Pin.OUT)

timer = Timer(-1)

timer_disparado = False

def timer_callback(t):
    global timer_disparado
    timer_disparado = True

naranja.off()
rosa.on()
print("PRUEBA TIMER")
print("Naranja = OFF")
print("Rosa = ON")
print("Esperando 3 segundos ")

timer.init(
    mode = Timer.ONE_SHOT,
    period = 3000,
    callback = timer_callback
)

contador = 0

while True:
    print("MAIN Trabajando: ", contador)
    contador += 1
    
    if timer_disparado:
        timer_disparado = False
        naranja.on()
        rosa.off()

        print("TIMER DISPARADO")
        print("Naranja = ON")
        print("Rosa = OFF")

        print("GP15", naranja.value())
        print("GP14", rosa.value())
        print()
    
    sleep_ms(500)