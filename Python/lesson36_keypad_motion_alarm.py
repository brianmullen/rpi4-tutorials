from time import sleep
from _App import App
from _KeyPad import KeyPad
from _Core import InputPin
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
hasIntruder=-1

def onReturn(value):
    global userInput
    userInput = value
    print('New: ', value)

def main():
    global userInput, password, currentState, hasIntruder

    fps = 0.2
    sensor = InputPin(21)
    keypad = KeyPad(returnKey='D')
    keypad.onReturn = lambda output: onReturn(output)
    LCD.init(0x27, 1)
    
    def processEvents():
        global userInput
        while userInput != '*':
            keypad.processEvents()
            sleep(0.1)

    readThread = Thread(target=processEvents)
    readThread.daemon = True
    readThread.start()

    while userInput != '*':
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
                LCD.write(0, 1, password)
                sleep(2)
                LCD.clear()
                currentState=previousState
                if currentState == AlarmState.ARMED:
                    LCD.write(0, 0, 'Armed')
                elif currentState == AlarmState.DISARMED:
                    LCD.write(0, 0, 'Disarmed')
        
        if currentState == AlarmState.ARMED:
            newHasIntruder=sensor.value
            if newHasIntruder != hasIntruder:
                hasIntruder = newHasIntruder
                if hasIntruder == 1:
                    LCD.write(0, 1, 'Intruder Alert')
                elif hasIntruder == 0:
                    LCD.write(0, 1, 'All Clear     ')
        
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
LCD.clear()
