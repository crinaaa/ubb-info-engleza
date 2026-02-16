class Route:
    def __init__(self, route_id: int, length:int):
        self._id = route_id
        self._length = length

    @property
    def id(self):
        return self._id

    @property
    def length(self):
        return self._length