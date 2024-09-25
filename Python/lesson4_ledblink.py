from time import sleep
from _App import App
from _Output import LED

def main():
    fps = 0.4
    led = LED(17)
    led.off()

    while True:
        blinkTimes = int(input('How many times do you want the LED to blink? '))
        sleep(fps)
        for i in range(0, blinkTimes, 1):
            led.on()
            sleep(fps)
            led.off()
            sleep(fps)

app = App()
app.main = lambda: main()
app.run()
