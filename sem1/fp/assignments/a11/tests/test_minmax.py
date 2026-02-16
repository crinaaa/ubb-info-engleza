import unittest
from domain.board import Board
from domain.player import Player
from start_game.minmax import MinimaxAI  # import your AI class


class TestMinimaxAI(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.ai_symbol = "x"
        self.opponent_symbol = "0"
        self.ai = MinimaxAI(self.board, self.ai_symbol, self.opponent_symbol, max_depth=2)

    def test_evaluate_empty_board(self):
        """An empty board should have score 0 (neutral)"""
        score = self.ai.evaluate_board()
        self.assertEqual(score, 0)

    def test_evaluate_ai_advantage(self):
        """If AI has more pieces than opponent, score should be positive"""
        self.board.place_piece(0, self.ai_symbol)
        self.board.place_piece(1, self.ai_symbol)
        self.board.place_piece(2, self.opponent_symbol)
        score = self.ai.evaluate_board()
        self.assertGreater(score, 0)

    def test_evaluate_opponent_advantage(self):
        """If opponent has more pieces, score should be negative"""
        self.board.place_piece(0, self.opponent_symbol)
        self.board.place_piece(1, self.opponent_symbol)
        self.board.place_piece(2, self.ai_symbol)
        score = self.ai.evaluate_board()
        self.assertLess(score, 0)

    def test_generate_moves_placement(self):
        """In placement phase, all empty positions should be moves"""
        moves = self.ai.generate_all_moves(self.ai_symbol, phase=1, can_fly=False)
        self.assertIn((0,), moves)
        self.assertIn((23,), moves)
        self.assertEqual(len(moves), 24)  # all positions empty initially

    def test_generate_moves_moving(self):
        """In moving phase, AI pieces can move to adjacent positions"""
        # Place a single AI piece
        self.board.place_piece(0, self.ai_symbol)
        moves = self.ai.generate_all_moves(self.ai_symbol, phase=2, can_fly=False)
        self.assertIn((0, 1), moves)
        self.assertIn((0, 9), moves)
        self.assertNotIn((0, 2), moves)  # not adjacent

    def test_simulate_and_undo_move(self):
        """Simulating and undoing a move should leave the board unchanged"""
        original_board = self.board.get_board().copy()
        move = (0,)  # placement
        removed_piece = self.ai.simulate_move(move, self.ai_symbol)
        self.ai.undo_simulated_move(move, self.ai_symbol, removed_piece)
        self.assertEqual(self.board.get_board(), original_board)

    def test_choose_best_move_returns_valid_move(self):
        """AI should return a valid move on empty board"""
        move = self.ai.choose_best_move(phase=1, can_fly=False)
        self.assertIn(move[0], range(24))
        self.assertTrue(self.board.is_position_empty(move[0]))

    def test_remove_simulated_opponent_piece(self):
        """Simulate a mill removal"""
        # Place opponent pieces
        self.board.place_piece(0, self.opponent_symbol)
        self.board.place_piece(1, self.opponent_symbol)
        self.board.place_piece(2, self.opponent_symbol)
        removed = self.ai.remove_simulated_opponent_piece(self.ai_symbol)
        self.assertIn(removed, [0, 1, 2])
        self.assertEqual(self.board.get_symbol(removed), " ")

    def test_is_game_over_detection(self):
        """Game is over if either player has less than 3 pieces"""
        # Place 2 AI pieces and 3 opponent pieces
        self.board.place_piece(0, self.ai_symbol)
        self.board.place_piece(1, self.ai_symbol)
        self.board.place_piece(2, self.opponent_symbol)
        self.board.place_piece(3, self.opponent_symbol)
        self.board.place_piece(4, self.opponent_symbol)
        self.assertTrue(self.ai.is_game_over())

if __name__ == "__main__":
    unittest.main()
