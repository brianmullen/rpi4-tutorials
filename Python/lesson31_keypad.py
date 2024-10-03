from time import sleep
from _App import App
import RPi.GPIO as GPIO

def main():
    fps = 0.2
    rows = [26,19,13,6]
    cols = [5,22,27,17]
    keys = [[1,2,3,'A'],[4,5,6,'B'],[7,8,9,'C'],['*',0,'#','D']]

    GPIO.setup(rows[0], GPIO.OUT)
    GPIO.setup(rows[1], GPIO.OUT)
    GPIO.setup(rows[2], GPIO.OUT)
    GPIO.setup(rows[3], GPIO.OUT)
    GPIO.setup(cols[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(cols[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(cols[2], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(cols[3], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    uRow = int(input('Which Row? '))
    uCol = int(input('Which Column? '))

    while True:
        GPIO.output(rows[uRow], GPIO.HIGH)
        isPressed = GPIO.input(cols[uCol])
        GPIO.output(rows[uRow], GPIO.LOW)
        
        if isPressed:
            print(keys[uRow][uCol])
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()