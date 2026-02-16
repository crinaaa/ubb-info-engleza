import os
import sys

from src.services.undo_service import UndoService

#add the adress
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.settings import Settings
from src.repository_factory import RepositoryFactory
from src.services.student_service import StudentService
from src.services.assignments_service import AssignmentService
from src.services.grade_service import GradeService
from src.ui.ui import ConsoleUI


def main():
    settings = Settings('settings.properties')

    factory = RepositoryFactory(settings)

    student_repo = factory.create_student_repository()
    assignment_repo = factory.create_assignment_repository()
    grade_repo = factory.create_grade_repository(student_repo, assignment_repo)

    undo_service = UndoService()

    student_service = StudentService(student_repo, grade_repo, undo_service)
    assignment_service = AssignmentService(assignment_repo, grade_repo, undo_service)
    grade_service = GradeService(grade_repo, student_repo, assignment_repo, student_service, assignment_service, undo_service)

    ui = ConsoleUI(student_service, assignment_service, grade_service, undo_service)
    ui.run()


if __name__ == "__main__":
    main()