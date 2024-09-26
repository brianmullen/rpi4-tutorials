from time import sleep
from _App import App
import _LCD1602

def main():
    fps = 0.2
    _LCD1602.init(0x27, 1)

    while True:
        _LCD1602.write(0, 0, 'Hello World')
        _LCD1602.write(0, 1, 'Welcome!')
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()

sleep(0.2)
_LCD1602.clear()

# Check if I2C is installed:
# lsmod | grep i2c
