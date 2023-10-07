from gpiozero import LED
led_erd = LED(21)
while True:
      user_input =input()
      if user_input =="on":
          led_erd.on()
      elif user_input =="off":
        led_erd.off()
      else:
          print("comando invalido")  