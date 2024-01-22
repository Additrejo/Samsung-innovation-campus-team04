import Adafruit_DHT
import time
import paho.mqtt.client as mqtt

#MQTT 
cliente = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Conectado a MQTT ")
    cliente.publish("sensores/dht11/tem", payload=humidity, qos=2, retain=False)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
cliente.on_connect = on_connect
cliente.connect("localhost", 1883, 60)
    
# Configuración del sensor DHT11
PIN_DHT11 = 17  # Reemplaza con el número de pin GPIO correcto

# Bucle principal
while True:
    try:
        # Leer datos desde el sensor DHT11
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, PIN_DHT11)

        # Verificar si la lectura fue exitosa
        if humidity is not None and temperature is not None: 
            # Imprimir los datos en la consola
            print(f'Temperatura: {temperature:.2f} °C, Humedad: {humidity:.2f}%')
            cliente.publish("sensores/dht11/temp", payload=temperature, qos=2, retain=False)
            cliente.publish("sensores/dht11/hum", payload=temperature, qos=2, retain=False)
        else:
            print('Error al leer el sensor DHT11. Intentando nuevamente...')

        # Esperar un tiempo antes de realizar la siguiente lectura
        time.sleep(0.5)
    except KeyboardInterrupt:
        # Manejar la interrupción del teclado (Ctrl+C) para salir del bucle
        print('Programa interrumpido. Saliendo...')
        break

