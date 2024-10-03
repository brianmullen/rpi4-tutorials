from types import LambdaType
import RPi.GPIO as GPIO

class KeyPad(object):
    def __init__(self, rows=[26,19,13,6], cols=[5,22,27,17], keys=[['1','2','3','A'],['4','5','6','B'],['7','8','9','C'],['*','0','#','D']], returnKey=None):
        self.__rows = rows
        self.__cols = cols
        self.__keys = keys
        self.__returnKey = returnKey
        self.__onReturn = None
        self.__output = ''
        self.__state = [[0 for x in range(len(rows))] for y in range(len(cols))] 
        super().__init__()
        for rowPin in self.__rows:
            GPIO.setup(rowPin, GPIO.OUT)
        for colPin in self.__cols:
            GPIO.setup(colPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    @property 
    def onReturn(self) -> LambdaType:
        return self.__onReturn
    
    @onReturn.setter
    def onReturn(self, newValue: LambdaType):
        self.__onReturn = newValue

    def processEvents(self):
        for row, rowPin in enumerate(self.__rows):
            GPIO.output(rowPin, GPIO.HIGH)
            for col, colPin in enumerate(self.__cols):
                newState = GPIO.input(colPin)
                if self.__state[row][col] != newState:
                    self.__state[row][col] = newState
                    if newState == 1:
                        self.__onKeyPressed(self.__keys[row][col])
            GPIO.output(rowPin, GPIO.LOW)
    
    def __onKeyPressed(self, key):
        if key == self.__returnKey:
            if len(self.__output) > 0:
                if self.__onReturn is not None:
                    self.__onReturn(self.__output)
                self.__output = ''
        else:
            self.__output += str(key)
