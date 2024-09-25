from time import sleep
from _App import App
from _Output import LED

def main():
    fps = 1.0
    bit1 = LED(24)
    bit2 = LED(23)
    bit4 = LED(22)
    bit8 = LED(27)
    bit16 = LED(17)

    bit1.off()
    bit2.off()
    bit4.off()
    bit8.off()
    bit16.off()

    for i in range(0, 32, 1):
        if bool(i & 0b00001):
            bit1.on()
        else:
            bit1.off()

        if bool(i & 0b00010):
            bit2.on()
        else:
            bit2.off()

        if bool(i & 0b00100):
            bit4.on()
        else:
            bit4.off()

        if bool(i & 0b01000):
            bit8.on()
        else:
            bit8.off()

        if bool(i & 0b10000):
            bit16.on()
        else:
            bit16.off()
        
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
