#!/usr/bin/env python3
#-----------------------------------------------------
#
#		This is a program for all ADC chip. It 
#	converts analog signal to digital signal.
#

from time import sleep
from _Core import PinResistor, OutputPin, InputOutputPin, PinIO

class ADC0834BadChannel(ValueError):
    "Error rased when an invalid channel is given to an :class:`ADC0834`"

class ADC0834BadFrequency(ValueError):
    "Error rased when an invalid frequency is given to an :class:`ADC0834`"

class ADC0834(object):
    def __init__(self, chip_select_pin: int = 17, clock_pin: int = 18, io_pin: int = 27, channel: int = 0, frequency: int = 250_000, resistor: PinResistor = PinResistor.NONE):
        if not 0 <= channel < 4:
            raise ADC0834BadChannel('channel must be between 0 and 3')
        self.__channel = channel
        if not 10_000 <= frequency < 400_000:
            raise ADC0834BadFrequency('frequency must be between 10,000 and 400,000')
        self.__frequency = frequency
        self.__chip_select = OutputPin(chip_select_pin, resistor=resistor)
        self.__clock = OutputPin(clock_pin, resistor=resistor)
        self.__io = InputOutputPin(io_pin, io=PinIO.OUTPUT, resistor=resistor)
        super().__init__()

    def __del__(self):
        if self.__chip_select is not None:
            self.close()

    @property
    def is_closed(self) -> bool:
        return self.__chip_select is None

    @property
    def channel(self):
        return self.__channel
    
    @channel.setter
    def channel(self, newValue: int):
        if not 0 <= newValue < 4:
            raise ADC0834BadChannel('channel must be between 0 and 3')
        if self.__channel != newValue:
            self.__channel = newValue

    @property
    def frequency(self):
        return self.__frequency

    @property
    def value(self):
        self.__io.io = PinIO.OUTPUT
        self.__chip_select.value = 0

        # Start bit
        self.__clock.value = 0
        self.__io.value = 1
        self.__tick()
        self.__clock.value = 1
        self.__tick()

        # Single End mode
        self.__clock.value = 0
        self.__io.value = 1
        self.__tick()
        self.__clock.value = 1
        self.__tick()

        # ODD
        odd = self.__channel & 1
        self.__clock.value = 0
        self.__io.value = odd
        self.__tick()
        self.__clock.value = 1
        self.__tick()

        # Select
        select = int(self.__channel > 1 & 1)
        self.__clock.value = 0
        self.__io.value = select
        self.__tick()
        self.__clock.value = 1
        self.__tick()

        # Allow the MUX to settle and set IO to INPUT
        self.__clock.value = 0
        self.__io.io = PinIO.INPUT
        self.__tick()

        # Read the value from MSB to LSB
        value1 = 0
        for i in range(0, 8):
            self.__clock.value = 1  
            self.__tick()
            self.__clock.value = 0  
            self.__tick()
            value1 = value1 << 1 | self.__io.value

        # Read the value from LSB to MSB
        value2 = 0
        for i in range(0, 8):
            value2 = value2 | self.__io.value << i
            self.__clock.value = 1  
            self.__tick()
            self.__clock.value = 0  
            self.__tick()

        # Clear all internal registers and set IO to OUTPUT
        self.__chip_select.value = 1
        self.__io.io = PinIO.OUTPUT

        # Only return value if valid
        return value1 if value1 == value2 else 0

    def close(self):
        if self.__chip_select is not None:
            self.__chip_select.close()
            self.__chip_select = None
        if self.__clock is not None:
            self.__clock.close()
            self.__clock = None
        if self.__io is not None:
            self.__io.close()
            self.__io = None
    
    def __tick(self):
        sleep(1 / self.__frequency / 2)
