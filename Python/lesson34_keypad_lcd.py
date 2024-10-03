from time import sleep
from _App import App
from _KeyPad import KeyPad
import _LCD1602 as LCD 

def onReturn(value):
    LCD.write(0, 0, 'User Input Was:')
    LCD.write(0, 1, value)
    sleep(5)
    LCD.clear()

def main():
    fps = 0.2
    keypad = KeyPad(returnKey='D')
    keypad.onReturn = lambda output: onReturn(output)
    LCD.init(0x27, 1)
    
    while True:
        LCD.write(0, 0, 'Input Value:')
        keypad.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
LCD.clear()
