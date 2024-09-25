from time import sleep
from _App import App
from _Core import PinResistor
from _Output import LED
from _Input import Button, ButtonState

def on_button_state(led: LED, state: ButtonState):
    if state == ButtonState.UP:
        led.off()
    else:
        led.on()

def main():
    fps = 0.2
    led = LED(6)
    led.off()
    button = Button(26, PinResistor.PULL_UP)
    button.state_change = lambda state: on_button_state(led, state)

    while True:
        button.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()

# pull up resistor = 1 default, 0 when button pressed; resisitor connected to 3.3v
# pull down resistor = 0 default, 1 when button pressed; resisitor connected to ground
