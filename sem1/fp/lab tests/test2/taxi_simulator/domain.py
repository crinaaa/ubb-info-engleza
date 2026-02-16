class Taxi:
    def __init__(self, taxi_id:int, x:int, y:int, fare:int):
        self._id = taxi_id
        self._x = x
        self._y = y
        self._fare = fare

    @property
    def id(self):
        return self._id

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def fare(self):
        return self._fare

    @fare.setter
    def fare(self, value):
        self._fare = value
