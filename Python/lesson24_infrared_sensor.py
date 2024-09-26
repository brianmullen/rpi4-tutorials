from time import sleep
from _App import App
from _Core import InputPin

def main():
    fps = 0.1
    sensor = InputPin(23)
    
    # normalize sensor
    sleep(10)

    while True:
        motion = sensor.value
        print(motion)
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
