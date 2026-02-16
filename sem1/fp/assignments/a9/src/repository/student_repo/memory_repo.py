from src.domain.student import Student, generate_students
from src.repository.repo_exceptions import RepositoryException


class StudentMemoryRepo:
    def __init__(self, prepopulate = True) -> None:
        """
        Initializes a StudentMemoryRepo with an optional prepopulation of students.
        :param prepopulate: if True, the repository will be prepopulated with
                            20 randomly generated students
        :type prepopulate: bool
        """
        self._students = {}
        if prepopulate:
            for s in generate_students(20):
                self.add(s)

    def add(self, new_student: Student) -> None:
        """
        Adds a new student to the repository.
        :param new_student: the Student object to add to the repository
        :raises RepositoryException: if a student with the same ID already exists
        :return: None
        """
        if new_student.id in self._students:
            raise RepositoryException(f"Student with ID {new_student.id} already exists!")
        self._students[new_student.id] = new_student

    def remove(self, student_id: int) -> None:
        """
        Removes a student from the repository by ID.
        :param student_id: the ID of the student to remove
        :raises RepositoryException: If a student with the given ID does not exist
        :return: None
        """
        if student_id not in self._students:
            raise RepositoryException(f"Student with ID {student_id} does not exist!")
        del self._students[student_id]

    def update(self, student: Student) -> None:
        """
        Updates an existing student in the repository, that is, it replaces
        the student with the matching ID with the provided student object.

        :param student: The updated Student object
        :raises RepositoryException: if a student with the given ID does not exist
        :return: None
        """
        if student.id not in self._students:
            raise RepositoryException(f"Student with ID {student.id} does not exist!")
        self._students[student.id] = student

    def get_all(self) -> list[Student]:
        """
        Returns all students in the repository.
        :return: a list containing all Student objects in the repository
        :rtype: list[Student]
        :return: list of all students
        """
        return list(self._students.values())

    def get_by_id(self, student_id: int) -> Student | None:
        """
        Finds a student by their ID.

        :param student_id: the ID of the student to retrieve
        :return: The Student object with the matching ID, or None if not found
        :rtype: Student | None
        :return: Student object if found, None otherwise
        """
        return self._students.get(student_id)