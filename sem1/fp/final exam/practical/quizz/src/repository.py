from src.domain import Question


class TextRepo:
    def __init__(self, filename:str):
        self._filename = filename
        self._questions = {}
        self._load_file()


    def _load_file(self):
        with open(self._filename, "r") as fin:
            for line in fin:
                parts = line.strip().split(";")
                q_id = int(parts[0])
                text = parts[1]
                a1 = parts[2]
                a2 = parts[3]
                a3 = parts[4]
                correct = int(parts[5])
                level = parts[6]

                self._questions[q_id] = Question(q_id, text, a1, a2, a3, correct, level)

    def save_file(self):
        self._save_file()
    #for master list
    def _save_file(self):
        with open(self._filename, "w") as fout:
            for q in self.get_all():
                fout.write(f"{q.id};{q.text};{q.a1};{q.a2};{q.a3};{q.correct};{q.level}\n")


    def get_all(self):
        return list(self._questions.values())

    # adds the question (to the MASTER list!)
    def add_question(self, q_id, text, a1, a2, a3, correct, level):
        new_q = Question(q_id, text, a1, a2, a3, correct, level)
        self._questions[q_id] = new_q