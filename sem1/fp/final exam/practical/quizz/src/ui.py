from src.service import QuizService, ServiceException


class ConsoleUI:
    def __init__(self, repo):
        self._service = QuizService(repo)

    def print_menu(self):
        print("1. Add a question to the master list")
        print("2. Create a new quiz.")
        print("3. Take a quiz.")
        print("4. Exit.")

    def run(self):
        while True:
            self.print_menu()
            self._service.generate_pseudo_questions()
            command = input("> ")
            parts = command.split(" ")
            if parts[0] == "add":
                self.add_question_ui(parts)
            elif parts[0] == "create":
                self.create_quiz_ui(parts)
            elif parts[0] == "start":
                self.take_quiz_ui(parts)
            elif parts[0] == "exit":
                print("Exiting the program!")
                break
            else:
                print("Invalid command! Try again!")

    def add_question_ui(self, command_parts):
        try:
            raw_data = " ".join(command_parts)
            data = raw_data.split(';')

            q_id = int(data[0].split()[1])
            text = data[1]
            a1 = data[2]
            a2 = data[3]
            a3 = data[4]
            correct = int(data[5])
            level = data[6]

            self._service.add_question(q_id, text, a1, a2, a3, correct, level)
            print("Question added!.")
        except (IndexError,ValueError):
            print("Invalid command format! Try again!")

    def create_quiz_ui(self, parts):
        try:
            difficulty = parts[1]
            count = int(parts[2])
            filename = parts[3]

            success = self._service.create_quiz(difficulty, count, filename)

            if success:
                print(f"Quiz created successfully in {filename}.")
            else:
                print("You need more questions in order to satisfy the quiz rules.")
        except (IndexError, ValueError, ServiceException):
            print("Invalid format! Try again!")


    def take_quiz_ui(self, parts):
        try:
            filename = parts[1]
            questions = self._service.get_quiz_questions(filename)

            total_score = 0
            print("Start quiz!")

            for q in questions:
                print(f"\nQuestion: {q.text} (Level: {q.level})")
                print(f"1. {q.a1}")
                print(f"2. {q.a2}")
                print(f"3. {q.a3}")

                user_choice = input("Your answer (1, 2, or 3): ").strip()

                if user_choice == "exit":
                    break

                try:
                    ans_int = int(user_choice)
                    points = self._service.calculate_points(q, ans_int)

                    if points > 0:
                        print(f"Correct! You get {points} points.")
                        total_score += points
                    else:
                        print(f"Wrong. The correct answer was {q.correct}.")
                except ValueError:
                    #print("Answer not possible! We go to the next question.")\
                    print(f"Invalid answer. The correct answer was {q.correct}.")


            print(f"\nQuiz Finished! Total score: {total_score} points.")

        except FileNotFoundError:
            print(f"The file was not found.")
        except IndexError:
            print("Invalid command!")