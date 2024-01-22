import RPi.GPIO as GPIO
import time

# Configuración de pines
pin_sensor_agua_analogico = 26  # Puedes cambiar el número del pin según la conexión real

def obtener_porcentaje_nivel():
    # Configura el pin como entrada analógica
    GPIO.setup(pin_sensor_agua_analogico, GPIO.IN)

    # Lee el valor analógico del pin
    valor_analogico = GPIO.input(pin_sensor_agua_analogico)

    # Convierte el valor leído a un rango de 0-100
    porcentaje_nivel = (valor_analogico / 1023.0) * 100.0

    return porcentaje_nivel

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        while True:
            porcentaje_nivel_actual = obtener_porcentaje_nivel()
            print(f'Porcentaje de nivel: {porcentaje_nivel_actual:.2f}%')
            time.sleep(1)

    except KeyboardInterrupt:
        print("Programa interrumpido por el usuario.")

    finally:
        GPIO.cleanup()
