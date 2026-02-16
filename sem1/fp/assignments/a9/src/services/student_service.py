from src.exceptions import ValidationException, RepositoryException, ServiceException
from src.domain.student import Student

class StudentService:
    def __init__(self, student_repo, grade_repo):
        """
        Initializes the StudentService with repositories.
        :param student_repo: repository for student data operations
        :param grade_repo: repository for grade data operations
        """
        self._student_repo = student_repo
        self._grade_repo = grade_repo

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
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            if not name or len(name.strip()) == 0:
                raise ValidationException("Name cannot be empty")

            if group <= 0:
                raise ValidationException("Group must be positive")

            if self._student_repo.get_by_id(student_id):
                raise RepositoryException(f"Student with ID {student_id} already exists")

            student = Student(student_id, name, group)
            self._student_repo.add(student)

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
            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            self._grade_repo.remove_by_student(student_id)
            self._student_repo.remove(student_id)

        except RepositoryException as re:
            raise re
        except Exception:
            raise ServiceException("Error removing student")

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
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            if not name or len(name.strip()) == 0:
                raise ValidationException("Name cannot be empty")

            if group <= 0:
                raise ValidationException("Group must be positive")

            if not self._student_repo.get_by_id(student_id):
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            student = Student(student_id, name, group)
            self._student_repo.update(student)

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