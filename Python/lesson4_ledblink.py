from time import sleep
import RPi.GPIO as GPIO
from _Output import LED

GPIO.setmode(GPIO.BCM)
fps = 0.4
led = LED(17)

try:
    led.off()

    while True:
        blinkTimes = int(input('How many times do you want the LED to blink? '))
        for i in range(0, blinkTimes, 1):
            led.on()
            sleep(fps / 2)
            led.off()
            sleep(fps)
except KeyboardInterrupt:
    print(' Interrupted')

GPIO.cleanup()
print("Done!")
