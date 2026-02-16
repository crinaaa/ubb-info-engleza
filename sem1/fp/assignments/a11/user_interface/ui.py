from domain.board import Board
from domain.player import Player
from service.game_service import GameService
from start_game.minmax import MinimaxAI
from exceptions.exception_module import RemovalException


class ConsoleUI:
    def __init__(self, player_name: str = "Player"):
        self._player_name = player_name

        # Game components
        self._board = Board()
        self._human = Player(self._player_name, "X")
        self._computer = Player("Computer", "0")
        self._game_service = GameService(self._human, self._computer, self._board)
        self._ai = MinimaxAI(self._board, "0", "X")
        self.phase_2_announced = False  # Track phase 2 message

    def display_board(self):
        """Display the current board"""
        p = self._board.get_board()

        def symbol_or_dot(i):
            return p[i] if p[i] != " " else f"{i:d}"

        print(f"""
        {symbol_or_dot(0)}---------{symbol_or_dot(1)}---------{symbol_or_dot(2)}
        |         |         |
        |   {symbol_or_dot(3)}-----{symbol_or_dot(4)}-----{symbol_or_dot(5)}   |
        |   |     |     |   |
        |   |  {symbol_or_dot(6)}--{symbol_or_dot(7)}--{symbol_or_dot(8)}  |   |
        |   |  |     |  |   |
        {symbol_or_dot(9)}--{symbol_or_dot(10)}-{symbol_or_dot(11)}    {symbol_or_dot(12)}-{symbol_or_dot(13)}-{symbol_or_dot(14)}
        |   |  |     |  |   |
        |   | {symbol_or_dot(15)}-{symbol_or_dot(16)}-{symbol_or_dot(17)} |   |
        |   |     |     |   |
        |  {symbol_or_dot(18)}----{symbol_or_dot(19)}----{symbol_or_dot(20)}   |
        |         |         |
        {symbol_or_dot(21)}--------{symbol_or_dot(22)}--------{symbol_or_dot(23)}
        """)

    # human moves
    def _get_human_placement(self):
        while True:
            try:
                val = input("Enter position to place your piece (0-23) or 'quit': ").strip()
                if val.lower() == "quit":
                    return -1
                pos = int(val)
                if 0 <= pos <= 23:
                    if not self._board.is_position_empty(pos):
                        print("That position is already occupied.")
                        continue
                    return pos
                print("Invalid position. Must be 0-23.")
            except ValueError:
                print("Invalid input. Enter a number 0-23 or 'quit'.")

    def _get_human_movement(self):
        while True:
            try:
                from_input = input("Move FROM position (0-23) or 'quit': ").strip()
                if from_input.lower() == "quit":
                    return -1, -1
                from_pos = int(from_input)

                to_input = input("Move TO position (0-23) or 'quit': ").strip()
                if to_input.lower() == "quit":
                    return -1, -1
                to_pos = int(to_input)

                return from_pos, to_pos
            except ValueError:
                print("Invalid input. Enter numbers 0-23 or 'quit'.")

    def _get_human_removal(self):
        while True:
            try:
                val = input("Remove opponent piece (0-23) or 'quit': ").strip()
                if val.lower() == "quit":
                    return -1
                pos = int(val)
                if 0 <= pos <= 23:
                    return pos
                print("Invalid position. Must be 0-23.")
            except ValueError:
                print("Invalid input. Enter a number 0-23 or 'quit'.")


    # human player's turn
    def human_turn(self):
        state = self._game_service.get_game_state()
        is_placement = state['phase'] == 1
        success = False

        # Announce phase 2 starts
        if state['phase'] == 2 and not self.phase_2_announced:
            print("\nAll pieces placed. Movement phase begins!\n")
            self.phase_2_announced = True

        while not success:
            self.display_board()
            try:
                if is_placement:
                    pos = self._get_human_placement()
                    if pos == -1:
                        print("You quit the game.")
                        return False
                    self._game_service.place_piece(pos)
                    print(f"Placed piece at {pos}.")
                else:
                    from_pos, to_pos = self._get_human_movement()
                    if from_pos == -1 or to_pos == -1:
                        print("You quit the game.")
                        return False

                    symbol_at_from = self._board.get_symbol(from_pos)
                    if symbol_at_from != "X":
                        print("You must move one of your own pieces.")
                        continue
                    if not self._piece_has_legal_moves(from_pos):
                        print("That piece has no legal moves.")
                        continue
                    if not self._board.is_position_empty(to_pos):
                        print("Destination must be empty.")
                        continue

                    self._game_service.move_piece(from_pos, to_pos)
                    print(f"Moved piece from {from_pos} to {to_pos}.")

                # Handle mill if formed
                state = self._game_service.get_game_state()
                if state['mill_formed']:
                    while True:
                        remove_pos = self._get_human_removal()
                        if remove_pos == -1:
                            return False
                        try:
                            self._game_service.remove_opponent_piece(remove_pos)
                            print(f"Removed opponent piece at {remove_pos}.")
                            break
                        except Exception as e:
                            print(e)

                success = True
            except RemovalException:
                while True:
                    remove_pos = self._get_human_removal()
                    if remove_pos == -1:
                        return False
                    try:
                        self._game_service.remove_opponent_piece(remove_pos)
                        print(f"Removed opponent piece at {remove_pos}.")
                        break
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(f"Error: {e}")
        return True

    # check if piece can move
    def _piece_has_legal_moves(self, pos: int) -> bool:
        """
        Returns True if the selected human piece can move somewhere.
        Handles both movement and flying.
        """
        human_pieces = [i for i in range(24) if self._board.get_symbol(i) == "X"]
        can_fly = len(human_pieces) == 3

        if can_fly:
            return any(self._board.is_position_empty(i) for i in range(24))

        for adj in self._board.get_adjacent_positions(pos):
            if self._board.is_position_empty(adj):
                return True
        return False

    # handle the computer turn
    def computer_turn(self):
        state = self._game_service.get_game_state()
        is_placement = state['phase'] == 1
        try:
            if is_placement:
                pos = self._ai.get_placement_move()[0]
                self._game_service.place_piece(pos)
                print(f"Computer placed at position {pos}.")
            else:
                can_fly = self._computer.is_flying()
                from_pos, to_pos = self._ai.get_move(can_fly)
                self._game_service.move_piece(from_pos, to_pos)
                print(f"Computer moved from {from_pos} to {to_pos}.")

            # Now check if mill was formed
            state = self._game_service.get_game_state()
            if state['mill_formed']:
                remove_pos = self._ai.get_removal_move()
                self._game_service.remove_opponent_piece(remove_pos)
                print(f"Computer removed your piece at {remove_pos} due to forming a mill.")

        except RemovalException:
            # if game_service raises RemovalException directly
            remove_pos = self._ai.get_removal_move()
            self._game_service.remove_opponent_piece(remove_pos)
            print(f"Computer removed your piece at {remove_pos} due to forming a mill.")

        except Exception as e:
            print(f"Computer error: {e}")

    # check if the game is over
    def show_game_over(self):
        state = self._game_service.get_game_state()
        self.display_board()
        print("\nGAME OVER")
        winner = state['winner']
        if winner == self._human:
            print(f"{self._player_name} wins!")
        elif winner == self._computer:
            print("Computer wins!")
        else:
            print("Draw!")

    # main loop, that handles the game
    def run(self):
        print(f"Starting Nine Men's Morris: {self._player_name} (X) vs Computer (O)")
        while True:
            state = self._game_service.get_game_state()

            # check for game over
            if state['game_over']:
                self.show_game_over()
                break

            # determine whose turn it is
            if state['current_player'] == self._human:
                cont = self.human_turn()
                if not cont:
                    break
            else:
                self.computer_turn()

        print("Thanks for playing!")
