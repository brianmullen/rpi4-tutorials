from time import sleep
from _App import App
from _KeyPad import KeyPad

def main():
    fps = 0.2
    keypad = KeyPad(returnKey='D')
    keypad.onReturn = lambda output: print(output)

    while True:
        keypad.processEvents()
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
