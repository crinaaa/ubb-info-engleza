import unittest
from domain.player import Player
from domain.board import Board
from service.game_service import GameService
from exceptions.exception_module import RemovalException, GameException, InvalidPlacementPosition

class TestPhase1(unittest.TestCase):

    def setUp(self):
        # Players
        self.p1 = Player("Alice", "X")
        self.p2 = Player("Bot", "0")

        # Board
        self.board = Board()

        # Game Service
        self.game = GameService(self.p1, self.p2, self.board)

    def test_place_piece_success(self):
        self.game.place_piece(0)
        self.assertEqual(self.board.get_symbol(0), "X")
        self.assertEqual(self.p1.get_pieces_in_hand(), 8)
        self.assertEqual(self.p1.get_pieces_on_board(), 1)


    def test_place_piece_occupied(self):
        self.game.place_piece(0)
        with self.assertRaises(InvalidPlacementPosition):
            self.game.place_piece(0)

    def test_place_piece_invalid(self):
        with self.assertRaises(InvalidPlacementPosition):
            self.game.place_piece(24)  # out of bounds
        with self.assertRaises(InvalidPlacementPosition):
            self.game.place_piece(-1)

    def test_mill_formation_triggers_removal(self):
        # place 3 in a row for player1: positions 0,1,2
        self.game.place_piece(0)  # Alice
        self.game.place_piece(9)  # Bot
        self.game.place_piece(1)  # Alice
        self.game.place_piece(10)  # Bot

        # next move creates mill
        with self.assertRaises(RemovalException):
            self.game.place_piece(2)  # Alice forms mill

    def test_cannot_remove_mill_if_other_pieces_exist(self):
        # Alice forms a mill at [0,1,2]
        self.game.place_piece(0)  # Alice
        self.game.place_piece(9)  # Bot
        self.game.place_piece(1)  # Alice
        self.game.place_piece(10)  # Bot

        with self.assertRaises(RemovalException):
            self.game.place_piece(2)  # Alice completes mill

        # Set mill flag manually for testing removal
        self.game._mill_formed = True

        # bot pieces for removal
        self.board.place_piece(0, "0")
        self.board.place_piece(1, "0")
        self.board.place_piece(2, "0")
        self.board.place_piece(5, "0")

        # Update Bot counter to match
        self.p2._pieces_on_board = 4

        # remove a mill piece (0) while non-mill piece (5) exists → should raise GameException
        with self.assertRaises(GameException):
            self.game.remove_opponent_piece(0)

        # Remove the non-mill piece (5) → should succeed
        self.game.remove_opponent_piece(5)
        self.assertTrue(self.board.is_position_empty(5))
        self.assertEqual(self.p2.get_pieces_on_board(), 3)


    def test_phase_transition(self):
        # both players only 1 piece left
        self.p1._pieces_in_hand = 1
        self.p2._pieces_in_hand = 1

        # Place pieces
        self.game.place_piece(0)  # Alice
        self.game.place_piece(1)  # Bot

        # Check phase
        self.assertEqual(self.game._phase, 2)
