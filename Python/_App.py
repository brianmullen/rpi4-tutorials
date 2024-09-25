from enum import Enum
from types import LambdaType
import RPi.GPIO as GPIO

class PinType(Enum):
    BCM = GPIO.BCM
    BOARD = GPIO.BOARD

class App(object):
    def __init__(self, type: PinType = PinType.BCM):
        self.__type = type
        self.__main = None
        super().__init__()
        GPIO.setmode(type.value)
    
    def __del__(self):
        self.close()
    
    @property
    def type(self) -> PinType:
        return self.__type

    @property 
    def main(self) -> LambdaType:
        return self.__main

    @main.setter
    def main(self, newValue: LambdaType):
        if self.__type is not None:
            self.__main = newValue

    def run(self):
        try:
            if self.__main is not None:
                self.__main()
        except KeyboardInterrupt:
            print(' Interrupted')
        self.close()
    
    def close(self):
        self.__main = None
        if self.__type is not None:
            self.__type = None
            GPIO.cleanup()
            print("Done!")
