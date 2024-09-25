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
            self._idle_value = 1
        else:
            self._idle_value = 0
        self._lastValue = self._idle_value
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
        self._set_last_value(self.value)
    
    def _set_last_value(self, newValue):
        if self._lastValue != newValue:
            self._lastValue = newValue
            newState = ButtonState.UP if newValue == self._idle_value else ButtonState.DOWN
            self._set_state(newState)

    def _set_state(self, newValue):
        if self.__state != newValue:
            self.__state = newValue
            if self.__state_change is not None:
                self.__state_change(self.__state)

class ToggleButton(Button):
    def __init__(self, pin, resistor: PinResistor = PinResistor.PULL_UP):
        super().__init__(pin, resistor=resistor)
    
    def _set_last_value(self, newValue):
        if self._lastValue != newValue:
            self._lastValue = newValue
            if newValue == self._idle_value:
                newState = ButtonState.UP if self.state == ButtonState.DOWN else ButtonState.DOWN
                self._set_state(newState)
