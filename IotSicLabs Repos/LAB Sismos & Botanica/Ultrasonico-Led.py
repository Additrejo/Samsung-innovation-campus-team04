from gpiozero import DistanceSensor       #Librería sensor ultrasonico'''
from gpiozero import LED                  #Librería LED'''
from gpiozero import DigitalInputDevice   #Librería Sensor DHT11'''

from time import sleep
import time 

Led_1 = LED(14) 
ultrasonic = DistanceSensor(echo= 23, trigger= 24)
while True:
    distance = round(ultrasonic.distance * 100, 3)
    print(f"Distancia: {distance}  cm" )
    time.sleep(0.1)
    if distance <= 20:
         print('Muy cerca')
         Led_1.on()
    else:
          print('lejos')
          Led_1.off() 
 
