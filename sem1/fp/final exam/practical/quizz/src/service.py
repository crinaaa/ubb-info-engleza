import random

from src.domain import Question
from src.repository import TextRepo


class ServiceException(Exception):
    pass


class QuizService:
    def __init__(self, repo):
        self._repo = repo

    def generate_pseudo_questions(self):
        difficulties = ["easy", "medium", "hard"]
        topics = ["math", "history", "science", "biology", "logic", "literature"]
        words = ["happy", "exam", "mountain", "music", "concert"]
        for i in range(1, 101):
            diff = random.choice(difficulties)
            topic = random.choice(topics)
            word = random.choice(words)

            #construct the question
            text = f"What is a {diff} {topic} {word} question with ID {i}?"
            a1 = f"Option 1"
            a2 = f"Option 2"
            a3 = f"Option 3"
            correct_ans = random.randint(1, 3)

            self._repo.add_question(i, text, a1, a2, a3, correct_ans, diff)

        #save to the master
        self._repo.save_file()

    def add_question(self, q_id:int, text:str, a1:str,a2:str, a3:str, correct:int, level:str):
        self._repo.add_question(q_id, text, a1, a2, a3, correct, level)
        self._repo.save_file()

    def create_quiz(self, difficulty: str, num_questions: int, filename: str):
        """

        This method takes questions from the master question list.
        It randomly chooses half of the value of <num_questions> of difficulty <difficulty> and the
        rest are randomly chosen; their difficulty level is not important.

        It then combines all the chosen questions into one complete quiz list and then loads it in the
        file specified by the parameter <filename>.

        :param difficulty: the difficulty of the quiz (easy/medium/hard)
        :param num_questions: the number of questions in the quiz
        :param filename: the name of the file where we want to store the quiz
        :return: True if the quiz file was successfully created, False otherwise
        """

        if difficulty not in ["easy", "medium", "hard"]:
            raise ServiceException("Invalid format!")

        all_questions = self._repo.get_all()

        matching = [q for q in all_questions if q.level == difficulty] # questions with same level of difficulty
        others = [q for q in all_questions if q.level != difficulty]  # questions with different level of difficulty

        half = num_questions // 2 + (num_questions % 2)   #compute the minimum number of questions that need
                                                          #to have the given difficulty
        if len(matching) < half or len(all_questions) < num_questions:
            return False  # not enough questions to satisfy the rule about half of questions having the wanted difficulty

        quiz_list = random.sample(matching, half)    # take enough questions from the master list that have
                                                     # the given difficulty

        remaining_needed = num_questions - half     # the remaining number of questions we need

        # finally, add to the final questions list, random questions from the master list which have not been
        # added to the new question list
        quiz_list += random.sample(others + [q for q in matching if q not in quiz_list], remaining_needed)

        # the part to save to the new file
        with open(filename, "w") as f:
            for q in quiz_list:
                f.write(f"{q.id};{q.text};{q.a1};{q.a2};{q.a3};{q.correct};{q.level}\n")
        return True


    def get_quiz_questions(self, filename: str):
        # take questions from the file
        quiz_repo = TextRepo(filename)
        questions = quiz_repo.get_all()

        # start with the easy questions
        difficulty_order = {"easy": 1, "medium": 2, "hard": 3}
        questions.sort(key=lambda q: difficulty_order.get(q.level, 0))

        return questions

    def calculate_points(self, question, user_answer: int):
        difficulty_points = {"easy": 1, "medium": 2, "hard": 3}
        if user_answer == question.correct:
            return difficulty_points.get(question.level, 0)
        return 0