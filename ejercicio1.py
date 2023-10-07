from gpiozero import LED, Button
from time import sleep

# Configuración de los pines
led = LED(17)  # Pin GPIO17
button = Button(2)  # Pin GPIO2

# Función para encender y apagar el LED
def toggle_led():
    led.toggle()

# Asociar la función al evento de presionar el botón
button.when_pressed = toggle_led

try:
    while True:
        sleep(1)

except KeyboardInterrupt:
    # Limpiar los pines GPIO al presionar Ctrl+C
    led.off()
