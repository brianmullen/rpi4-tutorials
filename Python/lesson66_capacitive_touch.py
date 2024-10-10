from time import sleep
from _App import App
from _Input import Button

def main():
    fps = 0.2
    button = Button(17)
    button.state_change = lambda buttonState: print(buttonState)
    while True:
        button.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
