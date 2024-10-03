from time import sleep
from _App import App
from _KeyPad import KeyPad
import _LCD1602 as LCD
from threading import Thread
from enum import Enum

class AlarmState(Enum):
    ARMED = 1
    DISARMED = 2
    PASSWORD = 3

userInput=''
password='1234'
currentState = AlarmState.DISARMED

def onReturn(value):
    global userInput
    userInput = value
    print('New: ', value)

def main():
    global userInput, password, currentState

    fps = 0.2
    keypad = KeyPad(returnKey='D')
    keypad.onReturn = lambda output: onReturn(output)
    LCD.init(0x27, 1)
    
    def processEvents():
        while True:
            keypad.processEvents()
            sleep(0.1)

    readThread = Thread(target=processEvents)
    readThread.daemon = True
    readThread.start()

    while True:
        currentInput=userInput
        newState=currentState

        if currentInput == 'A' + password:
            newState = AlarmState.ARMED
        elif currentInput == 'B' + password:
            newState = AlarmState.DISARMED
        elif currentInput == 'C' + password:
            newState = AlarmState.PASSWORD

        if newState != currentState:
            previousState=currentState
            currentState=newState
            LCD.clear()
            if newState == AlarmState.ARMED:
                LCD.write(0, 0, 'Armed')
            elif newState == AlarmState.DISARMED:
                LCD.write(0, 0, 'Disarmed')
            elif newState == AlarmState.PASSWORD:
                LCD.write(0, 0, 'Enter Password:')
                while userInput == 'C' + password:
                    pass
                password = userInput
                LCD.clear()
                LCD.write(0, 0, password)
                sleep(2)
                LCD.clear()
                currentState=previousState
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
LCD.clear()
