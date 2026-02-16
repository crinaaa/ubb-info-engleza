from src.domain.grade import Grade, generate_grades
from src.exceptions import RepositoryException


class GradeMemoryRepo:


    def __init__(self, student_repo=None, assignment_repo=None, prepopulate=True):
        self._grades = {}
        self._student_repo = student_repo
        self._assignment_repo = assignment_repo

        if prepopulate and student_repo and assignment_repo:
            grades = generate_grades(list(student_repo.get_all()), list(assignment_repo.get_all()), n=20)
            for g in grades:
                self.add_auto(g)

    def add_auto(self, grade: Grade) -> None:

        key = (grade.assignment_id, grade.student_id)
        #prevent duplicates when the user assigns an assignment to a student
        if key in self._grades:
            raise ValueError(f"Student {grade.student_id} already has assignment {grade.assignment_id}")

        self._grades[key] = grade

    def update_grade(self, assignment_id: int, student_id: int, grade_value: int) -> None:
        # sets grade for the first time
        key = (assignment_id, student_id)
        if key not in self._grades:
            raise ValueError("Grade does not exist")

        # cannot change existing grade
        if self._grades[key].grade is not None:
            raise ValueError(f"Grade already set for assignment {assignment_id} and student {student_id}")

        self._grades[key].set_grade(grade_value)

    def set_grade(self, assignment_id: int, student_id: int, grade_value):
        # sets grade (allows updates for undo/redo)
        key = (assignment_id, student_id)
        if key not in self._grades:
            raise ValueError(f"Grade does not exist for assignment {assignment_id} and student {student_id}")

        self._grades[key].set_grade(grade_value)

    def remove_by_student(self, student_id: int) -> None:
        # the format is "assignment id,student it,grade"
        keys = [k for k in self._grades if k[1] == student_id]
        for k in keys:
            del self._grades[k]

    def remove_by_assignment(self, assignment_id: int) -> None:
        # the format is "assignment id,student it,grade"
        keys = [k for k in self._grades if k[0] == assignment_id]
        for k in keys:
            del self._grades[k]

    def remove_by_student_assignment(self, assignment_id: int, student_id: int) -> None:
        # removes a specific grade by assignment and student ids
        # used for undo/redo operations

        key = (assignment_id, student_id)
        if key in self._grades:
            del self._grades[key]
        else:
            raise RepositoryException(f"No grade found for assignment {assignment_id} and student {student_id}")

    def get_all(self):
        return list(self._grades.values())

    def get_ungraded_by_student(self, student_id: int):
        return [g for g in self._grades.values() if g.student_id == student_id and g.grade is None]

    def grade_exists(self, assignment_id: int, student_id: int) -> bool:
        key = (assignment_id, student_id)
        return key in self._grades   #true if we've found the key, that is if there is a key
                                    # tuple with assignment id and student id

    def get_grade(self, assignment_id: int, student_id: int) -> Grade:
        key = (assignment_id, student_id)
        if key not in self._grades:
            raise ValueError(f"No grade found for assignment {assignment_id} and student {student_id}")
        return self._grades[key]