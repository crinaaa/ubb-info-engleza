import unittest

from src.repository import TextRepo
from src.service import QuizService, ServiceException


class Testing(unittest.TestCase):
    def setUp(self):
        with open("master_test.txt", "w") as f:
            f.write("3;What is a hard history question with ID 3?;Option 1;Option 2;Option 3;2;hard\n"
                    "4;What is a easy logic question with ID 4?;Option 1;Option 2;Option 3;1;easy\n"
                    "5;What is a hard biology question with ID 5?;Option 1;Option 2;Option 3;2;hard\n"
                    "6;What is a medium literature question with ID 6?;Option 1;Option 2;Option 3;2;medium")

        self._repo = TextRepo("master_test.txt")
        self._service = QuizService(self._repo)


    def test_create_quiz_correct(self):
        ok = self._service.create_quiz("hard", 4, "test_ok.txt")
        self.assertEqual(ok, True)

    def test_create_quiz_not_enough_questions(self):
        ok = self._service.create_quiz("easy", 1000, "test_no.txt")
        self.assertEqual(ok, False)

    def test_create_quiz_invalid_input(self):
        with self.assertRaises(ServiceException):
            self._service.create_quiz("eas", 12, "testy.txt")