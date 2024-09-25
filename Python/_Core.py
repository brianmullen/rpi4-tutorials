from enum import Enum
import RPi.GPIO as GPIO

class PinIO(Enum):
    INPUT = GPIO.IN
    OUTPUT = GPIO.OUT

class PinResistor(Enum):
    NONE = 1
    PULL_UP = 2
    PULL_DOWN = 3
    PULL_UP_EXTERNAL = 4
    PULL_DOWN_EXTERNAL = 5

class Pin(object):
    def __init__(self, pin: int, io: PinIO, resistor: PinResistor = PinResistor.NONE):
        self.__pin = pin
        self.__io = io
        self.__resistor = resistor
        super().__init__()
        if resistor == PinResistor.PULL_DOWN:
            GPIO.setup(pin, io.value, pull_up_down=GPIO.PUD_DOWN)
        elif resistor == PinResistor.PULL_UP:
            GPIO.setup(pin, io.value, pull_up_down=GPIO.PUD_UP)
        else:
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
    def resistor(self) -> PinResistor:
        return self.__resistor

    @property
    def is_closed(self) -> bool:
        return self.__pin is None

    def close(self):
        self.__pin = None
        self.__io = None
        self.__resistor = None

    def _setIO(self, newValue: PinIO):
        if not self.is_closed and self.__io != newValue:
            self.__io = newValue
            if self.__resistor == PinResistor.PULL_DOWN:
                GPIO.setup(self.__pin, newValue.value, pull_up_down=GPIO.PUD_DOWN)
            elif self.__resistor == PinResistor.PULL_UP:
                GPIO.setup(self.__pin, newValue.value, pull_up_down=GPIO.PUD_UP)
            else:
                GPIO.setup(self.__pin, newValue.value)

    def _setResistor(self, newValue: PinResistor):
        if not self.is_closed and self.__resistor != newValue:
            self.__resistor = newValue

    def _read(self):
        if not self.is_closed and self.__io == PinIO.INPUT:
            return GPIO.input(self.__pin)
        else:
            return None
    
    def _write(self, newValue):
        if not self.is_closed and self.__io == PinIO.OUTPUT:
            GPIO.output(self.__pin, newValue)

class OutputPin(Pin):
    def __init__(self, pin, resistor: PinResistor = PinResistor.NONE):
        super().__init__(pin, io=PinIO.OUTPUT, resistor=resistor)
    
    @property
    def value(self):
        return None

    @value.setter
    def value(self, newValue):
        self._write(newValue)

class InputPin(Pin):
    def __init__(self, pin, resistor: PinResistor = PinResistor.NONE):
        super().__init__(pin, io=PinIO.INPUT, resistor=resistor)
    
    @property
    def value(self):
        return self._read()

class InputOutputPin(Pin):
    def __init__(self, pin, io: PinIO = PinIO.OUTPUT, resistor: PinResistor = PinResistor.NONE):
        super().__init__(pin, io=io, resistor=resistor)
    
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
