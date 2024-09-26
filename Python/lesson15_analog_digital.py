from time import sleep
from _App import App
from _Output import PWMLED
from _ADC0834 import ADC0834

def main():
    fps = 1.0/60.0
    adc = ADC0834(chip_select_pin=17, clock_pin=18, io_pin=27)
    led = PWMLED(26, frequency=100)
    led.off()
    
    while True:
        brightness = adc.value / 255.0
        led.duty_cycle = brightness * 100
        print(brightness)
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
