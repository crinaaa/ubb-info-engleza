import unittest
from domain.player import Player
from domain.board import Board
from service.game_service import GameService
from exceptions.exception_module import RemovalException, GameException, InvalidMoveException, InvalidPlacementPosition

class TestPhase2(unittest.TestCase):

    def setUp(self):
        self.p1 = Player("Alice", "X")
        self.p2 = Player("Bot", "0")

        self.board = Board()

        self.game = GameService(self.p1, self.p2, self.board)

        # Force Phase 2
        self.game._phase = 2
        self.game._mill_formed = False


    def test_legal_adjacent_move(self):
        self.board.place_piece(0, "X")
        self.board.place_piece(1, " ")  # empty destination

        self.game.move_piece(0, 1)

        self.assertEqual(self.board.get_symbol(0), " ")
        self.assertEqual(self.board.get_symbol(1), "X")

    def test_illegal_non_adjacent_move(self):
        self.board.place_piece(0, "X")
        self.board.place_piece(14, " ")  # non-adjacent

        with self.assertRaises(InvalidMoveException):
            self.game.move_piece(0, 14)


    def test_move_opponent_piece(self):
        self.board.place_piece(9, "0")
        self.board.place_piece(10, " ")

        with self.assertRaises(GameException):
            self.game.move_piece(9, 10)

    def test_move_to_occupied_position(self):
        self.board.place_piece(0, "X")
        self.board.place_piece(1, "0")  # occupied

        with self.assertRaises(GameException):
            self.game.move_piece(0, 1)


    def test_mill_formation_on_move(self):
        # Setup: Alice has X at positions 0 and 1
        self.board.place_piece(0, "X")
        self.board.place_piece(1, "X")
        # Place a movable piece at 14 (adjacent to 2)
        self.board.place_piece(14, "X")
        self.board.place_piece(2, " ")  # destination

        # Move 14 → 2 to complete mill [0,1,2]
        with self.assertRaises(RemovalException):
            self.game.move_piece(14, 2)

        self.assertTrue(self.game._mill_formed)


    def test_flying_phase_move(self):
        # Reduce Alice pieces to 3 → flying
        self.p1._pieces_on_board = 3

        self.board.place_piece(0, "X")
        self.board.place_piece(10, " ")  # non-adjacent

        self.game.move_piece(0, 10)

        self.assertEqual(self.board.get_symbol(0), " ")
        self.assertEqual(self.board.get_symbol(10), "X")
