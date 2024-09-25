from time import sleep
from _App import App
from _Core import PinResistor
from _Output import LED
from _Input import ToggleButton

def main():
    fps = 0.1
    led = LED(6)
    led.off()
    button = ToggleButton(26, PinResistor.PULL_UP)
    button.state_change = lambda state: led.toggle()
    
    while True:
        button.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()

# pull up resistor = 1 default, 0 when button pressed; resisitor connected to 3.3v
# pull down resistor = 0 default, 1 when button pressed; resisitor connected to ground
