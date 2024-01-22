# Include the library files
import RPi.GPIO as GPIO
import smbus
import paho.mqtt.client as mqtt
from time import sleep

# Some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68  # MPU6050 device address

# MQTT Configuration
mqtt_broker = "192.168.0.20"
mqtt_port = 1883
mqtt_topic_x = "angles/x"
mqtt_topic_y = "angles/y"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe([(mqtt_topic_x, 0), (mqtt_topic_y, 0)])

def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} {msg.payload}")

# Set up MQTT client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker, mqtt_port, 60)

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
    low = bus.read_byte_data(Device_Address, addr + 1)

    # Concatenate higher and lower value
    value = ((high << 8) | low)

    # To get a signed value from MPU6050
    if value > 32768:
        value = value - 65536
    return value

MPU_Init()

while True:
    # Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT)
    acc_y = read_raw_data(ACCEL_YOUT)
    acc_z = read_raw_data(ACCEL_ZOUT)

    # Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT)
    gyro_y = read_raw_data(GYRO_YOUT)
    gyro_z = read_raw_data(GYRO_ZOUT)

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

    # Convert accelerometer X and Y axis values from 0 to 180
    value_x = round((Ax - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    value_y = round((Ay - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    # Publish angles to MQTT
    mqtt_client.publish(mqtt_topic_x, value_x)
    mqtt_client.publish(mqtt_topic_y, value_y)

    # Print the angles
    print("El ángulo del eje X es:", value_x)
    print("El ángulo del eje Y es:", value_y)

    sleep(2.0)
