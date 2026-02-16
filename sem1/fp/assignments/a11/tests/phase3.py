import unittest
from domain.player import Player
from domain.board import Board
from service.game_service import GameService
from exceptions.exception_module import RemovalException, GameException, InvalidMoveException

class TestPhase3Flying(unittest.TestCase):

    def setUp(self):
        self.p1 = Player("Alice", "X")
        self.p2 = Player("Bot", "0")

        self.board = Board()

        self.game = GameService(self.p1, self.p2, self.board)

        # Force Phase 3 (flying)
        self.game._phase = 3
        self.game._mill_formed = False

    def test_flying_move_anywhere(self):
        self.p1._pieces_on_board = 3
        self.board.place_piece(0, "X")
        self.board.place_piece(14, " ")  # destination

        self.game.move_piece(0, 14)

        self.assertEqual(self.board.get_symbol(0), " ")
        self.assertEqual(self.board.get_symbol(14), "X")


    def test_non_flying_cannot_move_far(self):
        self.p1._pieces_on_board = 4  # Not flying
        self.board.place_piece(0, "X")
        self.board.place_piece(14, " ")

        with self.assertRaises(InvalidMoveException):
            self.game.move_piece(0, 14)

    def test_cannot_move_opponent_piece(self):
        self.p1._pieces_on_board = 3
        self.board.place_piece(9, "0")
        self.board.place_piece(5, " ")

        with self.assertRaises(GameException):
            self.game.move_piece(9, 5)

    def test_cannot_move_to_occupied(self):
        self.p1._pieces_on_board = 3
        self.board.place_piece(0, "X")
        self.board.place_piece(5, "0")  # occupied

        with self.assertRaises(GameException):
            self.game.move_piece(0, 5)

    def test_mill_formation_while_flying(self):
        self.p1._pieces_on_board = 3
        # Setup positions to form mill at [0,1,2]
        self.board.place_piece(0, "X")
        self.board.place_piece(1, "X")
        self.board.place_piece(14, "X")  # piece to move
        self.board.place_piece(2, " ")   # destination

        with self.assertRaises(RemovalException):
            self.game.move_piece(14, 2)

        self.assertTrue(self.game._mill_formed)
