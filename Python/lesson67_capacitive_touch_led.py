from time import sleep
from _App import App
from _Output import RGBLED
from _Input import Button, ButtonState
from enum import Enum

class LEDSTATE(Enum):
    OFF = 1
    RED = 2
    GREEN = 3
    BLUE = 4

state = LEDSTATE.OFF

def main():
    fps = 0.2
    led = RGBLED(red_pin=5, green_pin=6, blue_pin=26)
    led.off()
    button = Button(17)

    def toggleState(buttonState):
        global state

        if buttonState == ButtonState.DOWN:
            if state == LEDSTATE.OFF:
                state = LEDSTATE.RED
                led.red.on()
            elif state == LEDSTATE.RED:
                state = LEDSTATE.GREEN
                led.red.off()
                led.green.on()
            elif state == LEDSTATE.GREEN:
                state = LEDSTATE.BLUE
                led.green.off()
                led.blue.on()
            elif state == LEDSTATE.BLUE:
                state = LEDSTATE.OFF
                led.off()
    button.state_change = lambda buttonState: toggleState(buttonState)

    while True:
        button.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
