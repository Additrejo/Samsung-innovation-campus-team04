# Include the library files
import RPi.GPIO as GPIO
import smbus
from time import sleep
import json
import paho.mqtt.client as mqtt

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set the first servo motor pin as an output pin
GPIO.setup(4, GPIO.OUT)
pwm1 = GPIO.PWM(4, 50)
pwm1.start(0)

# Set the second servo motor pin as an output pin
GPIO.setup(27, GPIO.OUT)
pwm2 = GPIO.PWM(27, 50)
pwm2.start(0)

# Some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F
GYRO_XOUT  = 0x43
GYRO_YOUT  = 0x45
GYRO_ZOUT  = 0x47

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68  # MPU6050 device address

def angle(Angle, pwm):
    duty = Angle / 18 + 2
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    pwm.ChangeDutyCycle(0)  # Detener el pulso para mantener la posición

def setAngle():
    angle(90, pwm1)
    angle(90, pwm2)

def MPU_Init():
    # Write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    # Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    # Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    # Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    # Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    # Concatenate higher and lower value
    value = ((high << 8) | low)

    # To get a signed value from MPU6050
    if value > 32768:
        value = value - 65536
    return value

# Configuración MQTT
mqtt_broker = "192.168.0.20"  # Cambia esto al broker MQTT que estés usando
mqtt_port = 1883
mqtt_topic = "topic4"  # Cambia esto al topic que desees

def on_connect(client, userdata, flags, rc):
    print("Conectado con código de resultado " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

# Inicializar el MPU6050
MPU_Init()

while True:
    # Leer datos brutos del acelerómetro y giroscopio
    acc_x = read_raw_data(ACCEL_XOUT)
    acc_y = read_raw_data(ACCEL_YOUT)
    acc_z = read_raw_data(ACCEL_ZOUT)

    gyro_x = read_raw_data(GYRO_XOUT)
    gyro_y = read_raw_data(GYRO_YOUT)
    gyro_z = read_raw_data(GYRO_ZOUT)

    # Convertir datos brutos en ángulos
    Ax = acc_x / 16384.0
    Ay = acc_y / 16384.0 
    Az = acc_z / 16384.0

    Gx = gyro_x / 131.0
    Gy = gyro_y / 131.0
    Gz = gyro_z / 131.0

    in_min = 1
    in_max = -1
    out_min = 0
    out_max = 180

    setAngle()  # Utilizar esta función para configurar el punto del servomotor

    # Convertir valores de los ejes X e Y del acelerómetro de 0 a 180   
    value_x = (Ax - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    value_y = (Ay - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    value_x = int(value_x)
    value_y = int(value_y)

    # Imprimir los ángulos en la consola
    print("El ángulo del eje X es:", value_x)
    print("El ángulo del eje Y es:", value_y)

    # Publicar los ángulos en el topic MQTT
    mqtt_payload = {
        "angle_x": value_x,
        "angle_y": value_y
    }
    client.publish(mqtt_topic, json.dumps(mqtt_payload))

    # Controlar los servomotores
    if 0 <= value_x <= 180:
        angle(value_x, pwm1)
    if 0 <= value_y <= 180:
        angle(value_y, pwm2)

    sleep(1.0)
    sleep(0.5)
