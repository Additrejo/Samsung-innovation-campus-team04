from gpiozero import DigitalInputDevice
from time import sleep

# Configuración del sensor DHT11
dht11_pin = 4  # Cambia el número del pin según tu configuración

dht11_sensor = DigitalInputDevice(dht11_pin, pull_up=True, bounce_time=1)

try:
    while True:
        dht11_sensor.when_activated = None  # Deshabilita las interrupciones
        sleep(1)  # Espera un segundo para que el sensor se estabilice

        try:
            # Lee los bits del sensor DHT11
            bits = []
            for i in range(40):
                start_time = time()
                while dht11_sensor.is_active == 0:
                    pass

                while dht11_sensor.is_active == 1:
                    pass

                bit_time = time() - start_time
                bits.append(1 if bit_time > 0.00005 else 0)

            # Procesa los bits en datos de temperatura y humedad
            humidity = bits[0:8]
            humidity_point = bits[8:16]
            temperature = bits[16:24]
            temperature_point = bits[24:32]
            checksum = bits[32:40]

            if sum(humidity + humidity_point + temperature + temperature_point) == checksum[0]:
                temperature_value = int("".join(map(str, temperature)), 2)
                humidity_value = int("".join(map(str, humidity)), 2)
                print(f"Temperatura: {temperature_value}°C, Humedad: {humidity_value}%")
            else:
                print("Error en la verificación del checksum")

        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"Error: {e}")
        finally:
            dht11_sensor.when_activated = None  # Restaura las interrupciones
            sleep(2)  # Espera antes de la próxima lectura

except KeyboardInterrupt:
    print("\nPrograma terminado por el usuario.")
