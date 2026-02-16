from src.settings import Settings
from src.repository.student_repo.memory_repo import StudentMemoryRepo
from src.repository.student_repo.text_repo import StudentTextRepo
from src.repository.student_repo.binary_repo import StudentBinaryRepo
from src.repository.assignment_repo.memory_repo import AssignmentMemoryRepo
from src.repository.assignment_repo.text_repo import AssignmentTextRepo
from src.repository.assignment_repo.binary_repo import AssignmentBinaryRepo
from src.repository.grade_repo.memory_repo import GradeMemoryRepo
from src.repository.grade_repo.text_repo import GradeTextRepo
from src.repository.grade_repo.binary_repo import GradeBinaryRepo


class RepositoryFactory:
    def __init__(self, settings: Settings):
        self._settings = settings

    def create_student_repository(self):
        repo_type = self._settings.get_repository_type()
        filename = self._settings.get_student_file()

        if repo_type == 'textfiles':
            return StudentTextRepo(filename, prepopulate=True)
        elif repo_type == 'binaryfiles':
            return StudentBinaryRepo(filename, prepopulate=True)
        else:
            return StudentMemoryRepo(prepopulate=True)

    def create_assignment_repository(self):
        repo_type = self._settings.get_repository_type()
        filename = self._settings.get_assignment_file()

        if repo_type == 'textfiles':
            return AssignmentTextRepo(filename, prepopulate=True)
        elif repo_type == 'binaryfiles':
            return AssignmentBinaryRepo(filename, prepopulate=True)
        else:
            return AssignmentMemoryRepo(prepopulate=True)

    def create_grade_repository(self, student_repo, assignment_repo):
        repo_type = self._settings.get_repository_type()
        filename = self._settings.get_grade_file()

        if repo_type == 'textfiles':
            return GradeTextRepo(filename, student_repo, assignment_repo, prepopulate=True)
        elif repo_type == 'binaryfiles':
            return GradeBinaryRepo(filename, student_repo, assignment_repo, prepopulate=True)
        else:
            return GradeMemoryRepo(student_repo, assignment_repo, prepopulate=True)