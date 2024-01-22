from gpiozero import LED
from time import sleep
from signal import pause
Led = LED(16)
Led1 = LED(20)
Led2 = LED(21)
while True:
    #led1 grenn
	Led.on()
	sleep(4)
	Led.off()
	sleep(1)
	#led2 yellow
	Led1.on()
	sleep(3)
	Led1.blink(0.5)
	sleep(5)
	Led1.off()
	sleep(1)
	#led3 red
	Led2.on()
	sleep(3)
	Led2.off()
	sleep(1)
	
