# binary_repo.py - FIXED
import pickle
from src.repository.grade_repo.memory_repo import GradeMemoryRepo
from src.domain.grade import Grade, generate_grades
from src.exceptions import RepositoryException


class GradeBinaryRepo(GradeMemoryRepo):
    def __init__(self, filename="grades.bin", student_repo=None, assignment_repo=None, prepopulate=False):
        super().__init__(student_repo, assignment_repo, prepopulate=False)
        self._filename = filename
        self._load_file()

        # prepopulate only if empty
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
            with open(self._filename, "rb") as fin:   #open to read from the file
                loaded_data = pickle.load(fin)
                self._grades.clear()
                self._grades.update(loaded_data)

        except (FileNotFoundError, EOFError):
            # if the file doesn't exist or is empty, we create it with empty data
            with open(self._filename, "wb") as f:
                pickle.dump({}, f)   #empty data
        except Exception:    #handle other exceptions
            raise RepositoryException(f"Error loading file {self._filename}")


    def _save_file(self) -> None:
        try:
            with open(self._filename, "wb") as fout:   #open the file to write in it
                pickle.dump(self._grades, fout)
        except Exception:   #we handle other exceptions
            raise RepositoryException(f"Error saving to file {self._filename}")


    #override from parent class in order to save to file
    def add_auto(self, grade: Grade) -> None:
        super().add_auto(grade)
        self._save_file()

    # def update_grade(self, assignment_id: int, student_id: int, grade_value: int) -> None:
    #     super().update_grade(assignment_id, student_id, grade_value)
    #     self._save_file()

    def set_grade(self, assignment_id: int, student_id: int, grade_value: int) -> None:
        super().set_grade(assignment_id, student_id, grade_value)
        self._save_file()

    def remove_by_student(self, student_id: int) -> None:
        super().remove_by_student(student_id)
        self._save_file()

    def remove_by_assignment(self, assignment_id: int) -> None:
        super().remove_by_assignment(assignment_id)
        self._save_file()

    def remove_by_student_assignment(self, assignment_id: int, student_id: int) -> None:
        super().remove_by_student_assignment(assignment_id, student_id)
        self._save_file()



