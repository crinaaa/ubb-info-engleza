class Student:
    def __init__(self, student_id: int, name: str, attendances: int, grade: int):
        self._id = student_id
        self._name = name
        self._attendances = attendances
        self._grade = grade

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def attendances(self):
        return self._attendances

    @property
    def grade(self):
        return self._grade

    def set_grade(self, new_grade:int):
        self._grade = new_grade