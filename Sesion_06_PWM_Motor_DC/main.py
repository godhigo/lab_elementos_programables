from machine import Pin, PWM
from time import sleep_ms

PWM_FREQ = 150     
MIN_DUTY = 35       
KICK_MS = 150       

IN1 = Pin(2, Pin.OUT)  
IN2 = Pin(3, Pin.OUT) 
ENA = PWM(Pin(4))
ENA.freq(PWM_FREQ)      

IN1.value(0)
IN2.value(0)
ENA.duty_u16(0)

PASO_RAMPA = 10
DELAY_RAMPA_MS = 80
MANTENER_MS = 1500
PAUSA_INVERSION_MS = 800
PAUSA_CICLO_MS = 2500
NIVELES = [30, 60, 90, 100]

DETENIDO = 0
ADELANTE = 1
REVERSA = 2

velocidad_actual = 0
direccion_actual = DETENIDO

def duty_real(percent):
    if percent == 0:
        return 0
    real = MIN_DUTY + (100 - MIN_DUTY) * percent / 100
    return int(real * 65535 / 100)

def set_speed(percent):
    global velocidad_actual
    percent = int(max(0, min(100, percent)))

    if velocidad_actual == 0 and percent > 0:
        ENA.duty_u16(65535)
        sleep_ms(KICK_MS)

    ENA.duty_u16(duty_real(percent))
    velocidad_actual = percent

def forward():
    global direccion_actual
    IN1.value(1)
    IN2.value(0)
    direccion_actual = ADELANTE

def reverse():
    global direccion_actual
    IN1.value(0)
    IN2.value(1)
    direccion_actual = REVERSA

def stop():
    global direccion_actual
    set_speed(0)
    IN1.value(0)
    IN2.value(0)
    direccion_actual = DETENIDO

def ramp_to(start, end, step=10, delay_ms=100):
    if start == end:
        set_speed(end)
        return

    if start < end:
        paso = step
        etiqueta = "Acelerando"
    else:
        paso = -step
        etiqueta = "Desacelerando"

    for speed in range(start, end, paso):
        set_speed(speed)
        print(f"{etiqueta}: {speed} %")
        sleep_ms(delay_ms)

    set_speed(end)
    print(f"{etiqueta}: {end} %")

def cambiar_direccion(nueva):
    if nueva == direccion_actual:
        return

    if velocidad_actual > 0:
        print("[SEGURIDAD] Bajando a 0 % antes de cambiar de direccion")
        ramp_to(velocidad_actual, 0, PASO_RAMPA, DELAY_RAMPA_MS)

    stop()
    sleep_ms(PAUSA_INVERSION_MS)

    if nueva == ADELANTE:
        print("[DIRECCION] FORWARD")
        forward()
    elif nueva == REVERSA:
        print("[DIRECCION] REVERSE")
        reverse()

def mantener(ms):
    print(f"[MANTENER] {velocidad_actual} % durante {ms} ms")
    sleep_ms(ms)

def prueba_niveles():
    print("\n########## PRUEBA DE VELOCIDADES (DO 04) ##########")
    cambiar_direccion(ADELANTE)
    for nivel in NIVELES:
        ramp_to(velocidad_actual, nivel, PASO_RAMPA, DELAY_RAMPA_MS)
        print(f"[NIVEL] {nivel} %")
        mantener(MANTENER_MS)
    ramp_to(velocidad_actual, 0, PASO_RAMPA, DELAY_RAMPA_MS)
    print("[STOP] Motor detenido")
    stop()
    sleep_ms(PAUSA_INVERSION_MS)

def secuencia_challenge():
    print("\n RETO 06")
    cambiar_direccion(ADELANTE)                                 
    ramp_to(0, 100, PASO_RAMPA, DELAY_RAMPA_MS)                 
    mantener(MANTENER_MS)                                       
    cambiar_direccion(REVERSA)                                  
    ramp_to(0, 80, PASO_RAMPA, DELAY_RAMPA_MS)                  
    mantener(MANTENER_MS)                                       
    ramp_to(80, 0, PASO_RAMPA, DELAY_RAMPA_MS)                  
    print("[STOP] Motor detenido")
    stop()                                                      

print("RETO 06 - SMART MOTOR CONTROLLER")
print(f"Pines: GP2 = IN1, GP3 = IN2, GP4 = ENA/PWM @ ({PWM_FREQ} Hz)")
print(f"Zona muerta compensada: 1 % logico = {MIN_DUTY} % real")
stop()
sleep_ms(1500)

numero_ciclo = 0

while True:
    numero_ciclo += 1
    print(60 * "=")
    print(f"    CICLO {numero_ciclo}")
    prueba_niveles()
    secuencia_challenge()
    sleep_ms(PAUSA_CICLO_MS)