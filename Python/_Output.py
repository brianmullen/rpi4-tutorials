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
