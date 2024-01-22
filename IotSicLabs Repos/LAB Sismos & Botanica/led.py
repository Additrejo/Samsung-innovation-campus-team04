from gpiozero import LED
from time import sleep

# Define el pin GPIO que estás utilizando
pin_led = 13

# Crea un objeto LED en el pin especificado
led = LED(pin_led)

try:
    # Enciende el LED
    led.on()
    print("LED encendido")

    # Espera 5 segundos
    sleep(5)

    # Apaga el LED
    led.off()
    print("LED apagado")

finally:
    # Asegúrate de que los recursos se liberen al salir del programa
    led.close()
