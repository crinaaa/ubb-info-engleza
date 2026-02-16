class Ship:
    def __init__(self, coordinates):
        self._coordinates = coordinates
        self._hits = []

    @property
    def coordinates(self):
        return self._coordinates

    def is_hit(self, x:int, y:int):
        if (x,y) in self._coordinates:
            if (x,y) not in self._hits:
                self._hits.append((x,y))
            return True
        return False

    def is_sunk(self):
        return len(self._hits) == len(self._coordinates)