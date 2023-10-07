from gpiozero import LED
import time

# Define el pin GPIO al que está conectado el LED (en este caso, GPIO 17)
led = LED(17)

try:
    # Pide al usuario que ingrese el tiempo en segundos
    tiempo_encendido = int(input("Ingresa el tiempo de encendido del LED (segundos): "))
    led.on()
    print(f"LED encendido durante {tiempo_encendido} segundos...")
    time.sleep(tiempo_encendido)
    led.off()
    print("LED apagado")

except KeyboardInterrupt:
    pass