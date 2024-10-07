from enum import Enum

class BoundsType(Enum):
    LOWER = 1
    UPPER = 2

class Bounds(object):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper
        super().__init__()
