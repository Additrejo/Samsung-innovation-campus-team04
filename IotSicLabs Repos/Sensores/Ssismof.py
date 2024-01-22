import RPi.GPIO as GPIO
import time
import random
import paho.mqtt.client as mqtt

# Configuración del servo
servo_pin = 23  # Cambia el número de pin según tu conexión
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # Frecuencia de 50 Hz

# Configuración del servidor MQTT y el topic
broker_address = "192.168.0.20"  # Coloca la dirección de tu broker MQTT
topic = "topic3"  # Coloca el mismo topic que configuraste en Node-RED

# Variable para almacenar el mensaje recibido
num = ""

# Función que se llama cuando se recibe un mensaje MQTT
def on_message(client, userdata, message):
    global num
    try:
        num = float(message.payload.decode())
        print(f"Mensaje recibido: {num}")
    except ValueError:
        print("Mensaje MQTT no válido. Se espera un número.")

# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message

# Conexión al broker MQTT y suscripción al topic
client.connect(broker_address)
client.subscribe(topic)

# Inicio del bucle para mantener la conexión y procesar mensajes
client.loop_start()

# Función para mover el servo según la intensidad del sismo
def move_servo_intensity(intensity):
    for _ in range(int(intensity * 0.5)):
        move_servo(random.uniform(0, 60), duration=0.05)
    time.sleep(0.2)
    for _ in range(int(intensity * 0.5), 0, -1):
        move_servo(random.uniform(0, 60), duration=0.05)
    time.sleep(0.2)

# Función para mover el servo con una intensidad específica
def move_servo(position, duration=0.1):
    duty_cycle = 2 + (position / 18)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(duration)
    pwm.ChangeDutyCycle(0)

try:
    pwm.start(0)

    while True:
        # Revisa el mensaje MQTT y ajusta la intensidad del sismo
        if num and isinstance(num, (int, float)):
            print(f"Simulando sismo de intensidad {num}")
            move_servo_intensity(num)
        else:
            print("Mensaje MQTT no válido. Se espera un número.")

        time.sleep(0.2 )  # Espera antes de revisar el siguiente mensaje

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()
