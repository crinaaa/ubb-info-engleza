from src.domain.student import Student, generate_students
from src.repository.student_repo.memory_repo import StudentMemoryRepo
from src.exceptions import RepositoryException


class StudentTextRepo(StudentMemoryRepo):
    def __init__(self, filename="students.txt", prepopulate=False):
        super().__init__(prepopulate=False)
        self._filename = filename
        self._load_file()

        if prepopulate and len(self.get_all()) == 0:
            for s in generate_students(20):
                try:
                    super().add(s)
                except RepositoryException:    # avoid duplicates
                    pass
            self._save_file()

    def _load_file(self) -> None:
        """
        Loads student data from the text file into memory.
        :raises RepositoryException: If there's an error reading or parsing the file
        :return: None
        """
        try:
            with open(self._filename, "r") as fin:     #open the file for reading
                for line in fin:
                    line = line.strip()
                    if line:
                        parts = line.split(",")   # split by comma, format is "id,name,group"
                        if len(parts) != 3:
                            continue     # skip bad lines

                        student_id = int(parts[0].strip())
                        name = parts[1].strip()
                        stud_group = int(parts[2].strip())
                        student = Student(student_id, name, stud_group)
                        super().add(student)

        except FileNotFoundError:    #handle the case when we do not have the file; we create it
            with open(self._filename, "w") as f:
                pass
        except Exception as e:      #catch other possible errors
            raise RepositoryException(f"Error loading file {self._filename}")


    def _save_file(self) -> None:
        """
        Saves all student data from memory to the text file.
        :raises RepositoryException: if there's an error writing to the file
        :return: None
        """
        try:
            with open(self._filename, "w") as fout:    # open the file for writing
                for student in self.get_all():
                    fout.write(f"{student.id},{student.name},{student.group}\n")
        except Exception as e:
            raise RepositoryException(f"Error saving to file {self._filename}")

    def add(self, new_student: Student) -> None:
        """
        Adds a new student to the repository and saves to file.
        :param new_student: The Student object to add to the repository
        :raises RepositoryException: if a student with the same ID already exists,
                                     or if there's an error saving to file
        :return: None
        """
        super().add(new_student)
        self._save_file()

    def remove(self, student_id: int) -> None:
        """
        Removes a student from the repository by ID and saves to file.
        :param student_id: The ID of the student to remove
        :raises RepositoryException: if a student with the given ID does not exist,
                                     or if there's an error saving to file
        :return: None
        """
        super().remove(student_id)
        self._save_file()

    def update(self, student: Student) -> None:
        """
        Updates an existing student in the repository and persists to file.
        :param student: The updated Student object
        :raises RepositoryException: if a student with the given ID does not exist,
                                     or if there's an error saving to file

        :return: None
        """
        super().update(student)
        self._save_file()