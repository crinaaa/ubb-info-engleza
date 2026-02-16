from random import choice, randint
from src.exceptions import ValidationException, GradeException


class Grade:
    def __init__(self, assignment_id: int, student_id: int, grade_value = None):
        if assignment_id <= 0:
            raise ValidationException("Assignment ID must be positive")
        if student_id <= 0:
            raise ValidationException("Student ID must be positive")
        if grade_value is not None and not (1 <= grade_value <= 10):
            raise ValidationException("Grade must be between 1 and 10")

        self._assignment_id = assignment_id
        self._student_id = student_id
        self._grade = grade_value

    @property
    def assignment_id(self) -> int:
        return self._assignment_id

    @property
    def student_id(self) -> int:
        return self._student_id

    @property
    def grade(self):
        return self._grade

    def set_grade(self, value: int):
        if self._grade is not None:
            raise GradeException("Grade already set and cannot be changed")

        if not (1 <= value <= 10):
            raise ValidationException("Grade must be between 1 and 10")

        self._grade = value

    def __str__(self):
        grade_str = "Ungraded" if self.grade is None else str(self.grade)
        return f"Assignment ID: {self.assignment_id}, Student ID: {self.student_id}, Grade: {grade_str}"


def generate_grades(students, assignments, n=20):
    grades = []
    used_pairs = []  # list to track used combinations

    while len(grades) < n:
        #choose a student and an assignment
        student = choice(students)
        assignment = choice(assignments)

        key = (assignment.id, student.id)

        # check if key is already used
        if key in used_pairs:
            continue  # do not add the grade

        grade_value = choice([None, randint(1, 10)])
        grades.append(Grade(assignment.id, student.id, grade_value))
        used_pairs.append(key)  # add to list

    return grades