import random

from board import Board
from exceptions import ValidationException, GameException
from ship import Ship


class GameService:
    def __init__(self):
        self._player_ships = []
        self._computer_ships = []
        self._player_attacks = []
        self._computer_attacks = []
        self.player_board = Board(6,6)
        self.computer_board = Board(6,6)
        self.game_started = False

    def parse_coordinates(self, coordinates:str):
        coords = []
        for i in range(0,len(coordinates),2):
            col = coordinates[i].upper()
            row = coordinates[i+1]
            x = ord(col) - ord('A')
            y = int(row)
            coords.append((x,y))
        return coords

    def place_ship(self, coordinates:str):
        coords = self.parse_coordinates(coordinates)
        for x,y in coords:
            if x<0 or y<0 or x>5 or y>5:
                raise ValidationException("Part of the ship is outside the board!")

        xs = [c[0] for c in coords]
        ys = [c[1] for c in coords]

        is_horizontal = len(set(ys)) == 1 and (max(xs) - min(xs)) == 2
        is_vertical = len(set(xs)) == 1 and (max(ys) - min(ys)) == 2

        if not is_vertical and not is_horizontal:
            raise ValidationException("Invalid placement!")

        new_ship = Ship(coords)
        self.player_board.add_ship(new_ship)

    def start_game(self):
        if len(self.player_board._ships) < 2:
            raise GameException("Place two ships first!")

        self.computer_board._ships = []
        while len(self.computer_board._ships) < 2:
            x, y = random.randint(0, 5), random.randint(0, 5)
            direction = random.choice(['H', 'V'])

            coords = []
            for i in range(3):
                coords.append((x + i, y) if direction == 'H' else (x, y + i))

            # Validation check for computer ships
            try:
                for cx, cy in coords:
                    if not (0 <= cx <= 5 and 0 <= cy <= 5): raise ValueError()
                for s in self.computer_board._ships:
                    if any(c in s.coordinates for c in coords): raise ValueError()

                self.computer_board.add_ship(Ship(coords))
            except ValueError:
                continue

        self.game_started = True


    def player_attack(self, coord_str):
        if not self.game_started:
            raise GameException("The game has not started yet!")

        x = ord(coord_str[0].upper()) - ord('A')
        y = int(coord_str[1])

        if not (0<=x<=5 and 0<=y<=5):
            raise ValidationException("Invalid position!")

        if (x,y) in self.computer_board._attacks:
            raise GameException("Square already hit!")

        result = self.computer_board.receive_attack(x,y)
        return result

    def computer_attack(self):
        while True:
            x = random.randint(0, 5)
            y = random.randint(0, 5)
            if (x,y) not in self.player_board._attacks:
                result = self.player_board.receive_attack(x,y)
                col = chr(ord('A')+x)
                coord_str = f"{col}{y}"
                return result, coord_str

    def check_winner(self):
        if self.player_board.all_ships_sunk():
            return "computer"
        if self.computer_board.all_ships_sunk():
            return "player"
        return None

    def get_player_status(self,x,y):
        if (x,y) in self.player_board._attacks:
            return self.player_board._attacks[(x,y)]

        for ship in self.player_board._ships:
            if (x,y) in ship.coordinates:
                return "+"
        return "."

    def get_computer_status(self,x,y, cheat=False):
        if (x,y) in self.computer_board._attacks:
            return self.computer_board._attacks[(x,y)]

        if cheat:
            for ship in self.computer_board._ships:
                if (x,y) in ship.coordinates:
                    return "+"
        return "."