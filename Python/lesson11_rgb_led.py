from time import sleep
from _App import App
from _Core import PinResistor
from _Output import RGBLED
from _Input import ToggleButton

def main():
    fps = 0.1
    led = RGBLED(red_pin=5, green_pin=6, blue_pin=26)
    led.off()
    red_button = ToggleButton(17, PinResistor.PULL_UP)
    red_button.state_change = lambda state: led.red.toggle()
    green_button = ToggleButton(27, PinResistor.PULL_UP)
    green_button.state_change = lambda state: led.green.toggle()
    blue_button = ToggleButton(22, PinResistor.PULL_UP)
    blue_button.state_change = lambda state: led.blue.toggle()
    
    while True:
        red_button.processEvents()
        green_button.processEvents()
        blue_button.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
