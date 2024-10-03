from time import sleep
from _App import App
from _ADC0834 import ADC0834

def main():
    fps = 0.2
    adc = ADC0834(chip_select_pin=17, clock_pin=18, io_pin=27)

    while True:
        lightValue = adc.value
        print('Light Value: ', lightValue)
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
