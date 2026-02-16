from domain import Sentence
from exceptions import RepoException


class TextFileRepo:
    def __init__(self, filename:str):
        self._filename = filename
        self._sentences = []
        self._load_file()

    def _load_file(self):
        pos = 0
        with open(self._filename, "r") as fin:
            for line in fin:
                self._sentences.append(Sentence(line.strip()))

    def _save_file(self):
        with open(self._filename, "w") as fout:
            for s in self.get_all():
                fout.write(str(s)+"\n")

    def get_all(self):
        return self._sentences

    def add_sentence(self, new_sentence:Sentence):
        if new_sentence.sentence in self._sentences:
            raise RepoException("Duplicate sentence!")

        self._sentences.append(new_sentence)
        self._save_file()