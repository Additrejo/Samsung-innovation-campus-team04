import Adafruit_DHT
import time
import json
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt

# Define el tipo de sensor (DHT11) y el número de pin al que está conectado.
sensor = Adafruit_DHT.DHT11
pin = 17  # Ajusta el número de pin según tu configuración.

# Configuración del cliente MQTT
mqtt_broker = "192.168.100.168"  # Cambia esto al URL de tu broker MQTT
mqtt_topic_temp = "tem"
mqtt_topic_humidity = "hum"

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker con código de resultado "+str(rc))

# Conecta las funciones de callback
client.on_connect = on_connect

# Conéctate al broker MQTT
client.connect(mqtt_broker, 1883, 60)

# Inicializa listas para almacenar datos para graficar
temperatura_data = []
humedad_data = []
tiempo_data = []

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print("Temperatura: {:.1f}°C, Humedad: {:.1f}%".format(temperature, humidity))

        # Publica los datos en los topics MQTT
        client.publish(mqtt_topic_temp, temperature)
        client.publish(mqtt_topic_humidity, humidity)

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
        print("Error al leer el sensor. Intentando nuevamente...")

    # Espera unos segundos antes de realizar la próxima lectura.
    time.sleep(2)
