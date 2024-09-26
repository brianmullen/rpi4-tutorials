from time import sleep, time
from _App import App
from _Core import OutputPin, InputPin

def main():
    fps = 0.5
    trigger = OutputPin(23)
    echo = InputPin(24)

    while True:
        trigger.value = 0
        sleep(0.000002)
        trigger.value = 1
        sleep(0.00001)
        trigger.value = 0
        while echo.value == 0:
            pass
        start_time = time()
        while echo.value == 1:
            pass
        stop_time = time()
        ping_travel_time = stop_time - start_time
        total_distance = 767 * ping_travel_time * 5280 * 12 / 3600
        target_distance = total_distance / 2
        print(round(target_distance, 1), ' Inches')

        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
