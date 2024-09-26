from time import sleep
from _App import App
import RPi.GPIO as GPIO

#####
# Doesn't Work!
# Motor from kit seems to be dead
#####

def main():
    fps = 1.0/60.0
    pwm_pin=12
    GPIO.setup(pwm_pin, GPIO.OUT)

    pwm = GPIO.PWM(pwm_pin, 100)
    pwm.start(0)

    while True:
        pwm_percent = float(input('PWM%: '))
        pwm.ChangeDutyCycle(pwm_percent)
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
