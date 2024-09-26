from time import sleep
from _App import App
# from _Core import OutputPin
from _Output import PWMLED

def main():
    # fps = 1.0
    # active_buzzer = OutputPin(17)
    passive_buzzer = PWMLED(17, 400)
    passive_buzzer.duty_cycle = 50

    while True:
        # active_buzzer.value = 1
        # sleep(1)
        # active_buzzer.value = 0
        # sleep(fps)

        for i in range(150, 2000):
            passive_buzzer.frequency = i
            sleep(0.01)
        for i in range(2000, 150, -1):
            passive_buzzer.frequency = i
            sleep(0.01)

app = App()
app.main = lambda: main()
app.run()
