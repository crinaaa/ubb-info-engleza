class Address:
    def __init__(self, add_id:int, name:str, number:int, x:int, y:int):
        self._id = add_id
        self._name = name
        self._number = number
        self._x = x
        self._y = y

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y