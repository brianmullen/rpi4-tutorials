from time import sleep
from _App import App
from _Core import PinResistor
from _Output import RGBLED, RGBColor
from _Input import ToggleButton

red_value=0.99
green_value=0.99
blue_value=0.99

def brighten(led: RGBLED, colors, increment, minValue, maxValue):
    global red_value, green_value, blue_value

    if RGBColor.RED in colors:
        red_value *= increment
        if red_value > maxValue:
            red_value = minValue
        led.red.duty_cycle = int(red_value)
    if RGBColor.GREEN in colors:
        green_value *= increment
        if green_value > maxValue:
            green_value = minValue
        led.green.duty_cycle = int(green_value)
    if RGBColor.BLUE in colors:
        blue_value *= increment
        if blue_value > maxValue:
            blue_value = minValue
        led.blue.duty_cycle = int(blue_value)

def main():
    fps = 0.1
    led = RGBLED(red_pin=5, green_pin=6, blue_pin=26)
    led.off()
    red_button = ToggleButton(17, PinResistor.PULL_UP)
    red_button.state_change = lambda state: brighten(led, {RGBColor.RED}, 1.5849, 0.99, 100.0)
    green_button = ToggleButton(27, PinResistor.PULL_UP)
    green_button.state_change = lambda state: brighten(led, {RGBColor.GREEN}, 1.5849, 0.99, 100.0)
    blue_button = ToggleButton(22, PinResistor.PULL_UP)
    blue_button.state_change = lambda state: brighten(led, {RGBColor.BLUE}, 1.5849, 0.99, 100.0)
    
    while True:
        red_button.processEvents()
        green_button.processEvents()
        blue_button.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
