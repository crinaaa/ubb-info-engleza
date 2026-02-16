from src.domain.grade import Grade
from src.exceptions import ValidationException, RepositoryException, ServiceException
from src.domain.student import Student
from src.services.undo_service import FunctionCall, Operation


class StudentService:
    def __init__(self, student_repo, grade_repo, undo_service):
        """
        Initializes the StudentService with repositories.
        :param student_repo: repository for student data operations
        :param grade_repo: repository for grade data operations
        :param undo_service: service for undo/redo operations
        """
        self._student_repo = student_repo
        self._grade_repo = grade_repo
        self._undo_service = undo_service


    def add_student(self, student_id: int, name: str, group: int):
        """
        Adds a new student to the system.
        :param student_id: the id for the student (must be positive)
        :param name: the name of the student (cannot be empty)
        :param group: the group number of the student (must be positive)
        :raises ValidationException: If:
            - student_id <= 0
            - name is empty or whitespace only
            - group <= 0
        :raises RepositoryException: if a student with the same ID already exists
        :raises ServiceException: if any other error occurs during the operation
        """
        try:
            # input validation
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            if not name or len(name.strip()) == 0:
                raise ValidationException("Name cannot be empty")

            if group <= 0:
                raise ValidationException("Group must be positive")

            if self._student_repo.get_by_id(student_id):
                raise RepositoryException(f"Student with ID {student_id} already exists")

            # create student
            student = Student(student_id, name, group)

            # create undo/redo operations
            undo_call = FunctionCall(self._student_repo.remove, student_id)
            redo_call = FunctionCall(self._student_repo.add, student)
            operation = Operation(undo_call, redo_call)

            # perform the operation
            self._student_repo.add(student)

            # record for undo
            self._undo_service.record(operation)

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception:
            raise ServiceException("Error adding student")

    def remove_student(self, student_id: int):
        """
        Removes a student and all their grades from the system.
        :param student_id: the ID of the student to remove (must be positive)
        :raises ValidationException: if student_id <= 0
        :raises RepositoryException: if student with given ID does not exist
        :raises ServiceException: if any other error occurs during the operation
        """
        try:
            # get student first (for undo)
            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            # get student's grades before removal (for undo)
            all_grades = self._grade_repo.get_all()
            student_grades = [grade for grade in all_grades if grade.student_id == student_id]

            # create copies of the grades of a certain student
            # we need them for undo/redo
            grade_copies = []
            for grade in student_grades:
                # create a copy of the grade object
                grade_copy = Grade(grade.assignment_id, grade.student_id, grade.grade)
                grade_copies.append(grade_copy)

            # create undo/redo operations
            # we need to handle two repos: student_repo+grade_repo

            # undo operations: restore student+their grades
            undo_calls = [
                FunctionCall(self._student_repo.add, student),
                FunctionCall(self._restore_grades, grade_copies)
            ]

            # redo operations: remove student+their grades
            redo_calls = [
                FunctionCall(self._student_repo.remove, student_id),
                FunctionCall(self._grade_repo.remove_by_student, student_id)
            ]

            # create combined operation using helper function
            undo_combined = FunctionCall(self._execute_multiple, undo_calls)
            redo_combined = FunctionCall(self._execute_multiple, redo_calls)
            operation = Operation(undo_combined, redo_combined)

            #make the removal
            self._grade_repo.remove_by_student(student_id)
            self._student_repo.remove(student_id)

            # record for undo
            self._undo_service.record(operation)

        except RepositoryException as re:
            raise re
        except Exception as e:
            raise ServiceException(f"Error removing student: {e}")

    def _restore_grades(self, grades):
        #helper function to restore grades for undo
        for grade in grades:
            self._grade_repo.add_auto(grade)

    def _execute_multiple(self, function_calls):
        #execute multiple function calls.
        #complex undo/redo operations
        for func_call in function_calls:
            func_call.call()

    def update_student(self, student_id: int, name: str, group: int):
        """
        Updates an existing student's information.
        :param student_id: the ID of the student to update (must be positive)
        :param name: the new name for the student (cannot be empty)
        :param group: the new group number for the student (must be positive)
        :raises ValidationException: If:
            - student_id <= 0
            - name is empty or whitespace only
            - group <= 0
        :raises RepositoryException: if student with given ID does not exist
        :raises ServiceException: if any other error occurs during the operation
        """
        try:
            # validation
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            if not name or len(name.strip()) == 0:
                raise ValidationException("Name cannot be empty")

            if group <= 0:
                raise ValidationException("Group must be positive")

            # get old student data for undo
            old_student = self._student_repo.get_by_id(student_id)
            if not old_student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            # create new student
            new_student = Student(student_id, name, group)

            # create undo/redo operations
            undo_call = FunctionCall(self._student_repo.update, old_student)
            redo_call = FunctionCall(self._student_repo.update, new_student)
            operation = Operation(undo_call, redo_call)

            # make the update
            self._student_repo.update(new_student)

            # record for undo
            self._undo_service.record(operation)

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception:
            raise ServiceException("Error updating student")


    def list_students(self):
        """
        List all students.
        :return: list of all Student objects
        :raises ServiceException: if any error occurs during the operation
        """
        try:
            return self._student_repo.get_all()
        except Exception:
            raise ServiceException("Error listing students")

    def get_student(self, student_id: int):
        """
        Finds a specific student by ID.
        :param student_id: the ID of the student to retrieve (must be positive)
        :return: the Student object with the given ID
        :raises ValidationException: if student_id <= 0
        :raises RepositoryException: if student with given ID does not exist
        :raises ServiceException: if any other error occurs during the operation
        """
        try:
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")
            return student

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error getting student: {e}")

    def get_students_by_group(self, group: int):
        """
        Finds all students belonging to a specific group.
        :param group: the group number to filter by (must be positive)
        :return: list of Student objects in the specified group
        :raises ValidationException: if group <= 0
        :raises ServiceException: if any other error occurs during the operation
        """
        try:
            if group <= 0:
                raise ValidationException("Group must be positive")

            all_students = self._student_repo.get_all()
            return [student for student in all_students if student.group == group]

        except ValidationException as ve:
            raise ve
        except Exception as e:
            raise ServiceException(f"Error getting students by group: {e}")

    def student_exists(self, student_id: int) -> bool:
        """
        Checks if a student with the given ID exists.
        :param student_id: the ID of the student to check
        :return: True if student exists, False otherwise
        :raises ServiceException: if any error occurs during the check
        """
        try:
            return self._student_repo.get_by_id(student_id) is not None
        except Exception as e:
            raise ServiceException(f"Error checking student existence: {e}")