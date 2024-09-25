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
