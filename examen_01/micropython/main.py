from machine import Pin, Timer
from time import ticks_ms, ticks_diff, sleep_ms


# =========================================================
# PINES
# =========================================================

btn_a = Pin(16, Pin.IN, Pin.PULL_UP)
btn_b = Pin(17, Pin.IN, Pin.PULL_UP)

led_rojo = Pin(13, Pin.OUT)
led_amarillo = Pin(14, Pin.OUT)
led_verde = Pin(15, Pin.OUT)


# =========================================================
# TIEMPOS
# =========================================================

T_ESPERA_B = 5000
T_ACCESO = 3000
T_BLOQUEO = 10000
T_REBOTE = 250

MAX_FALLOS = 3


# =========================================================
# ESTADOS
# =========================================================

BLOQUEADO = 0
ESPERANDO_B = 1
ACCESO = 2
BLOQUEO_SEGURIDAD = 3

estado = BLOQUEADO
fallos = 0


# =========================================================
# EVENTOS
# =========================================================

evento_a = False
evento_b = False

evento_timeout = False
evento_fin_acceso = False
evento_fin_bloqueo = False


# =========================================================
# ANTIRREBOTE
# =========================================================

ultimo_a = 0
ultimo_b = 0


# =========================================================
# TIMERS
# =========================================================

tim_espera = Timer()
tim_acceso = Timer()
tim_bloqueo = Timer()


# =========================================================
# LEDs
# =========================================================

def leds(rojo, amarillo, verde):
    led_rojo.value(rojo)
    led_amarillo.value(amarillo)
    led_verde.value(verde)


# =========================================================
# MENSAJE INICIAL
# =========================================================

def mostrar_bloqueado():
    print()
    print("==============================")
    print("[LISTO] SISTEMA BLOQUEADO")
    print("Secuencia correcta: A -> B")
    print("==============================")


# =========================================================
# REGISTRAR FALLO
# =========================================================

def registrar_fallo(mensaje):

    global fallos
    global estado

    fallos += 1

    print()
    print(mensaje)
    print("[ERROR] Intentos fallidos:", fallos)

    # -----------------------------------------------------
    # 3 fallos -> bloqueo de seguridad
    # -----------------------------------------------------

    if fallos >= MAX_FALLOS:

        estado = BLOQUEO_SEGURIDAD

        leds(1, 0, 0)

        print()
        print("[BLOQUEO] 3 errores detectados")
        print("[BLOQUEO] Sistema bloqueado 10 segundos")

        tim_bloqueo.init(
            mode=Timer.ONE_SHOT,
            period=T_BLOQUEO,
            callback=fin_bloqueo
        )

    # -----------------------------------------------------
    # Todavía puede intentar nuevamente
    # -----------------------------------------------------

    else:

        estado = BLOQUEADO

        leds(1, 0, 0)

        print("[LISTO] Intenta nuevamente con A -> B")


# =========================================================
# INTERRUPCIONES DE BOTONES
# =========================================================

def irq_a(pin):

    global evento_a
    global ultimo_a

    ahora = ticks_ms()

    if ticks_diff(ahora, ultimo_a) > T_REBOTE:

        ultimo_a = ahora
        evento_a = True


def irq_b(pin):

    global evento_b
    global ultimo_b

    ahora = ticks_ms()

    if ticks_diff(ahora, ultimo_b) > T_REBOTE:

        ultimo_b = ahora
        evento_b = True


# =========================================================
# CALLBACKS DE TIMERS
# =========================================================

def timeout(timer):

    global evento_timeout

    evento_timeout = True


def fin_acceso(timer):

    global evento_fin_acceso

    evento_fin_acceso = True


def fin_bloqueo(timer):

    global evento_fin_bloqueo

    evento_fin_bloqueo = True


# =========================================================
# CONFIGURAR INTERRUPCIONES
# =========================================================

