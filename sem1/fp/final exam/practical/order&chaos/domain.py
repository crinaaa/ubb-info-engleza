from texttable import Texttable

class Board:
    def __init__(self):
        self._board = [[0 for i in range(6)] for j in range(6)]
        #0 no piece
        #2 - letter O
        #1 - letter X

    @property
    def board(self):
        return self._board

    def move(self, row:int, col:int, symbol:int):
        if symbol == "X":
            val = 1
        else:
            val = 2
        self._board[row][col] = val

    def get_cell(self, row:int, col:int):
        return self._board[row][col]

    def is_full(self):
        full = True
        for i in range(6):
            for j in range(6):
                if self._board[i][j] == 0:
                    full = False
        return full

    def symbol(self, row:int, col:int):
        if self._board[row][col] == 0:
            return " "
        elif self._board[row][col] == 2:
            return "O"
        else:
            return "X"

    def __str__(self):
        table = Texttable()
        for i in range(0,6):
            row_data = []
            for j in range(0,6):
                row_data.append(self.symbol(i,j))
            table.add_row(row_data)
        return table.draw()