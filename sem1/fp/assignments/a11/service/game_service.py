from domain.board import Board
from domain.player import Player
from exceptions.exception_module import RemovalException, GameException, InvalidMoveException, InvalidPlacementPosition

class GameService:
    def __init__(self, player1: Player, player2: Player, board: Board):
        """
        Initializes the game service with two players and a board.
        Sets starting phase to 1 (placement), current player to player1,
        and initializes flags for mill formation and game over.
        """
        self._board = board
        self._players = [player1, player2]
        self._current_player_index = 0  # keep track of whose turn it is
        self._phase = 1  # 1 = placing, 2 = moving, 3 = flying
        self._mill_formed = False
        self._game_over = False
        self._winner = None

    def current_player(self):
        """
        Returns the player whose turn it is currently(0 for the first player, 1 for the second player).
        """
        return self._players[self._current_player_index]
        # returns 0 for the first player, 1 for the second player

    def opponent(self):
        """
        Returns the opponent of the current player(if it's the first player's turn, it returns 1, otherwise it returns 0).
        """
        return self._players[1 - self._current_player_index]
        # if it's the first player1's turn, it returns 1, otherwise it returns 0

    def switch_turn(self):
        self._current_player_index = 1 - self._current_player_index

    def get_game_state(self):
        """
        Returns the current game state as a dictionary for UI display.
        Includes board state, current player, phase, mill formation flag,
        game over status, winner, and pieces counts for both players.
        """
        return {
            'board': self._board.get_board(),
            'current_player': self.current_player(),
            'phase': self._phase,
            'mill_formed': self._mill_formed,
            'game_over': self._game_over,
            'winner': self._winner,
            'player1_pieces_in_hand': self._players[0].get_pieces_in_hand(),
            'player1_pieces_on_board': self._players[0].get_pieces_on_board(),
            'player2_pieces_in_hand': self._players[1].get_pieces_in_hand(),
            'player2_pieces_on_board': self._players[1].get_pieces_on_board(),
        }

    def clear_mill_state(self):
        """
        Resets the mill formation flag; after a mill is formed, and the players removes one of
        the opponent's pieces, the mill flag is set to False again.
        """
        self._mill_formed = False

    def force_draw(self):
        """
        If the game cannot conclude with having a winner, we decide it is a draw.
        """
        self._game_over = True
        self._winner = None

    def is_game_over(self):
        """Check if game is over"""
        return self._game_over

    def check_game_over(self):
        """
        Checks whether the game should end and sets the winner if so.
        Ends the game if a player has less than 3 pieces on board or has no legal moves.
        Returns True if the game ends, False otherwise.
        """

        # don't check for game over during placement phase
        if self._phase == 1:
            return False

        # check if any player has less than 3 pieces (important only after placement phase)
        for i, player in enumerate(self._players):
            opponent = self._players[1 - i]
            if player.get_pieces_on_board() < 3:
                self._game_over = True
                self._winner = opponent
                return True

        # check if current player has no legal moves
        current = self.current_player()
        if not self.has_legal_moves(current):
            self._game_over = True
            self._winner = self.opponent()
            return True

        return False

    def has_legal_moves(self, player: Player):
        """Check if player has legal moves"""

        symbol = player.get_symbol()

        #if player can fly, they can move anywhere there is an empty space
        if player.is_flying():
            for i in range(24):
                if self._board.is_position_empty(i):
                    return True
            return False

        #normal move: check if player can move to adjacent empty position
        for i in range(24):
            if self._board.get_symbol(i) == symbol:
                adjacent = self._board.get_adjacent_positions(i)
                for adj_pos in adjacent:
                    if self._board.is_position_empty(adj_pos):
                        return True

        return False

    """
    !!!Rules!!!
    1.Players take turns placing their pieces on empty positions.
    2.When a player places a piece that forms a mill, they remove one opponent piece
    (cannot remove pieces in a mill unless all opponent’s pieces are in mills).
    3.After all 9 pieces are placed, the game moves to Phase 2 (moving pieces).
    """

    # Phase 1 : placing pieces

    def place_piece(self, pos: int):
        """
        Places a piece from the current player at the specified position.
        Raises:
            InvalidPlacementPosition: if the position is invalid or occupied
            GameException: if the player has no pieces to place
            RemovalException: if the placement forms a mill
        """
        player = self.current_player()
        symbol = player.get_symbol()

        # validate positions
        if not self._board.is_valid_position(pos):
            raise InvalidPlacementPosition(f"Position {pos} is invalid! Try again!")
        if not self._board.is_position_empty(pos):
            raise InvalidPlacementPosition(f"Position {pos} is occupied! Try again!")

        #check if player has pieces to place
        if player.has_pieces_to_place() == 0:
            raise GameException(f"{player.get_name()} has no pieces left to place!")

        #place piece on board
        self._board.place_piece(pos, symbol)
        player.place_piece()  #update counter for pieces on board and in hand

        #check if a mill is formed
        if self._board.check_mill(pos, symbol):
            self._mill_formed = True
            #raise exception to the UI to remove the opponent's piece
            raise RemovalException(f"{player.get_name()} formed a mill! Remove an opponent piece!")

        #check if Phase 1 ends
        if all(p.get_pieces_in_hand() == 0 for p in self._players):
            self._phase = 2    #move to phase 2

        #switch turn
        if not self._mill_formed:
            self.switch_turn()

    def remove_opponent_piece(self, pos: int):
        """
        Removes an opponent's piece from the board after forming a mill.

        Raises:
            GameException: if no mill was formed, the position is invalid,
                        or rules prevent removal
        """
        if not self._mill_formed:
            raise GameException("You can only remove an opponent piece after forming a mill!")

        opponent = self.opponent()
        opponent_symbol = opponent.get_symbol()

        # validate position
        if not self._board.is_valid_position(pos):
            raise InvalidPlacementPosition(f"Position {pos} is invalid! Try again!")

        if self._board.is_position_empty(pos):
            raise GameException(f"Position {pos} is empty! Try again!")

        if self._board.get_symbol(pos) != opponent_symbol:
            raise GameException("You can only remove opponent's pieces!")

        # Cannot remove a mill piece unless all opponent's pieces are in mills
        if self._board.part_of_mill(pos, opponent_symbol):
            if self._board.opponent_has_non_mill_pieces(opponent_symbol):
                raise GameException("Cannot remove a mill piece while your opponent has non-mill pieces!")

        # perform removal
        self._board.remove_piece(pos)
        opponent.remove_piece()

        self._mill_formed = False  # reset the flag for the mill formation

        # check if Phase 1 ends
        if all(p.get_pieces_in_hand() == 0 for p in self._players):
            self._phase = 2

        # switch turn
        self.switch_turn()


    # Phases 2&3 (includes the flying part when moving a piece on the board)

    def move_piece(self, from_pos: int, to_pos: int):
        """
        Moves a piece for the current player from one position to another.

        Raises:
            GameException: if move is invalid for current phase or player
            InvalidPlacementPosition: if positions are invalid
            InvalidMoveException: if moving to non-adjacent position (unless flying)
            RemovalException: if move forms a mill
        """
        if self._phase < 2:
            raise GameException("Cannot move pieces in Phase1! Try another move!")

        player = self.current_player()
        symbol = player.get_symbol()

        # validate positions
        if not self._board.is_valid_position(from_pos) or not self._board.is_valid_position(to_pos):
            raise InvalidPlacementPosition("Invalid board positions! Try again!")

        if self._board.get_symbol(from_pos) != symbol:
            raise GameException("You can only move your own piece!")

        if not self._board.is_position_empty(to_pos):
            raise GameException("Destination position is not empty!")

        # check adjacency unless player is flying
        if not player.is_flying():
            if to_pos not in self._board.get_adjacent_positions(from_pos):
                raise InvalidMoveException("You can only move to adjacent positions! Try again!")

        # update to flying phase if player has exactly 3 pieces on board
        if player.get_pieces_on_board() == 3:
            self._phase = 3

        # move piece
        self._board.remove_piece(from_pos)
        self._board.place_piece(to_pos, symbol)

        # check for mill formation
        if self._board.check_mill(to_pos, symbol):
            self._mill_formed = True
            raise RemovalException(f"{player.get_name()} formed a mill! Remove an opponent piece.")

        # switch turn if no mill was formed
        self.switch_turn()