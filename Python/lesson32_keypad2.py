from time import sleep
from _App import App
import RPi.GPIO as GPIO

def main():
    fps = 0.2
    rows = [26,19,13,6]
    cols = [5,22,27,17]
    keys = [[1,2,3,'A'],[4,5,6,'B'],[7,8,9,'C'],['*',0,'#','D']]
    state = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    for rowPin in rows:
        GPIO.setup(rowPin, GPIO.OUT)
    for colPin in cols:
        GPIO.setup(colPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        for row, rowPin in enumerate(rows):
            GPIO.output(rowPin, GPIO.HIGH)
            for col, colPin in enumerate(cols):
                previousState = state[row][col]
                newState = GPIO.input(colPin)
                if previousState != newState:
                    state[row][col] = newState
                    if newState == 1:
                        print(keys[row][col])
            GPIO.output(rowPin, GPIO.LOW)
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
