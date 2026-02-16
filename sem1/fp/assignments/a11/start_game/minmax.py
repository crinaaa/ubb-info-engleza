from typing import Tuple, List

class MinimaxAI:
    """
    AI player of the game.
    Attributes:
        board: The game board object.
        symbol: The AI's symbol.
        opponent_symbol: The opponent's symbol.
        max_depth: How many moves ahead the AI looks.
    """

    def __init__(self, board, symbol, opponent_symbol, max_depth=4):
        self.board = board
        self.symbol = symbol
        self.opponent_symbol = opponent_symbol
        self.max_depth = max_depth

    def evaluate_board(self) -> int:
        """
        Evaluates the board for the AI.
        Returns:
            Positive score: good for AI
            Negative score: good for opponent
        """
        ai_count = sum(1 for i in range(24) if self.board.get_symbol(i) == self.symbol)
        opp_count = sum(1 for i in range(24) if self.board.get_symbol(i) == self.opponent_symbol)

        # Only consider game over if it has at least one piece on board
        if opp_count > 0 and ai_count == 0:
            return -10000
        if ai_count > 0 and opp_count == 0:
            return 10000

        # number of moves available
        ai_moves = self.count_mobility(self.symbol)
        opp_moves = self.count_mobility(self.opponent_symbol)
        if opp_count > 0 and opp_moves == 0:
            return 9000
        if ai_count > 0 and ai_moves == 0:
            return -9000

        # Base score = piece count + mobility
        score = (ai_count - opp_count) * 100
        score += (ai_moves - opp_moves) * 10

        # Mill evaluation (for the computer and the human player)
        for mill in self.board.mills:
            symbols = [self.board.get_symbol(p) for p in mill]
            if symbols.count(self.symbol) == 3:
                score += 50
            elif symbols.count(self.opponent_symbol) == 3:
                score -= 50
            elif symbols.count(self.symbol) == 2 and symbols.count(" ") == 1:
                score += 15
            elif symbols.count(self.opponent_symbol) == 2 and symbols.count(" ") == 1:
                score -= 20

        return score


    def count_mobility(self, symbol):
        """
        Counts how many moves a player can make.
        If it has only 3 pieces, flying is allowed, otherwise it moves to adjacent positions.
        """
        count = 0
        flying = sum(1 for i in range(24) if self.board.get_symbol(i) == symbol) == 3
        for i in range(24):
            if self.board.get_symbol(i) == symbol:
                targets = range(24) if flying else self.board.get_adjacent_positions(i)
                for t in targets:
                    if self.board.is_position_empty(t):
                        count += 1
        return count


    def choose_best_move(self, phase: int, can_fly: bool) -> Tuple[int, int]:
        """
        Chooses the best move using Minimax.
        Arguments:
            phase: Current game phase (1=placing, 2=moving, 3=flying)
            can_fly: True if AI can fly (phase 3).
        Returns:
            Best move: (to_pos,) for placement or (from_pos, to_pos) for moving.
            (the computer's goal is to MAXIMIZE the score)
        """
        best_score = float("-inf")
        best_move = None

        for move in self.generate_all_moves(self.symbol, phase, can_fly):
            # make the move
            removed_piece = self.simulate_move(move, self.symbol)

            # recursively evaluate the move
            score = self.minimax(self.max_depth - 1, False, phase)

            # undo the move
            self.undo_simulated_move(move, self.symbol, removed_piece)

            # keep the best scoring move
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def minimax(self, depth: int, is_maximizing: bool, phase: int) -> int:
        """
        Recursive Minimax evaluation.
        Arguments:
            depth: Remaining depth to search.
            is_maximizing: True if AI is to move, False if opponent.
            phase: Current game phase.
        Returns:
            Numerical evaluation of the board.
        """
        # Base case: if the game is over, or we reached the depth limit, we stop
        if depth == 0 or self.is_game_over():
            return self.evaluate_board()

        if is_maximizing:   #the AI's turn  (we need a maximal score)
            max_eval = float("-inf")
            for move in self.generate_all_moves(self.symbol, phase, self.symbol_can_fly()):
                removed_piece = self.simulate_move(move, self.symbol)
                evall = self.minimax(depth - 1, False, phase)
                self.undo_simulated_move(move, self.symbol, removed_piece)
                max_eval = max(max_eval, evall)
            return max_eval
        else:
            min_eval = float("inf")
            for move in self.generate_all_moves(self.opponent_symbol, phase, self.opponent_can_fly()):
                removed_piece = self.simulate_move(move, self.opponent_symbol)
                evall = self.minimax(depth - 1, True, phase)
                self.undo_simulated_move(move, self.opponent_symbol, removed_piece)
                min_eval = min(min_eval, evall)
            return min_eval


    #helper functions that simulate the possible actions

    def simulate_move(self, move, symbol):
        """
        Makes a move on the board for simulation purposes.
        Args:
            move: (to_pos,) for placement or (from_pos, to_pos) for moving.
            symbol: The player making the move.
        Returns:
            removed_piece: Position of any opponent piece removed (or None)
        """
        removed_piece = None
        if len(move) == 1:  # placement
            to_pos = move[0]
            self.board.place_piece(to_pos, symbol)
            if self.board.check_mill(to_pos, symbol):
                removed_piece = self.remove_simulated_opponent_piece(symbol)
        else:  # if we have 2 positions(source and destination) => moving/flying
            from_pos, to_pos = move
            self.board.remove_piece(from_pos)
            self.board.place_piece(to_pos, symbol)
            if self.board.check_mill(to_pos, symbol):
                removed_piece = self.remove_simulated_opponent_piece(symbol)
        return removed_piece

    def undo_simulated_move(self, move, symbol, removed_piece):
        """
        Undoes a simulated move.
        Args:
            move: The move that was simulated.
            symbol: The player who moved.
            removed_piece: The opponent piece that was removed, if any.
        """
        if len(move) == 1:   # placement phase
            to_pos = move[0]
            self.board.remove_piece(to_pos)
        else:       # 2 given positions => moving or flying phase
            from_pos, to_pos = move
            self.board.remove_piece(to_pos)
            self.board.place_piece(from_pos, symbol)
        if removed_piece is not None:
            self.board.place_piece(removed_piece, self.opponent_symbol if symbol == self.symbol else self.symbol)


    #generate moves

    def generate_all_moves(self, symbol, phase: int, can_fly: bool) -> List[Tuple[int, int]]:
        """
        Generates all possible moves for a player.
        Returns:
            List of moves:
                Phase 1: [(to_pos,)]
                Phase 2/3: [(from_pos, to_pos)]
        """
        moves = []
        if phase == 1:  # Placement phase
            for i in range(24):
                if self.board.is_position_empty(i):
                    moves.append((i,))
        else:  # Moving or flying
            positions = [i for i in range(24) if self.board.get_symbol(i) == symbol]
            for from_pos in positions:
                targets = range(24) if can_fly else self.board.get_adjacent_positions(from_pos)
                for to_pos in targets:
                    if self.board.is_position_empty(to_pos):
                        moves.append((from_pos, to_pos))
        return moves

    def remove_simulated_opponent_piece(self, symbol):
        """
        Simulates removal of an opponent piece after forming a mill.
        Returns:
            The position of the piece removed (or None)
        """
        opponent_symbol = self.opponent_symbol if symbol == self.symbol else self.symbol
        for i in range(24):
            if self.board.get_symbol(i) == opponent_symbol and not self.board.part_of_mill(i, opponent_symbol):
                self.board.remove_piece(i)
                return i
        # If all opponent pieces are in mills, remove first piece
        for i in range(24):
            if self.board.get_symbol(i) == opponent_symbol:
                self.board.remove_piece(i)
                return i
        return None



    def is_game_over(self) -> bool:
        """
        Checks if either player has less than 3 pieces.
        """
        ai_count = sum(1 for i in range(24) if self.board.get_symbol(i) == self.symbol)
        opp_count = sum(1 for i in range(24) if self.board.get_symbol(i) == self.opponent_symbol)
        return ai_count < 3 or opp_count < 3

    def symbol_can_fly(self) -> bool:
        # Count AI pieces
        count = sum(1 for i in range(24) if self.board.get_symbol(i) == self.symbol)
        return count == 3

    def opponent_can_fly(self) -> bool:
        # Count opponent pieces
        count = sum(1 for i in range(24) if self.board.get_symbol(i) == self.opponent_symbol)
        return count == 3

    def get_placement_move(self):
        """
        Returns the best position to place a piece (Phase 1).
        Returns:
            (to_pos,) tuple
        """
        # Phase 1 = placing, can_fly=False
        best_move = self.choose_best_move(phase=1, can_fly=False)
        return (best_move[0],)

    def get_move(self, can_fly: bool):
        """
        Returns the best move (from_pos, to_pos) using Minimax.
        Args:
            can_fly: True if AI has 3 pieces and can move anywhere.
        """
        best_move = self.choose_best_move(phase=2, can_fly=can_fly)
        return best_move  # already (from_pos, to_pos)

    def get_removal_move(self) -> int:
        """
        Returns the best opponent piece to remove.
        Tries to remove a piece not in a mill first.
        """
        for i in range(24):
            if self.board.get_symbol(i) == self.opponent_symbol:
                if not self.board.part_of_mill(i, self.opponent_symbol):
                    return i
        # If all opponent pieces are in mills, remove first piece
        for i in range(24):
            if self.board.get_symbol(i) == self.opponent_symbol:
                return i
        return -1  # fallback
