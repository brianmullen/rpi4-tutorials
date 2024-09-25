from time import sleep
from _App import App
from _Core import PinResistor
from _Output import PWMLED
from _Input import ToggleButton

increment = 1.5849
steps = 0
brightness = 0

def on_increment(led: PWMLED):
    global increment, steps, brightness

    steps = min(steps + 1, 10)
    if steps == 10:
        brightness = 1
    else:
        brightness = min(increment**steps, 100) / 100
        brightness = min(max(brightness, 0.0), 1.0)
    led.duty_cycle = brightness * 100.0

def on_decrement(led: PWMLED):
    global increment, steps, brightness

    steps = max(steps - 1, 0)
    if steps == 0:
        brightness = 0
    else:
        brightness = max(increment**steps, 0) / 100
        brightness = min(max(brightness, 0.0), 1.0)
    led.duty_cycle = brightness * 100.0

def main():
    fps = 0.01
    led = PWMLED(12)
    led.off()
    incButton = ToggleButton(5, PinResistor.PULL_UP)
    incButton.state_change = lambda state: on_increment(led)
    decButton = ToggleButton(6, PinResistor.PULL_UP)
    decButton.state_change = lambda state: on_decrement(led)

    while True:
        incButton.processEvents()
        decButton.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()

# BRIGHTNESS == DUTY CYCLE
# REFRESH RATE aka flicker == FREQUENCY
