from machine import Pin, ADC
from time import sleep_ms

sensor = ADC(Pin(26))
leds = {
    "NORMAL": Pin(13, Pin.OUT),
    "WARNING": Pin(14, Pin.OUT),
    "ALARM": Pin(15, Pin.OUT)
}

UMBRAL_WARNING = 50
UMBRAL_ALARM = 75
MUESTRAS = 10
TIEMPO_MUESTREO = 100

historial = []
estado_actual = None

try:
    print("Iniciando monitor inteligente...")
    while True:
        lectura = sensor.read_u16()
        historial.append(lectura)
        
        if len(historial) > MUESTRAS:
            historial.pop(0)
            
        promedio = max(0, min(65535, sum(historial) / len(historial)))
        
        voltaje = promedio * 3.3 / 65535
        porcentaje = round(promedio * 100 / 65535, 1)
        
        nuevo_estado = "NORMAL"
        if porcentaje >= UMBRAL_ALARM:
            nuevo_estado = "ALARM"
        elif porcentaje >= UMBRAL_WARNING:
            nuevo_estado = "WARNING"
            
        if nuevo_estado != estado_actual:
            for nombre, pin_led in leds.items():
                pin_led.value(nombre == nuevo_estado)
            
            if estado_actual is not None:
                print(f"\n[!] TRANSICION: {estado_actual} -> {nuevo_estado}\n")
            estado_actual = nuevo_estado
            
        print(f"Raw: {lectura} | Volts: {voltaje:.2f} V | Nivel: {porcentaje} % | Estado: {estado_actual}")
        sleep_ms(TIEMPO_MUESTREO)

except KeyboardInterrupt:
    pass
finally:
    for pin_led in leds.values():
        pin_led.value(0)
    print("\nEjecución terminada. Hardware asegurado.")