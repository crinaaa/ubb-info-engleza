import pickle
from src.domain.assignment import Assignment, generate_assignments
from src.repository.assignment_repo.memory_repo import AssignmentMemoryRepo
from src.exceptions import RepositoryException


class AssignmentBinaryRepo(AssignmentMemoryRepo):
    def __init__(self, filename="assignments.bin", prepopulate=False):
        super().__init__(prepopulate=False)
        self._filename = filename
        self._load_file()

        if prepopulate and len(self.get_all()) == 0:
            for a in generate_assignments(20):
                try:
                    super().add(a)
                except RepositoryException:   #skip duplicates
                    pass
            self._save_file()

    def _load_file(self) -> None:
        """
        Loads assignment data from the binary file into memory using pickle.
        :raises RepositoryException: if there's an error reading, deserializing,
                                     or accessing the file
        :return: None
        """
        try:
            with open(self._filename, "rb") as fin:   #open the file to read
                loaded_data = pickle.load(fin)

                # clear parent's data and load from file
                self._assignments.clear()
                self._assignments.update(loaded_data)

        except (FileNotFoundError, EOFError):
            # if the file doesn't exist or is empty, we create it with empty data
            with open(self._filename, "wb") as f:
                pickle.dump({}, f)
        except Exception:   #handle other errors
            raise RepositoryException(f"Error loading file {self._filename}")

    def _save_file(self) -> None:
        """
        Saves all assignment data from memory to the binary file using pickle.
        :raises RepositoryException: If there's an error writing or serializing to the file
        :return: None
        """
        try:
            with open(self._filename, "wb") as fout:   #open the file to write in it
                pickle.dump(self._assignments, fout)
        except Exception:   #handle other exceptions
            raise RepositoryException(f"Error saving to file {self._filename}")


    #overrides functions from the memory repo in order to save to file
    def add(self, new_assignment: Assignment) -> None:
        """
        Adds a new assignment to the repository and saves to binary file.
        :param new_assignment: The Assignment object to add to the repository
        :raises RepositoryException: if an assignment with the same ID already exists,
                                     or if there's an error saving to file
        :return: None
        """
        super().add(new_assignment)
        self._save_file()

    def remove(self, assignment_id: int) -> None:
        """
        Removes an assignment from the repository by ID and saves to binary file.
        :param assignment_id: The ID of the assignment to remove
        :raises RepositoryException: if an assignment with the given ID does not exist,
                                     or if there's an error saving to file
        :return: None
        """
        super().remove(assignment_id)
        self._save_file()

    def update(self, assignment: Assignment) -> None:
        """
        Updates an existing assignment in the repository and saves to binary file.
        :param assignment: the updated Assignment object
        :raises RepositoryException: if an assignment with the given ID does not exist,
                                     or if there's an error saving to file
        :return: None
        """
        super().update(assignment)
        self._save_file()