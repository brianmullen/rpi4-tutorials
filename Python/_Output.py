from _Core import OutputPin, PinResistor

class LED(OutputPin):
    def __init__(self, pin, resistor: PinResistor = PinResistor.NONE):
        super().__init__(pin, resistor=resistor)

    def on(self):
        self.value = 1
    
    def off(self):
        self.value = 0
