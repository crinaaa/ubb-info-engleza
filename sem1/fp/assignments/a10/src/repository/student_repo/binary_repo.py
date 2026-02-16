import os
import pickle
from src.domain.student import Student, generate_students
from src.repository.student_repo.memory_repo import StudentMemoryRepo
from src.exceptions import RepositoryException


class StudentBinaryRepo(StudentMemoryRepo):
    def __init__(self, filename="students.bin", prepopulate=False):
        super().__init__(prepopulate=False)
        self._filename = filename
        self._load_file()

        if prepopulate and len(self.get_all()) == 0:
            for s in generate_students(20):
                try:
                    super().add(s)
                except RepositoryException:    #skip duplicates
                    pass
            self._save_file()

    def _load_file(self) -> None:
        """
        Loads student data from the binary file into memory using pickle.
        :raises RepositoryException: if there's an error reading, deserializing,
                                     or accessing the file
        :return: None
        """
        try:
            # check if file exists and has content
            if not os.path.exists(self._filename) or os.path.getsize(self._filename) == 0:
                # if the file doesn't exist or is empty - create with empty data
                with open(self._filename, "wb") as f:
                    pickle.dump({}, f)
                return   # no data to load because we've only created the file, it does not have data

            with open(self._filename, "rb") as fin:  # open the file for reading
                loaded_data = pickle.load(fin)
                self._students.clear()
                self._students.update(loaded_data)

        except (EOFError, pickle.UnpicklingError):
            # if the file is corrupted or empty, we recreate it
            with open(self._filename, "wb") as f:
                pickle.dump({}, f)
        except Exception as e:   #handle other exceptions
            raise RepositoryException(f"Error loading file {self._filename}: {e}")

    def _save_file(self) -> None:
        """
        Saves all student data from memory to the binary file using pickle.
        :raises RepositoryException: if there's an error writing or serializing to the file
        :return: None
        """
        try:
            with open(self._filename, "wb") as fout:
                pickle.dump(self._students, fout)
        except Exception as e:
            raise RepositoryException(f"Error saving to file {self._filename}")



    #overrides function from the memory repo
    def add(self, new_student: Student) -> None:
        """
        Adds a new student to the repository and saves to binary file.
        :param new_student: the Student object to add to the repository
        :raises RepositoryException: if a student with the same ID already exists,
                                     or if there's an error saving to file
        :return: None
        """
        super().add(new_student)
        self._save_file()

    def remove(self, student_id: int) -> None:
        """
        Removes a student from the repository by ID and saves to binary file.
        :param student_id: the ID of the student to remove
        :raises RepositoryException: if a student with the given ID does not exist,
                                     or if there's an error saving to file
        :return: None
        """
        super().remove(student_id)
        self._save_file()

    def update(self, student: Student) -> None:
        """
        Updates an existing student in the repository and saves to binary file.
        :param student: The updated Student object
        :raises RepositoryException: if a student with the given ID does not exist,
                                     or if there's an error saving to file
        :return: None
        """
        super().update(student)
        self._save_file()