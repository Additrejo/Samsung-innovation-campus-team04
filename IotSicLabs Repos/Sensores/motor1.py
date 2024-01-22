import RPi.GPIO as GPIO
import time
import random

servo_pin = 27  # Cambia el número de pin según tu conexión

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # Frecuencia de 50 Hz

def move_servo(position, duration=0.1):
    duty_cycle = 2 + (position / 18)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(duration)
    pwm.ChangeDutyCycle(0)

def simulate_earthquake(intensity):
    for _ in range(3):
        for _ in range(intensity * 2):
            move_servo(random.uniform(0, 60), duration=0.05)
        time.sleep(0.2)
        for _ in range(intensity * 2, 0, -1):
            move_servo(random.uniform(0, 60), duration=0.05)
        time.sleep(0.2)

try:
    pwm.start(0)

    while True:
        intensity = random.randint(5, 10)  # Elige una intensidad aleatoria
        print(f"Simulando sismo de intensidad {intensity}")
        simulate_earthquake(intensity)
        time.sleep(random.uniform(3, 10))  # Espera entre sismos

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()
