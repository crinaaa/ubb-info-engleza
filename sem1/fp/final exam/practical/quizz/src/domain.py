class Question:
    def __init__(self, q_id:int, text:str, a1:str, a2:str, a3:str, correct:int, level:str):
        self._id = q_id
        self._text = text
        self._a1 = a1
        self._a2 = a2
        self._a3 = a3
        self._correct = correct
        self._level = level

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def a1(self):
        return self._a1

    @property
    def a2(self):
        return self._a2

    @property
    def a3(self):
        return self._a3

    @property
    def correct(self):
        return self._correct

    @property
    def level(self):
        return self._level