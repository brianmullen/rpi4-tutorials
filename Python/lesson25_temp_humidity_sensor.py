from time import sleep
import dht11
from _App import App

def main():
    fps = 0.2
    sensor = dht11.DHT11(17)

    while True:
        result = sensor.read()
        if result.is_valid():
            temperature = round(result.temperature * (9.0/5.0) + 32, 1)
            print("Temperature:", temperature, "Humidity:", result.humidity)
        sleep(fps)

app = App()
app.main = lambda: main()
app.run()
