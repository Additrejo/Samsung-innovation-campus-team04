'''
Samsung innovation campus.
Autor: Equipo 4. Juan, Addi, Aldo.
Programa: Ejercicio 2.
Creado: 13/Octubre/2023. 
Versión: 1.0
Descrpción: Programa que con el tiempo escrito en la consola, refleje el led encendido ese tiempo Requistos: LED GPIO17
'''

from gpiozero import LED
import time

#EJERCICIO  2. 

# Define el pin GPIO al que está conectado el LED (en este caso, GPIO 17)
led = LED(17)

try:
    # Pide al usuario que ingrese el tiempo en segundos
    tiempo_encendido = int(input("Ingresa el tiempo de encendido del LED (segundos): "))
    led.on()
    print(f"LED encendido durante {tiempo_encendido} segundos...") 
    time.sleep(tiempo_encendido)    #10000 ms
    led.off()
    print("LED apagado")

except KeyboardInterrupt:
    pass
