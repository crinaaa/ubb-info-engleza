class Player:
    def __init__(self, name:str, symbol:str):
        """
        Initializes a player with a name and a symbol.
        Each player starts with 9 pieces in hand
        and no pieces on the board.
        """
        self._name = name   # player's name
        self._symbol = symbol   # "x" for human player, "0" for the computer
        self._pieces_in_hand = 9  # pieces not yet on board
        self._pieces_on_board = 0  # pieces already placed on the board

    def has_pieces_to_place(self):
        return self._pieces_in_hand > 0

    def is_flying(self):
        return  self._pieces_on_board == 3

    def remove_piece(self):
        self._pieces_on_board -= 1

    def place_piece(self):
        """
        Places a piece from the player's hand onto the board.
        Decreases pieces in hand and increases pieces on the board.
        """
        self._pieces_on_board += 1
        self._pieces_in_hand -= 1

    def get_name(self):
        return self._name

    def get_symbol(self):
        return self._symbol

    def get_pieces_in_hand(self):
        return self._pieces_in_hand

    def get_pieces_on_board(self):
        return self._pieces_on_board