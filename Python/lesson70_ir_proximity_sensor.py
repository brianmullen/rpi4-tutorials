from time import sleep
from _App import App
from _Core import InputPin, PinResistor

def main():
    fps = 0.1
    sensor = InputPin(17, resistor = PinResistor.PULL_UP)

    while True:
        print(sensor.value, end='\r')
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
