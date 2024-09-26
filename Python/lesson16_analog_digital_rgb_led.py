from time import sleep
from _App import App
from _Output import RGBLED
from _ADC0834 import ADC0834

def main():
    fps = 1.0/60.0
    adc = ADC0834(chip_select_pin=17, clock_pin=18, io_pin=27)
    led = RGBLED(red_pin=23, green_pin=24, blue_pin=25)
    led.off()
    
    while True:
        adc.channel = 0
        red_value = adc.value / 255.0 * 100
        led.red.duty_cycle = int(red_value)

        adc.channel = 1
        green_value = adc.value / 255.0 * 100
        led.green.duty_cycle = int(green_value)

        adc.channel = 2
        blue_value = adc.value / 255.0 * 100
        led.blue.duty_cycle = int(blue_value)
        
        print("red: ", int(red_value), "green: ", int(green_value), "blue: ", int(blue_value))
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
