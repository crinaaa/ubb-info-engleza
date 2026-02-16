class Board:
    """
    Represents the board of the game.
    Manages piece placement, movement rules, and mill detection.
    """
    def __init__(self):
        self._positions = [" " for i in range(24)]   # the board is empty at the start

        # adjacency list for legal moves
        self._adjacency = {
            0: [1, 9],
            1: [0, 2, 4],
            2: [1, 14],
            3: [4, 10],
            4: [1, 3, 5, 7],
            5: [4, 13],
            6: [7, 11],
            7: [4, 6, 8],
            8: [7, 12],
            9: [0, 10, 21],
            10: [3, 18, 9, 11],
            11: [6, 10, 15],
            12: [8, 13, 17],
            13: [5, 12, 14, 20],
            14: [2, 13, 23],
            15: [11, 16],
            16: [15, 17, 19],
            17: [12, 16],
            18: [10, 19],
            19: [16, 18, 20, 22],
            20: [13, 19],
            21: [9, 22],
            22: [19, 21, 23],
            23: [14, 22]
        }

        # all possible mill combinations (a mill = 3 consecutive pieces on a row or in a line)
        self.mills = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [15, 16, 17],
            [18, 19, 20], [21, 22, 23], [0, 9, 21], [3, 10, 18],
            [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17],
            [5, 13, 20], [2, 14, 23], [9, 10, 11], [12, 13, 14]
        ]

    def is_position_empty(self, pos:int):
        return self._positions[pos] == " "

    def place_piece(self, pos:int, symbol: str):
        self._positions[pos] = symbol

    def remove_piece(self, pos:int):
        self._positions[pos] = " "

    def check_mill(self, pos:int, symbol:str):
        """
        Checks if placing or moving a piece at the given position
        forms a mill for the specified symbol.

        Returns True if a mill is formed.
        """
        for mill in self.mills:
            if pos in mill:
                if all(self._positions[p] == symbol for p in mill):
                    return True
        return False

    def get_adjacent_positions(self, pos:int):
        """
        Returns a list of positions adjacent to the given position.
        """
        return self._adjacency.get(pos, [])

    def get_board(self):
        """
        Returns the positions of the board, as a list.
        """
        return  self._positions

    def is_valid_position(self, pos:int):
        return 0 <= pos < 24

    def get_symbol(self, pos:int):
        """
        Returns the symbol stored at the given position.
        """
        return self._positions[pos]

    def part_of_mill(self, pos: int, symbol: str):
        """
        Checks whether the piece at the given position
        is part of a mill for the specified symbol.
        """
        for mill in self.mills:
            if pos in mill:
                if all(self._positions[p] == symbol for p in mill):
                    return True
        return False

    #You cannot remove an opponent’s mill piece unless all opponent pieces are in mills
    def opponent_has_non_mill_pieces(self, symbol: str):
        """
        Checks whether the opponent has at least one piece
        that is not part of a mill.

        Returns True if such a piece exists.
        """
        for i in range(24):
            if self._positions[i] == symbol:
                if not self.part_of_mill(i, symbol):
                    return True
        return False
