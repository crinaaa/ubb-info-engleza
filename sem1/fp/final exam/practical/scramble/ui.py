from exceptions import ValidationException, GameException
from service import ServiceSentence


class ConsoleUI:
    def __init__(self, repo):
        self._service = ServiceSentence(repo)
        self._game_over = False

    def run(self):
        original, chosen_sentence, score = self._service.choose_sentence()
        while not self._game_over:
            print(f"{chosen_sentence}, [score is: {score}]")

            user_input = input("Enter the command: ").strip()

            if user_input == "exit":
                print("Exiting!")
                break

            if user_input == "undo":
                try:
                    chosen_sentence = self._service.undo()
                except GameException as e:
                    print(e)  # Prints "Nothing to undo!"
                continue

            try:
                if user_input.startswith("swap"):
                    parts = user_input.split(" ")
                    if len(parts) != 6:
                        print("Invalid format!")
                        continue
                    w1, p1 = int(parts[1]), int(parts[2])
                    w2, p2 = int(parts[4]), int(parts[5])

                    chosen_sentence, score = self._service.perform_swap(w1,p1,w2,p2,chosen_sentence)

                    if chosen_sentence == original:
                        print("You won!")
                        print(f"{chosen_sentence}, [score is: {score}]")
                        break

                    elif score == 0:
                        print("You lost!")

                else:
                    print("Unknown command!")
            except (ValidationException, GameException) as e:
                print(e)