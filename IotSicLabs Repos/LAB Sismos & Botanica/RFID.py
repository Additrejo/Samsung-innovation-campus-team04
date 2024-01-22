import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Escanea una tarjeta RFID...")
    id, text = reader.read()
    print("ID de la tarjeta: {}".format(id))
    print("Datos almacenados en la tarjeta: {}".format(text))

finally:
    GPIO.cleanup()
