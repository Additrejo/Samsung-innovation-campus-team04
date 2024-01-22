from gpiozero import DistanceSensor, LED
import time
import paho.mqtt.client as mqtt
import subprocess
import matplotlib.pyplot as plt

# Configuración MQTT
broker_address = "192.168.0.20"  # Reemplaza con la dirección IP o nombre de dominio de tu servidor MQTT
topic = "graph2"
client = mqtt.Client()
client.connect(broker_address)

# Inicializar el sensor ultrasónico
ultrasonic = DistanceSensor(echo=23, trigger=24)
Led_1 = LED(14)

# Listas para almacenar datos de distancia y tiempo
distances = []
times = []

try:
    while True:
        distance = round(ultrasonic.distance * 1000, 0)
        current_time = time.time()
        print(f"Distancia: {distance} mm")

        # Publicar la distancia a través de MQTT
        client.publish(topic, str(distance))

        # Almacenar datos para graficar
        distances.append(distance)
        times.append(current_time)

        if distance > 140:
            print('Muestra no detectada')
            Led_1.on()
        else:
            print('Muestra detectada')
            Led_1.off()

        time.sleep(5)

except KeyboardInterrupt:
    # Cerrar la conexión MQTT al finalizar
    client.disconnect()

    # Graficar los datos
    plt.plot(times, distances)
    plt.xlabel('Tiempo')
    plt.ylabel('Distancia (cm)')
    plt.title('Grafico de Distancia')
    plt.grid(True)
    plt.show()
except Exception as e:
    print(f"Error: {str(e)}")
