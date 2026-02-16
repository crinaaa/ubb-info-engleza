import random

from domain.board import Board


class GameService:
    def __init__(self):
        self._board = Board()
        self._b_number = 3
        self._e_x = None
        self._e_y = None
        self._game_over = False

    @property
    def game_over(self):
        return self._game_over

    def add_star(self,x:int,y:int):
        self._board.board[x][y] = "*"

    def valid_star_position(self, x: int, y: int):
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return False

        # Check current and all 8 neighbors in one go
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx <= 7 and 0 <= ny <= 7:
                    if self._board.board[nx][ny] == '*':
                        return False
        return True

    def adjacent_e(self, x: int, y: int):
        if x == 0:
            if y == 0:
                if self._board.board[x + 1][y] == 'E' or self._board.board[x][y + 1] == 'E' or \
                        self._board.board[x + 1][y + 1] == 'E':
                    return True
            elif y == 7:
                if self._board.board[x + 1][y] == 'E' or self._board.board[x][y - 1] == 'E' or \
                        self._board.board[x + 1][y - 1] == 'E':
                    return True
            else:
                if self._board.board[x + 1][y] == 'E' or self._board.board[x][y + 1] == 'E' or self._board.board[x][
                    y - 1] == 'E' or self._board.board[x + 1][y + 1] == 'E' or self._board.board[x + 1][y - 1] == 'E':
                    return True
        elif x == 7:
            if y == 0:
                if self._board.board[x - 1][y] == 'E' or self._board.board[x][y + 1] == 'E' or \
                        self._board.board[x - 1][y + 1] == 'E':
                    return True
            elif y == 7:
                if self._board.board[x - 1][y] == 'E' or self._board.board[x][y - 1] == 'E' or \
                        self._board.board[x - 1][y - 1] == 'E':
                    return True
            else:
                if self._board.board[x - 1][y] == 'E' or self._board.board[x][y + 1] == 'E' or self._board.board[x][
                    y - 1] == 'E' or self._board.board[x - 1][y + 1] == 'E' or self._board.board[x - 1][y - 1] == 'E':
                    return True
        else:
            if y == 0:
                if self._board.board[x - 1][y] == 'E' or self._board.board[x + 1][y] == 'E' or self._board.board[x][
                    y + 1] == 'E' or self._board.board[x - 1][y + 1] == 'E' or self._board.board[x + 1][y + 1] == 'E':
                    return True
            elif y == 7:
                if self._board.board[x - 1][y] == 'E' or self._board.board[x + 1][y] == 'E' or self._board.board[x][
                    y - 1] == 'E' or self._board.board[x - 1][y - 1] == 'E' or self._board.board[x + 1][y - 1] == 'E':
                    return True
            else:
                if self._board.board[x - 1][y] == 'E' or self._board.board[x + 1][y] == 'E' or self._board.board[x][
                    y - 1] == 'E' or self._board.board[x][y + 1] == 'E' or self._board.board[x - 1][y - 1] == 'E' or \
                        self._board.board[x - 1][y + 1] == 'E' or self._board.board[x + 1][y - 1] == 'E' or \
                        self._board.board[x + 1][y + 1] == 'E':
                    return True
        return False

    def generate_random_stars(self):
        for _ in range(0,10):
            x = random.randint(0,7)
            y = random.randint(0,7)
            while not self.valid_star_position(x,y):
                x = random.randint(0, 7)
                y = random.randint(0, 7)
            self.add_star(x,y)

    def generate_random_b(self):
        for _ in range(0,self._b_number):
            x = random.randint(0,7)
            y = random.randint(0,7)
            while not self.valid_b_position(x,y):
                x = random.randint(0, 7)
                y = random.randint(0, 7)
            self._board.board[x][y] = "B"

    def generate_random_e(self):
        while True:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if self.valid_b_position(x, y):
                self._board.board[x][y] = "E"
                self._e_x = x  # Store current X
                self._e_y = y  # Store current Y
                break

    def valid_e_position(self, x:int, y:int):
        if self._board.board[x][y] != "*":
            return True
        return False

    def valid_b_position(self,x:int,y:int):
        if self._board.board[x][y] != "*":
            return True
        return False

    def get_board(self, cheat:bool):
        new_board = [[' ' for i in range(9)] for j in range(9)]

        new_board[0][0] = '0'
        new_board[0][1] = '1'
        new_board[0][2] = '2'
        new_board[0][3] = '3'
        new_board[0][4] = '4'
        new_board[0][5] = '5'
        new_board[0][6] = '6'
        new_board[0][7] = '7'
        new_board[0][8] = '8'

        new_board[1][0] = 'A'
        new_board[2][0] = 'B'
        new_board[3][0] = 'C'
        new_board[4][0] = 'D'
        new_board[5][0] = 'E'
        new_board[6][0] = 'F'
        new_board[7][0] = 'G'
        new_board[8][0] = 'H'

        for i in range(8):
            for j in range(8):
                if self._board.board[i][j] == "B":
                    if cheat or self.adjacent_e(i,j):
                        new_board[i+1][j+1] = "B"
                    else:
                        new_board[i+1][j+1] = " "
                else:
                    new_board[i+1][j+1] = self._board.board[i][j]

        return new_board

    def valid_new_e_pos(self,x:int, y:int):
        is_diagonal = abs(x - self._e_x) == abs(y - self._e_y)
        if x == self._e_x or y == self._e_y or is_diagonal:
            return True
        return False

    def warp_command(self, cmd:str):
        dict_let = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        dict_nr = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

        new_x = dict_let[cmd[0]]
        new_y = dict_nr[cmd[1]]

        old_x = self._e_x
        old_y = self._e_y

        if not self.valid_new_e_pos(new_x,new_y):
            return "Invalid move for the Endeavor!"

        while old_x != new_x or old_y != new_y:
            if old_x < new_x:
                old_x += 1
            elif old_x > new_x:
                old_x -= 1
            if old_y < new_y:
                old_y += 1
            elif old_y > new_y:
                old_y -= 1
            if self._board.board[old_x][old_y] == '*':
                return "Invalid move! A star is in the way!"

        if self._board.board[new_x][new_y] == 'B':
            self._game_over = 1
            return "You lost! You stepped on a Blingon Cruiser!"

        self._board.board[self._e_x][self._e_y] = ' '
        self._board.board[new_x][new_y] = 'E'
        self._e_x = new_x
        self._e_y = new_y
        return "True"

    def fire_command(self, cmd:str):
        dict_let = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        dict_nr = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

        target_x = dict_let[cmd[0]]
        target_y = dict_nr[cmd[1]]

        # Check adjacency (Rule 2b)
        if abs(target_x - self._e_x) <= 1 and abs(target_y - self._e_y) <= 1:
            if self._board.board[target_x][target_y] == 'B':
                self._board.board[target_x][target_y] = ' '  # Remove the hit ship
                self.get_new_configuration_for_ships()
                return "True"
            return "No ship at this position!"
        return "You can only fire on adjacent squares!"

    def get_new_configuration_for_ships(self):
        self._b_number -= 1
        if self._b_number == 0:
            self._game_over = 2
        for i in range(8):
            for j in range(8):
                if self._board.board[i][j] == 'B':
                    self._board.board[i][j] = ' '
        self.generate_random_b()