from exceptions import RepoException, ValidationException
from repo import TextFileRepo
from service import SentenceService


class ConsoleUI:
    def __init__(self, repo: TextFileRepo):
        self._service = SentenceService(repo)

    def print_menu(self):
        while True:
            print("1. Add a sentence.")
            print("2. Start the game.")
            print("0. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input!")
                continue

            if choice == 1:
                self.add_sentence_ui()

            elif choice == 2:
                self.start_game()

            elif choice == 0:
                print("Exiting!")
                break

            else:
                print("Invalid input!")


    def add_sentence_ui(self):
        try:
            sent = input("Enter the new sentence: ")
            self._service.add_sentence_service(sent)
        except (RepoException, ValidationException) as e:
            print(e)

    def start_game(self):
        text, revealed_letters = self._service.start_game()
        hangman = ""
        while True:
            display = self._service.masked_sentence(text, revealed_letters)
            print(display)
            print(hangman)

            if "_" not in display:
                print("You won!")
                break
            if hangman == "hangman":
                print("You lost!")
                break

            guess = input("Enter your guess: ")
            if guess == "x":
                print("Exiting the game!")
                break

            try:
                good, hangman = self._service.process_guess(guess,text,revealed_letters,hangman)
            except ValidationException as e:
                print(e)