# text_repo.py - FIXED
from src.repository.grade_repo.memory_repo import GradeMemoryRepo
from src.domain.grade import Grade, generate_grades
from src.exceptions import RepositoryException


class GradeTextRepo(GradeMemoryRepo):
    def __init__(self, filename="grades.txt", student_repo=None, assignment_repo=None, prepopulate=False):
        super().__init__(student_repo, assignment_repo, prepopulate=False)
        self._filename = filename
        self._load_file()

        # prepopulate only if file empty
        if prepopulate and len(self.get_all()) == 0 and student_repo and assignment_repo:
            grades = generate_grades(list(student_repo.get_all()), list(assignment_repo.get_all()))
            for g in grades:
                try:
                    super().add_auto(g)
                except RepositoryException:
                    pass  # skip duplicates
            self._save_file()

    def _load_file(self) -> None:
        try:
            with open(self._filename, "r") as fin:   #open the file for reading
                for line in fin:
                    if not line.strip():
                        continue
                    parts = line.strip().split(",")
                    if len(parts) != 3:
                        continue  # skip bad format lines

                    assignment_id = int(parts[0])
                    student_id = int(parts[1])
                    grade_value = None if parts[2] == "None" else int(parts[2])
                    grade = Grade(assignment_id, student_id, grade_value)
                    super().add_auto(grade)

        except FileNotFoundError:
            #if we do not have the file, we create it
            with open(self._filename, "w") as f:
                pass
        except Exception:   #handle other possible exceptions
            raise RepositoryException(f"Error loading file {self._filename}")


    def _save_file(self) -> None:
        try:
            with open(self._filename, "w") as fout:   #open the file for reading
                for g in self.get_all():
                    value_str = "None" if g.grade is None else str(g.grade)
                    fout.write(f"{g.assignment_id},{g.student_id},{value_str}\n")
        except Exception:
            raise RepositoryException(f"Error saving to file {self._filename}")

    # override functions from the memory repo in order to save them to file
    def add_auto(self, grade: Grade) -> None:
        super().add_auto(grade)
        self._save_file()

    def update_grade(self, assignment_id: int, student_id: int, grade_value: int) -> None:
        super().update_grade(assignment_id, student_id, grade_value)
        self._save_file()

    def remove_by_student(self, student_id: int) -> None:
        super().remove_by_student(student_id)
        self._save_file()

    def remove_by_assignment(self, assignment_id: int) -> None:
        super().remove_by_assignment(assignment_id)
        self._save_file()