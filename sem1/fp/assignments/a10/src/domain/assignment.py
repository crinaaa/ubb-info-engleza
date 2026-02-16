from src.domain.IdEntity import IdEntity
from datetime import date, timedelta
from faker import Faker
from random import randint
from src.exceptions import ValidationException


class Assignment(IdEntity):
    def __init__(self, assignment_id: int, description: str, deadline: date):
        super().__init__(assignment_id)

        if assignment_id <= 0:
            raise ValidationException("Assignment ID must be positive")
        if not description or len(description.strip()) == 0:
            raise ValidationException("Description cannot be empty")
        if len(description) > 200:
            raise ValidationException("Description too long (max 200 characters)")
        # if deadline < date.today():
        #     raise ValidationException("Deadline cannot be in the past")

        self._description = description
        self._deadline = deadline

    @property
    def description(self):
        return self._description

    @property
    def deadline(self):
        return self._deadline

    def __str__(self):
        return f"Assignment {self.id} | {self.description} (deadline: {self.deadline})"


def generate_assignments(n=20):
    fake = Faker()
    assignments = []
    for i in range(1, n + 1):
        description = fake.sentence(nb_words=4)
        days_offset = randint(-30, 30)
        deadline = date.today() + timedelta(days=days_offset)
        assignments.append(Assignment(i, description, deadline))
    return assignments