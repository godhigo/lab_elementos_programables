# =========================================================================
#  DO 04 / CHALLENGE 06 - Smart Motor Controller
#  Sesion 06: PWM + Puente H (L298N) + Motor DC
#  Angel Rugerio Jimenez
#  Axel Garcia Arellano
#
#  IN1/IN2 deciden hacia donde gira el motor; ENA (PWM) decide que tan
#  rapido. Toda la velocidad cambia por rampas y el sentido solo se
#  invierte con el motor en 0 %.
#  Probado en Wokwi y en hardware fisico (Pico 2 W + L298N + motor DC).
# =========================================================================

from machine import Pin, PWM
from time import sleep_ms

# ---------------- Ajustes del motor fisico ----------------
PWM_FREQ = 100          # Hz. Frecuencia baja = mas torque en motores chicos
MIN_DUTY = 40           # % real minimo con el que el motor SI gira (zona muerta)
KICK_MS = 120           # empujon al 100 % cuando arranca desde 0

# Pines del puente H (iguales en Wokwi y en el montaje fisico)
# Se crean ya en 0 para que el motor no se mueva al encender la Pico
IN1 = Pin(2, Pin.OUT, value=0)                   # GP2 - direccion
IN2 = Pin(3, Pin.OUT, value=0)                   # GP3 - direccion
ENA = PWM(Pin(4), freq=PWM_FREQ, duty_u16=0)     # GP4 - velocidad por PWM

# Parametros de la demostracion
PASO_RAMPA = 5          # % que cambia la velocidad en cada paso
DELAY_RAMPA_MS = 100    # tiempo entre pasos -> 0 a 100 % en 2 s
MANTENER_MS = 2000      # tiempo sostenido a velocidad constante
PAUSA_INVERSION_MS = 500  # motor detenido antes de cambiar el sentido
PAUSA_CICLO_MS = 3000   # descanso entre una demostracion completa y la siguiente
NIVELES = [25, 50, 75, 100]

# Constantes numericas para la direccion
DETENIDO = 0
ADELANTE = 1
REVERSA = 2

# Variables globales de control
velocidad_actual = 0
direccion_actual = DETENIDO


# ---------------- Funciones base ----------------
def _duty_real(percent):
    """Traduce 0-100 % 'logico' a duty real saltando la zona muerta.
    0 % = apagado. 1-100 % se reparte entre MIN_DUTY y 100 %,
    asi 25 % ya mueve el motor en lugar de solo zumbar."""
    if percent == 0:
        return 0
    real = MIN_DUTY + (100 - MIN_DUTY) * percent / 100
    return int(real * 65535 / 100)


def set_speed(percent):
    global velocidad_actual
    percent = int(max(0, min(100, percent)))   # saturacion: 0 <= percent <= 100

    # Si venimos de 0 y vamos a movernos, empujon para vencer la inercia
    if velocidad_actual == 0 and percent > 0:
        ENA.duty_u16(65535)
        sleep_ms(KICK_MS)

    ENA.duty_u16(_duty_real(percent))
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


# ---------------- TODO 1: rampa ----------------
# Sube o baja de start a end de step en step. range() excluye su limite,
# asi que al final se fija end a mano: la rampa siempre termina exacta,
# aunque la distancia no sea multiplo del paso (ej. 0 -> 75 con paso 10).
def ramp_to(start, end, step=10, delay_ms=100):
    if start == end:
        set_speed(end)
        return

    if start < end:
        paso = abs(step)
        etiqueta = "Acelerando"
    else:
        paso = -abs(step)       # si start > end el paso debe ser negativo
        etiqueta = "Desacelerando"

    for speed in range(start, end, paso):
        set_speed(speed)
        print(f"{etiqueta}: {speed} %")
        sleep_ms(delay_ms)

    set_speed(end)
    print(f"{etiqueta}: {end} %")


# ---------------- Cambio seguro de direccion ----------------
# Nunca se invierte en movimiento: primero rampa a 0 %, pausa con el
# motor detenido y solo entonces se cambia IN1/IN2.
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


# ---------------- Etapas de la demostracion ----------------
# Requisito 4: velocidades 25/50/75/100 %. Entre niveles tambien se usa
# rampa, para que ningun cambio de velocidad sea un escalon.
def prueba_niveles():
    print("\n--- PRUEBA DE VELOCIDADES ---")
    cambiar_direccion(ADELANTE)
    for nivel in NIVELES:
        ramp_to(velocidad_actual, nivel, PASO_RAMPA, DELAY_RAMPA_MS)
        print(f"[NIVEL] {nivel} %")
        mantener(MANTENER_MS)
    ramp_to(velocidad_actual, 0, PASO_RAMPA, DELAY_RAMPA_MS)
    print("[STOP] Motor detenido")
    stop()
    sleep_ms(PAUSA_INVERSION_MS)


# TODO 2: la secuencia del CHALLENGE 06
def secuencia_challenge():
    print("\n--- CHALLENGE 06 ---")
    cambiar_direccion(ADELANTE)                                  # 1) FORWARD
    ramp_to(0, 100, PASO_RAMPA, DELAY_RAMPA_MS)                  # 2) rampa 0 -> 100
    mantener(MANTENER_MS)                                        # 3) mantener 2 s
    ramp_to(100, 0, PASO_RAMPA, DELAY_RAMPA_MS)                  # 4) rampa 100 -> 0
    cambiar_direccion(REVERSA)                                   # 5) REVERSE (ya en 0 %)
    ramp_to(0, 75, PASO_RAMPA, DELAY_RAMPA_MS)                   # 6) rampa 0 -> 75
    mantener(MANTENER_MS)                                        # 7) mantener 2 s
    ramp_to(75, 0, PASO_RAMPA, DELAY_RAMPA_MS)                   # 8) rampa 75 -> 0
    print("[STOP] Motor detenido")
    stop()                                                       # 9) STOP


# ---------------- Inicio ----------------
print("DO 04 - SMART MOTOR CONTROLLER")
print(f"Pines: GP2=IN1, GP3=IN2, GP4=ENA/PWM ({PWM_FREQ} Hz)")
print(f"Zona muerta compensada: 1 % logico = {MIN_DUTY} % real")
stop()
sleep_ms(1000)

numero_ciclo = 0

try:
    # La demostracion se repite para poder grabar la evidencia en cualquier momento
    while True:
        numero_ciclo += 1
        print(20 * "=")
        print(f"CICLO {numero_ciclo}")
        prueba_niveles()
        secuencia_challenge()
        sleep_ms(PAUSA_CICLO_MS)
finally:
    # Ctrl-C (o cualquier error): apagar el motor antes de salir
    ENA.duty_u16(0)
    IN1.value(0)
    IN2.value(0)
    print("\n[FIN] Motor apagado")