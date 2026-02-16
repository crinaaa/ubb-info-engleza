from src.domain.assignment import Assignment, generate_assignments
from src.exceptions import RepositoryException
from src.repository.assignment_repo.memory_repo import AssignmentMemoryRepo
from datetime import datetime


class AssignmentTextRepo(AssignmentMemoryRepo):
    def __init__(self, filename="assignments.txt", prepopulate=False):
        super().__init__(prepopulate=False)
        self._filename = filename
        self._load_file()

        if prepopulate and len(self.get_all()) == 0:
            for a in generate_assignments(20):
                try:
                    super().add(a)
                except RepositoryException:    #skip duplicates
                    pass
            self._save_file()

    def _load_file(self) -> None:
        """
        Loads assignment data from the text file into memory.
        :raises RepositoryException: if there's an error reading, parsing the file,
                                     or converting date strings
        :return: None
        """
        try:
            with open(self._filename, "r") as fin:   #open the file for reading
                for line in fin:
                    line = line.strip()
                    if line:
                        parts = line.split(",")  #split by comma, format is "id,description,deadline"
                        if len(parts) != 3:
                            continue   #skip bad format lines

                        assignment_id = int(parts[0])
                        description = parts[1]
                        deadline = datetime.strptime(parts[2], "%Y-%m-%d").date()
                        assignment = Assignment(assignment_id, description, deadline)
                        super().add(assignment)

        except FileNotFoundError:
            # if we do not have the file, we create it
            with open(self._filename, "w") as f:
                pass
        except Exception as e:   #handle other errors
            raise RepositoryException(f"Error loading file {self._filename}")

    def _save_file(self) -> None:
        """
        Saves all assignment data from memory to the text file.
        :return: None
        """
        with open(self._filename, "w") as fout:   #open the file to write in it
            for assignment in self.get_all():
                deadline_str = assignment.deadline.strftime("%Y-%m-%d")
                fout.write(f"{assignment.id},{assignment.description},{deadline_str}\n")



    # overrides functions from the memory repo, in order to be able to save to the file
    def add(self, new_assignment: Assignment) -> None:
        """
        Adds a new assignment to the repository and saves to file.
        :param new_assignment: The Assignment object to add to the repository
        :raises RepositoryException: if an assignment with the same ID already exists
        :return: None
        """
        super().add(new_assignment)
        self._save_file()

    def remove(self, assignment_id: int) -> None:
        """
        Removes an assignment from the repository by ID and saves to file.
        :param assignment_id: The ID of the assignment to remove
        :raises RepositoryException: if an assignment with the given ID does not exist
        :return: None
        """
        super().remove(assignment_id)
        self._save_file()

    def update(self, assignment: Assignment) -> None:
        """
        Updates an existing assignment in the repository and saves to file.
        :param assignment: the updated Assignment object
        :raises RepositoryException: if an assignment with the given ID does not exist
        :return: None
        """
        super().update(assignment)
        self._save_file()