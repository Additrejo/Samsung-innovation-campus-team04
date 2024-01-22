import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import Adafruit_DHT
import json
import matplotlib.pyplot as plt

# Configuración de pines para el sensor de humedad
pin_sensor_humedad = 22  # GPIO17 o el pin que hayas elegido
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_sensor_humedad, GPIO.IN)

# Configuración de pines para el sensor de temperatura y humedad (DHT11)
pin_sensor_dht = 17  # Ajusta el número de pin según tu configuración.

# Configuración del cliente MQTT
mqtt_broker = "192.168.0.20"  # Cambia esto al URL de tu broker MQTT
mqtt_topic_humedad = "humedad"
mqtt_topic_temp = "temperatura"
mqtt_topic_estado = "estado"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker con código de resultado " + str(rc))

# Conecta las funciones de callback
client.on_connect = on_connect

# Conéctate al broker MQTT
client.connect(mqtt_broker, 1883, 60)

# Inicializa listas para almacenar datos para graficar
temperatura_data = []
humedad_data = []
tiempo_data = []

try:
    while True:
        # Sensor de humedad
        humedad_actual = GPIO.input(pin_sensor_humedad)
        estado_humedad = "Seco" if humedad_actual else "Húmedo"
        print(f'Estado Humedad: {estado_humedad}')

        # Publica el estado en el topic MQTT
        client.publish(mqtt_topic_estado, estado_humedad)

        # Sensor de temperatura y humedad (DHT11)
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin_sensor_dht)

        if humidity is not None and temperature is not None:
            print(f'Temperatura: {temperature:.1f}°C, Humedad: {humidity:.1f}%')

            # Publica los datos en los topics MQTT
            client.publish(mqtt_topic_temp, temperature)
            client.publish(mqtt_topic_humedad, humidity)

            # Almacena datos para graficar
            temperatura_data.append(temperature)
            humedad_data.append(humidity)
            tiempo_data.append(time.time())

            # Grafica la temperatura
            plt.plot(tiempo_data, temperatura_data, label='Temperatura (°C)')
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Temperatura (°C)')
            plt.legend()
            plt.pause(2)  # Pausa para permitir la actualización del gráfico

            # Grafica la humedad
            plt.plot(tiempo_data, humedad_data, label='Humedad (%)')
            plt.xlabel('Tiempo (s)')
            plt.ylabel('Humedad (%)')
            plt.legend()
            plt.pause(2)  # Pausa para permitir la actualización del gráfico

        else:
            print("Error al leer el sensor DHT11. Intentando nuevamente...")

        # Espera unos segundos antes de realizar la próxima lectura.
        time.sleep(3)

except KeyboardInterrupt:
    print("Programa interrumpido por el usuario.")

finally:
    GPIO.cleanup()
