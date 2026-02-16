# src/service/assignment_service.py
from datetime import date
from src.domain.assignment import Assignment
from src.repository.assignment_repo.memory_repo import AssignmentMemoryRepo
from src.repository.grade_repo.memory_repo import GradeMemoryRepo
from src.exceptions import ValidationException, RepositoryException, ServiceException
from src.services.undo_service import FunctionCall, Operation
from src.domain.grade import Grade


class AssignmentService:
    def __init__(self, assignment_repo: AssignmentMemoryRepo, grade_repo: GradeMemoryRepo, undo_service=None) -> None:
        """
        Initializes the AssignmentService with assignment and grade repositories.

        :param assignment_repo: repository for managing assignment data
        :param grade_repo: repository for managing grade data
        :param undo_service: service for undo/redo operations (optional)
        """
        self._assignment_repo = assignment_repo
        self._grade_repo = grade_repo
        self._undo_service = undo_service

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
            # Validation
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")

            if not description or len(description.strip()) == 0:
                raise ValidationException("Description cannot be empty")

            # if deadline < date.today():
            #     raise ValidationException("Deadline cannot be in the past")

            # create assignment
            assignment = Assignment(assignment_id, description, deadline)

            # create undo/redo operations
            undo_call = FunctionCall(self._assignment_repo.remove, assignment_id)
            redo_call = FunctionCall(self._assignment_repo.add, assignment)
            operation = Operation(undo_call, redo_call)

            # add assignment to repository
            self._assignment_repo.add(assignment)

            # record for undo
            if self._undo_service:
                self._undo_service.record(operation)

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

            # get assignment first (for undo)
            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            #get assignment's grades before removal (for undo)
            all_grades = self._grade_repo.get_all()
            assignment_grades = [grade for grade in all_grades if grade.assignment_id == assignment_id]

            # create copies for the undo op
            grade_copies = []
            for grade in assignment_grades:
                grade_copy = Grade(grade.assignment_id, grade.student_id, grade.grade)
                grade_copies.append(grade_copy)

            # create undo/redo operations
            undo_calls = [
                    FunctionCall(self._assignment_repo.add, assignment),
                    FunctionCall(self._restore_grades, grade_copies)
                ]

            #redo: remove assignment+its grades again
            redo_calls = [
                    FunctionCall(self._assignment_repo.remove, assignment_id),
                    FunctionCall(self._grade_repo.remove_by_assignment, assignment_id)
                ]

                #create combined operation
            undo_combined = FunctionCall(self._execute_multiple, undo_calls)
            redo_combined = FunctionCall(self._execute_multiple, redo_calls)
            operation = Operation(undo_combined, redo_combined)

            # first remove all grades for this assignment
            self._grade_repo.remove_by_assignment(assignment_id)
            # then remove the assignment
            self._assignment_repo.remove(assignment_id)

            # record for undo
            if self._undo_service:
                self._undo_service.record(operation)

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error removing assignment: {e}")

    def _restore_grades(self, grades):
        for grade in grades:
            self._grade_repo.add_auto(grade)

    def _execute_multiple(self, function_calls):
        #helper method to execute multiple function calls.
        #used for complex undo/redo operations.
        for func_call in function_calls:
            func_call.call()

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
            # validation
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")

            if not description or len(description.strip()) == 0:
                raise ValidationException("Description cannot be empty")

            if len(description) > 200:
                raise ValidationException("Description too long (max 200 characters)")

            if deadline < date.today():
                raise ValidationException("Deadline cannot be in the past")

            # get old assignment data for undo op
            old_assignment = self._assignment_repo.get_by_id(assignment_id)
            if not old_assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            # create new assignment
            new_assignment = Assignment(assignment_id, description, deadline)


            undo_call = FunctionCall(self._assignment_repo.update, old_assignment)
            redo_call = FunctionCall(self._assignment_repo.update, new_assignment)
            operation = Operation(undo_call, redo_call)

            # update assignment
            self._assignment_repo.update(new_assignment)

            # record for undo
            if self._undo_service:
                self._undo_service.record(operation)

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