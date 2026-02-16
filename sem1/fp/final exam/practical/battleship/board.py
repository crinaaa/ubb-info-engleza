from ship import Ship


class Board:
    def __init__(self, rows:int, col:int):
        self._rows = rows
        self.cols = col
        self._ships = []
        self._attacks = {}

    def add_ship(self, ship:Ship):
        if len(self._ships) >=2:
            self._ships.pop(0)
        self._ships.append(ship)

    def receive_attack(self,x,y):
        for ship in self._ships:
            if ship.is_hit(x,y):
                self._attacks[(x,y)] = "X"
                return "hit"
        self._attacks[(x,y)] = "o"
        return "miss"

    def all_ships_sunk(self):
        if not self._ships:
            return False
        return all(ship.is_sunk() for ship in self._ships)