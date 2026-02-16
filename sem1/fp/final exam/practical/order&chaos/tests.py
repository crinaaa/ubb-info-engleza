import unittest

from service import GameService


class Tests(unittest.TestCase):
    def setUp(self):
        self.service = GameService()

    def test_horizontal_win(self):
        for i in range(5):
            self.service._board.move(0, i, "X")
        self.assertTrue(self.service.check_win())

    def test_move(self):
        self.service.order_move(1,1,"X")
        self.assertEqual(self.service._board.get_cell(1,1),1)