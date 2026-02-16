class Board:
    def __init__(self):
        self._board = [[' ' for i in range(8)] for j in range(8)]

    @property
    def board(self):
        return self._board

    def set_board(self,x,y,c):
        self._board[x][y] = c