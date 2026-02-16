from random import randint
from src.domain.IdEntity import IdEntity
from faker import Faker
from src.exceptions import ValidationException


class Student(IdEntity):
    def __init__(self, student_id: int, name: str, group: int):
        super().__init__(student_id)

        if student_id <= 0:
            raise ValidationException("Student ID must be positive")
        if not name or len(name.strip()) == 0:
            raise ValidationException("Name cannot be empty")
        if group <= 0:
            raise ValidationException("Group must be positive")

        self._name = name
        self._group = group

    @property
    def name(self):
        return self._name

    @property
    def group(self):
        return self._group

    def __str__(self):
        return f"ID: {self.id} | Name: {self._name}, Group: {self._group}"


def generate_students(n=20):
    fake = Faker()
    students = []
    for i in range(1, n + 1):
        name = fake.name()
        group = randint(1, 5)
        students.append(Student(i, name, group))
    return students