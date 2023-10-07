from gpiozero import LED
from time import sleep
led_dictionary = {
       "red": LED(21),
       "yellow": LED(20),
       "grenn": LED(16)
}
while True:
    for led in led_dictionary.keys():
        led_dictionary[led].blink(on_time = 1, off_time = 1)
        sleep(2)
        #led_dictionary[led].off()