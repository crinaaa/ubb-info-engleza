class Sentence:
    def __init__(self, sentence:str):
        self._sentence = sentence

    @property
    def sentence(self):
        return self._sentence

    def __str__(self):
        return self._sentence