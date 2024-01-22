import RPi.GPIO as GPIO
import time

# Configuración de pines
servo_pin = 25  # Puedes cambiar el número de pin según tu conexión

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Crear un objeto PWM para el servo
pwm = GPIO.PWM(servo_pin, 50)  # Frecuencia de 50 Hz

# Función para mover el servo a una posición específica
def move_servo(position):
    duty_cycle = 2 + (position / 18)  # Calcular el ciclo de trabajo (duty cycle)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # Esperar un segundo para que el servo llegue a la posición
    pwm.ChangeDutyCycle(0)  # Detener el pulso para evitar vibraciones

# Mover el servo a la posición 0 grados
pwm.start(0)
move_servo(0)

# Esperar un segundo
time.sleep(1)

# Mover el servo a la posición 180 grados
move_servo(70)

# Limpiar y liberar recursos al finalizar
pwm.stop()
GPIO.cleanup()
