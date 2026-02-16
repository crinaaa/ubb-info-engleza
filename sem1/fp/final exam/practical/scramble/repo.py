from domain import Sentence


class TextFileRepo:
    def __init__(self, filename:str):
        self._filename = filename
        self._sentences = []
        self._load_file()

    def _load_file(self):
        with open(self._filename, "r") as fin:
            for line in fin:
                sent = Sentence(line)
                self._sentences.append(sent)

    def get_all(self):
        return self._sentences