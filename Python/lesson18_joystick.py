from time import sleep
from _App import App
from _Core import PinResistor
from _Input import ToggleButton
from _ADC0834 import ADC0834

def main():
    fps = 1.0/60.0
    adc = ADC0834(chip_select_pin=17, clock_pin=18, io_pin=27)
    button = ToggleButton(26, PinResistor.PULL_UP)
    button.state_change = lambda state: print('button pressed')
    
    while True:
        adc.channel = 0
        x_axis = adc.value
        adc.channel = 1
        y_axis = adc.value
        
        print('X=', x_axis, ' Y=', y_axis)
        button.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
