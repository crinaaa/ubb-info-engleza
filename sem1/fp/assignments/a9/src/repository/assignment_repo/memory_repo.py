from src.domain.assignment import Assignment, generate_assignments
from src.repository.repo_exceptions import RepositoryException


class AssignmentMemoryRepo:
    def __init__(self, prepopulate=True):
        self._assignments = {}
        if prepopulate:
            for a in generate_assignments(20):
                self.add(a)

    def add(self, new_assignment: Assignment) -> None:
        """
        Adds a new assignment to the repository.
        :param new_assignment: the Assignment object to add to the repository
        :raises RepositoryException: if an assignment with the same ID already exists
        :return: None
        """
        if new_assignment.id in self._assignments:
            raise RepositoryException(f"Assignment with ID {new_assignment.id} already exists!")
        self._assignments[new_assignment.id] = new_assignment

    def remove(self, assignment_id: int) -> None:
        """
        Removes an assignment from the repository by ID.
        :param assignment_id: the ID of the assignment to remove
        :raises RepositoryException: if an assignment with the given ID does not exist
        :return: None
        """
        if assignment_id not in self._assignments:
            raise RepositoryException(f"Assignment with ID {assignment_id} does not exist!")
        del self._assignments[assignment_id]

    def update(self, assignment: Assignment) -> None:
        """
        Updates an existing assignment in the repository.
        :param assignment: The updated Assignment object
        :raises RepositoryException: if an assignment with the given ID does not exist
        :return: None
        """
        if assignment.id not in self._assignments:
            raise RepositoryException(f"Assignment with ID {assignment.id} does not exist!")
        self._assignments[assignment.id] = assignment

    def get_all(self) -> list[Assignment]:
        """
        Returns all assignments in the repository.
        :return: A list containing all Assignment objects in the repository
        :rtype: list[Assignment]
        """
        return list(self._assignments.values())

    def get_by_id(self, assignment_id: int) -> Assignment:
        """
        Finds an assignment by its ID.
        :param assignment_id: The ID of the assignment to retrieve
        :return: The Assignment object with the matching ID
        :rtype: Assignment
        :raises RepositoryException: if an assignment with the given ID does not exist

        """
        if assignment_id not in self._assignments:
            raise RepositoryException(f"Assignment with ID {assignment_id} does not exist!")
        return self._assignments[assignment_id]