btn_a.irq(
    trigger=Pin.IRQ_FALLING,
    handler=irq_a
)

btn_b.irq(
    trigger=Pin.IRQ_FALLING,
    handler=irq_b
)


# =========================================================
# ESTADO INICIAL
# =========================================================

leds(1, 0, 0)

mostrar_bloqueado()


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

while True:

    # =====================================================
    # EVENTO BOTÓN A
    # =====================================================

    if evento_a:

        evento_a = False

        # -------------------------------------------------
        # Sistema bloqueado -> comenzar secuencia
        # -------------------------------------------------

        if estado == BLOQUEADO:

            estado = ESPERANDO_B

            leds(0, 1, 0)

            print()
            print("[A] Boton A detectado")
            print("[ESPERA] Presiona B antes de 5 segundos")

            tim_espera.init(
                mode=Timer.ONE_SHOT,
                period=T_ESPERA_B,
                callback=timeout
            )

        # -------------------------------------------------
        # Ya estamos esperando B
        # -------------------------------------------------

        elif estado == ESPERANDO_B:

            print("[INFO] A ignorado: ya se espera B")

        # -------------------------------------------------
        # Acceso activo
        # -------------------------------------------------

        elif estado == ACCESO:

            print("[INFO] A ignorado: acceso activo")

        # -------------------------------------------------
        # Bloqueo de seguridad
        # -------------------------------------------------

        elif estado == BLOQUEO_SEGURIDAD:

            print("[INFO] A ignorado: bloqueo de seguridad")


    # =====================================================
    # EVENTO BOTÓN B
    # =====================================================

    if evento_b:

        evento_b = False

        # -------------------------------------------------
        # B después de A -> acceso correcto
        # -------------------------------------------------

        if estado == ESPERANDO_B:

            tim_espera.deinit()

            estado = ACCESO
            
            fallos = 0
            
            leds(0, 0, 1)

            print()
            print("[B] Boton B detectado")
            print("[OK] ACCESO CONCEDIDO")
            print("[TIMER] Acceso activo durante 3 segundos")

            tim_acceso.init(
                mode=Timer.ONE_SHOT,
                period=T_ACCESO,
                callback=fin_acceso
            )

        # -------------------------------------------------
        # B antes que A
        # -------------------------------------------------

        elif estado == BLOQUEADO:

            registrar_fallo(
                "[ERROR] B fue presionado antes que A"
            )

        # -------------------------------------------------
        # Acceso activo
        # -------------------------------------------------

        elif estado == ACCESO:

            print("[INFO] B ignorado: acceso activo")

        # -------------------------------------------------
        # Bloqueo de seguridad
        # -------------------------------------------------

        elif estado == BLOQUEO_SEGURIDAD:

            print("[INFO] B ignorado: bloqueo de seguridad")


    # =====================================================
    # TIMEOUT DE 5 SEGUNDOS
    # =====================================================

    if evento_timeout:

        evento_timeout = False

        if estado == ESPERANDO_B:

            registrar_fallo(
                "[TIMEOUT] No se presiono B antes de 5 segundos"
            )


    # =====================================================
    # FIN DEL ACCESO
    # =====================================================

    if evento_fin_acceso:

        evento_fin_acceso = False

        if estado == ACCESO:

            estado = BLOQUEADO

            leds(1, 0, 0)

            print()
            print("[TIMER] Fin del acceso")

            mostrar_bloqueado()


    # =====================================================
    # FIN DEL BLOQUEO DE SEGURIDAD
    # =====================================================

    if evento_fin_bloqueo:

        evento_fin_bloqueo = False

        if estado == BLOQUEO_SEGURIDAD:

            fallos = 0

            estado = BLOQUEADO

            leds(1, 0, 0)

            print()
            print("[TIMER] Fin del bloqueo")
            print("[RESET] Intentos fallidos = 0")

            mostrar_bloqueado()


    sleep_ms(10)