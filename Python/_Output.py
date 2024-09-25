import RPi.GPIO as GPIO
from enum import Enum
from _Core import OutputPin, PinResistor

class LEDState(Enum):
    OFF = 1
    ON = 2

class LED(OutputPin):
    def __init__(self, pin, resistor: PinResistor = PinResistor.NONE):
        self.__state = LEDState.OFF
        super().__init__(pin, resistor=resistor)

    @property
    def state(self) -> LEDState:
        return self.__state

    def on(self):
        self.value = 1
        self.__state = LEDState.ON
    
    def off(self):
        self.value = 0
        self.__state = LEDState.OFF
    
    def toggle(self):
        if self.__state == LEDState.ON:
            self.off()
        else:
            self.on()

class PWMLED(LED):
    def __init__(self, pin, frequency: float = 100, resistor: PinResistor = PinResistor.NONE):
        self.__frequency = frequency
        self.__pwm = None
        self.__duty_cycle = 0.0
        super().__init__(pin, resistor=resistor)
        self.__pwm = GPIO.PWM(pin, frequency)
    
    @property
    def frequency(self) -> float:
        return self.__frequency
    
    @frequency.setter
    def frequency(self, newValue: float):
        if self.__frequency != newValue:
            self.__frequency = newValue
            self.__pwm.ChangeFrequence(newValue)
    
    @property
    def duty_cycle(self) -> float:
        return self.__duty_cycle
    
    @duty_cycle.setter
    def duty_cycle(self, newValue: float):
        if self.__duty_cycle != newValue:
            if self.__duty_cycle == 0 and newValue != 0:
                self.__pwm.start(newValue)
            elif self.__duty_cycle !=0 and newValue == 0:
                self.__pwm.stop()
            else:
                self.__pwm.ChangeDutyCycle(newValue)
            self.__duty_cycle = newValue
    
    def close(self):
        self.__pwm.stop()
        super().close()

class RGBLED(object):
    def __init__(self, red_pin: int, green_pin: int, blue_pin: int, resistor: PinResistor = PinResistor.NONE):
        self.__red = LED(red_pin, resistor=resistor)
        self.__green = LED(green_pin, resistor=resistor)
        self.__blue = LED(blue_pin, resistor=resistor)
        super().__init__()
    
    def __del__(self):
        if self.__red is not None:
            self.close()

    @property
    def red(self) -> LED:
        return self.__red
    
    @property
    def green(self) -> LED:
        return self.__green
    
    @property
    def blue(self) -> LED:
        return self.__blue

    @property
    def is_closed(self) -> bool:
        return self.__red is None

    def on(self):
        if not self.is_closed:
            self.__red.on()
            self.__green.on()
            self.__blue.on()
    
    def off(self):
        if not self.is_closed:
            self.__red.off()
            self.__green.off()
            self.__blue.off()
    
    def toggle(self):
        if not self.is_closed:
            self.__red.toggle()
            self.__green.toggle()
            self.__blue.toggle()

    def close(self):
        if self.__red is not None:
            self.__red.close()
            self.__red = None
        if self.__green is not None:
            self.__green.close()
            self.__green = None
        if self.__blue is not None:
            self.__blue.close()
            self.__blue = None
