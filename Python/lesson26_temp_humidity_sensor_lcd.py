from time import sleep
from _App import App
from _Input import ToggleButton
import _LCD1602
import dht11

is_fahrenheit = 1
is_dirty = 0
current_celsius = 0
current_humidity = 0

def toggle_temp():
    global is_fahrenheit, is_dirty
    
    is_fahrenheit = not is_fahrenheit
    is_dirty = 1

def lcd_write():
    global is_dirty, current_celsius, current_humidity

    _LCD1602.write(0, 0, 'Temp: ')
    if is_fahrenheit:
        fahrenheit = current_celsius * (9.0 / 5.0) + 32
        temperature = str(round(fahrenheit, 1))
        temperature_count = len(temperature)
        _LCD1602.write(6, 0, temperature)
        _LCD1602.write(6 + temperature_count, 0, ' F')
    else:
        temperature = str(round(current_celsius, 1))
        temperature_count = len(temperature)
        _LCD1602.write(6, 0, temperature)
        _LCD1602.write(6 + temperature_count, 0, ' C')
    
    humidity = str(round(current_humidity, 1))
    humidity_count = len(humidity)
    _LCD1602.write(0, 1, 'Humidity: ')
    _LCD1602.write(10, 1, humidity)
    _LCD1602.write(10 + humidity_count, 1, '%')

    is_dirty = 0

def main():
    global is_dirty, current_celsius, current_humidity

    fps = 0.2
    _LCD1602.init(0x27, 1)
    sensor = dht11.DHT11(27)
    button = ToggleButton(16)
    button.state_change = lambda state: toggle_temp()

    while True:
        result = sensor.read()

        if result.is_valid():
            current_celsius = result.temperature
            current_humidity = result.humidity
            is_dirty = 1
        
        button.processEvents()

        if is_dirty:
            lcd_write()

        sleep(fps)

app = App()
app.main = lambda: main()
app.run()

sleep(0.2)
_LCD1602.clear()

# detect address for lcd:
# i2cdetect -y 1
