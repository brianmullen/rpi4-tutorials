from enum import Enum
from types import LambdaType
from _Core import InputPin, PinResistor

class ButtonState(Enum):
    DOWN = 1
    UP = 2

class Button(InputPin):
    def __init__(self, pin, resistor: PinResistor = PinResistor.PULL_UP):
        self.__state = ButtonState.UP
        self.__state_change = None
        if resistor == PinResistor.PULL_UP or resistor == PinResistor.PULL_UP_EXTERNAL:
            self.__idle_value = 1
        else:
            self.__idle_value = 0
        self.__lastValue = self.__idle_value
        super().__init__(pin, resistor=resistor)

    @property
    def state(self) -> ButtonState:
        return self.__state

    @property
    def state_change(self) -> LambdaType:
        return self.__state_change

    @state_change.setter
    def state_change(self, newValue: LambdaType):
        self.__state_change = newValue

    def processEvents(self):
        newValue = self.value
        if newValue != self.__lastValue:
            self.__lastValue = newValue
            self.__state = ButtonState.UP if newValue == self.__idle_value else ButtonState.DOWN
            if self.__state_change is not None:
                self.__state_change(self.__state)
