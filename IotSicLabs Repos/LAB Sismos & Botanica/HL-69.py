import RPi.GPIO as GPIO
import time

# Configuración de pines
pin_sensor = 22  # GPIO17 o el pin que hayas elegido
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_sensor, GPIO.IN)

def obtener_humedad():
    # Lee el valor del pin
    valor_pin = GPIO.input(pin_sensor)

    # El valor leído puede ser 0 (seco) o 1 (húmedo)
    return valor_pin

if __name__ == "__main__":
    try:
        while True:
            humedad_actual = obtener_humedad()
            estado = "Seco" if humedad_actual else "Húmedo"
            print(f'Estado: {estado}')
            time.sleep(1)

    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")

    finally:
        GPIO.cleanup()
