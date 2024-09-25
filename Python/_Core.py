from enum import Enum
import RPi.GPIO as GPIO

class PinIO(Enum):
    INPUT = GPIO.IN
    OUTPUT = GPIO.OUT

class Pin(object):
    def __init__(self, pin: int, io: PinIO):
        self.__pin = pin
        self.__io = io
        super().__init__()
        GPIO.setup(pin, io.value)
    
    def __del__(self):
        if self.__pin is not None:
            self.close()
    
    @property
    def pin(self) -> int:
        return self.__pin

    @property
    def io(self) -> PinIO:
        return self.__io

    @property
    def is_closed(self) -> bool:
        return self.__pin is None

    def close(self):
        self.__pin = None
        self.__io = None

    def _setIO(self, newValue: PinIO):
        if not self.is_closed and self.__io != newValue:
            self.__io = newValue
            GPIO.setup(self.__pin, newValue.value)

    def _read(self):
        if not self.is_closed and self.__io == PinIO.INPUT:
            return GPIO.input(self.__pin)
        else:
            return None
    
    def _write(self, newValue):
        if not self.is_closed and self.__io == PinIO.OUTPUT:
            GPIO.output(self.__pin, newValue)

class OutputPin(Pin):
    def __init__(self, pin):
        super().__init__(pin, io=PinIO.OUTPUT)
    
    @property
    def value(self):
        return None

    @value.setter
    def value(self, newValue):
        self._write(newValue)

class InputPin(Pin):
    def __init__(self, pin):
        super().__init__(pin, io=PinIO.INPUT)
    
    @property
    def value(self):
        return self._read()

class InputOutputPin(Pin):
    def __init__(self, pin, io: PinIO = PinIO.OUTPUT):
        super().__init__(pin, io=io)
    
    @property
    def value(self):
        return self._read()
    
    @value.setter
    def value(self, newValue):
        self._write(newValue)
    
    @property
    def io(self) -> PinIO:
        return super().io

    @io.setter
    def io(self, newValue: PinIO):
        self._setIO(newValue)
