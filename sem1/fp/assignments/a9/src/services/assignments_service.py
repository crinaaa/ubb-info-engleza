# src/service/assignment_service.py
from datetime import date
from src.domain.assignment import Assignment
from src.repository.assignment_repo.memory_repo import AssignmentMemoryRepo
from src.repository.grade_repo.memory_repo import GradeMemoryRepo
from src.exceptions import ValidationException, RepositoryException, ServiceException


class AssignmentService:
    def __init__(self, assignment_repo: AssignmentMemoryRepo, grade_repo: GradeMemoryRepo) -> None:
        """
        Initializes the AssignmentService with assignment and grade repositories.

        :param assignment_repo: repository for managing assignment data
        :param grade_repo: repository for managing grade data
        :type grade_repo: GradeMemoryRepo
        """
        self._assignment_repo = assignment_repo
        self._grade_repo = grade_repo

    def add_assignment(self, assignment_id: int, description: str, deadline: date) -> None:
        """
        Adds a new assignment.
        :param assignment_id: the id for the assignment
        :param description: the description of the assignment
        :param deadline: the deadline date for the assignment

        :raises ValidationException: if: assignment_id is not positive,
                                     description is empty or whitespace only,
                                     or deadline is in the past
        :raises RepositoryException: if an assignment with the same ID already exists
        :raises ServiceException: if an unexpected error occurs during the add operation

        :return: None
        """
        try:
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")

            if not description or len(description.strip()) == 0:
                raise ValidationException("Description cannot be empty")

            if deadline < date.today():
                raise ValidationException("Deadline cannot be in the past")

            assignment = Assignment(assignment_id, description, deadline)
            self._assignment_repo.add(assignment)

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error adding assignment: {e}")

    def remove_assignment(self, assignment_id: int) -> None:
        """
        Removes an assignment and all associated grades.
        :param assignment_id: the ID of the assignment to remove
        :raises ValidationException: if assignment_id is not positive
        :raises RepositoryException: if assignment with the given ID does not exist
        :raises ServiceException: if an unexpected error occurs during removal

        :return: None
        """
        try:
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")


            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            # first remove all grades for this assignment
            self._grade_repo.remove_by_assignment(assignment_id)
            # then remove the assignment
            self._assignment_repo.remove(assignment_id)

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error removing assignment: {e}")

    def update_assignment(self, assignment_id: int, description: str, deadline: date) -> None:
        """
        Updates an existing assignment with new description and deadline.
        :param assignment_id: the ID of the assignment to update
        :param description: the new description for the assignment
        :param deadline: the new deadline date for the assignment
        :raises ValidationException: if: assignment_id is not positive,
                                     description is empty or whitespace only,
                                     description exceeds 200 characters,
                                     or deadline is in the past
        :raises RepositoryException: if assignment with the given ID does not exist
        :raises ServiceException: if an unexpected error occurs during update

        :return: None
        """
        try:

            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")

            if not description or len(description.strip()) == 0:
                raise ValidationException("Description cannot be empty")

            if len(description) > 200:
                raise ValidationException("Description too long (max 200 characters)")

            if deadline < date.today():
                raise ValidationException("Deadline cannot be in the past")

            # check if assignment exists
            existing_assignment = self._assignment_repo.get_by_id(assignment_id)
            if not existing_assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            # update assignment
            assignment = Assignment(assignment_id, description, deadline)
            self._assignment_repo.update(assignment)

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error updating assignment: {e}")

    def list_assignments(self) -> list[Assignment]:
        """
        Lists all assignments.
        :return: List of all Assignment objects
        :rtype: list[Assignment]
        :raises ServiceException: if an error occurs while retrieving assignments
        :return: List of all assignments
        """
        try:
            return self._assignment_repo.get_all()
        except Exception as e:
            raise ServiceException(f"Error listing assignments: {e}")

    def get_assignment(self, assignment_id: int) -> Assignment:
        """
        Finds a specific assignment by its ID.
        :param assignment_id: the ID of the assignment to retrieve
        :return: The Assignment object with the specified ID
        :rtype: Assignment
        :raises ValidationException: if assignment_id is not positive
        :raises RepositoryException: if assignment with the given ID does not exist
        :raises ServiceException: if an unexpected error occurs during retrieval
        :return: The requested Assignment object
        """
        try:
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")

            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            return assignment

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(e)