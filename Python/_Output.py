from _Core import OutputPin

class LED(OutputPin):
    def __init__(self, pin):
        super().__init__(pin)

    def on(self):
        self.value = 1
    
    def off(self):
        self.value = 0
