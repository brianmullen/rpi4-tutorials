class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super().__init__()

class Size(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        super().__init__()

class Rect(object):
    def __init__(self, x, y, width, height):
        self.__position = Position(x, y)
        self.__size = Size(width, height)
        super().__init__()
    
    @property
    def position(self) -> Position:
        return self.__position
    
    @property
    def size(self) -> Size:
        return self.__size

    @property
    def x(self):
        return self.__position.x
    @x.setter
    def x(self, newValue):
        self.__position.x = newValue
    
    @property
    def y(self):
        return self.__position.y
    @y.setter
    def y(self, newValue):
        self.__position.y = newValue
    
    @property
    def width(self):
        return self.__size.width
    @width.setter
    def width(self, newValue):
        self.__size.width = newValue
    
    @property
    def height(self):
        return self.__size.height
    @height.setter
    def height(self, newValue):
        self.__size.height = newValue
