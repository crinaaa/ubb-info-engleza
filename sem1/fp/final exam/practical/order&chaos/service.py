import random

from domain import Board
from exception import GameException
from repository import GameRepository


class GameService:
    def __init__(self):
        self._board = Board()
        self._repo = GameRepository()

    def __str__(self):
        return self._board.__str__()

    def save_game(self):
        # Access the private matrix from the Board domain object
        self._repo.save(self._board.board)

    def load_game(self):
        data = self._repo.load()
        if data:
            # Update the board state with the loaded data
            self._board._board = data
            return True
        return False

    def is_board_full(self):
        return self._board.is_full()

    def order_move(self, row:int, col:int, symbol:int):
        if not ( 0<=row<=5 and 0<=col<=5 ):
            raise GameException("Out of bound position!")
        if self._board.get_cell(row, col) != 0:
            raise GameException("Cell already occupied!")

        self._board.move(row,col,symbol)

    # def computer_move(self):
    #     # check if ORDER can win in the next move
    #
    #     for r in range(6):
    #         for c in range(6):
    #             if self._board.get_cell(r,c) == 0:
    #                 for sym in [1, 2]:
    #                     self._board.move(r,c,sym)
    #                     if self.check_win():
    #                         return r,c,sym
    #                     self._board.board[r][c] = 0
    #
    #     #random move
    #     empties = []
    #     for r in range(6):
    #         for c in range(6):
    #             if self._board.get_cell(r,c) == 0:
    #                 empties.append((r,c))
    #     row, col = random.choice(empties)
    #     symbol = random.choice(["X","O"])
    #     self._board.move(row, col, symbol)
    #     return row, col, symbol

    def computer_move(self):
        # 1. PRIORITY: Block any immediate 5-in-a-row
        for r in range(6):
            for c in range(6):
                if self._board.get_cell(r, c) == 0:
                    for symbol_to_test in [1, 2]:  # Test both X and O
                        self._board.board[r][c] = symbol_to_test
                        if self.check_win():
                            # If this move wins, Chaos takes the spot!
                            # Chaos doesn't have to use the same symbol,
                            # but it's easiest to just place it to break the line.
                            self._board.board[r][c] = 0  # reset simulation
                            self._board.move(r, c, symbol_to_test)
                            return r, c, symbol_to_test
                        self._board.board[r][c] = 0  # reset simulation

        # 2. SECONDARY: If no immediate win, make a random valid move
        empties = [(r, c) for r in range(6) for c in range(6) if self._board.get_cell(r, c) == 0]
        if empties:
            row, col = random.choice(empties)
            symbol = random.choice(["X", "O"])
            self._board.move(row, col, symbol)
            return row, col, symbol


    def check_win(self):
        for i in range(6):
            for j in range(6):
                symbol = self._board.get_cell(i,j)
                if symbol == 0:
                    continue

                if self.check_from_pos(i,j,symbol):
                    return True
        return False


    def check_from_pos(self, row:int, col:int, symbol:int):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 0
            for i in range(5):
                nr, nc = row + dr*i, col + dc*i
                if 0 <= nr < 6 and 0 <= nc < 6 and self._board.get_cell(nr, nc) == symbol:
                    count += 1
                else:
                    break
            if count == 5:
                return True
        return False