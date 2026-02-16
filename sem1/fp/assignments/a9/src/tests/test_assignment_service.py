import unittest
from datetime import date, timedelta
from src.services.assignments_service import AssignmentService
from src.repository.assignment_repo.memory_repo import AssignmentMemoryRepo
from src.repository.grade_repo.memory_repo import GradeMemoryRepo
from src.exceptions import ValidationException, RepositoryException


class TestAssignmentService(unittest.TestCase):

    def setUp(self):
        # Use actual repositories (no prepopulation)
        self.repo = AssignmentMemoryRepo(prepopulate=False)
        self.grade_repo = GradeMemoryRepo(prepopulate=False)
        self.service = AssignmentService(self.repo, self.grade_repo)
        self.tomorrow = date.today() + timedelta(days=1)

    def test_add_and_get_assignment(self):
        self.service.add_assignment(1, "Math homework", self.tomorrow)
        assignment = self.service.get_assignment(1)
        self.assertEqual(assignment.description, "Math homework")
        self.assertEqual(assignment.deadline, self.tomorrow)

    def test_add_assignment_invalid(self):
        yesterday = date.today() - timedelta(days=1)

        with self.assertRaises(ValidationException):
            self.service.add_assignment(0, "Test", self.tomorrow)  # invalid id
        with self.assertRaises(ValidationException):
            self.service.add_assignment(1, "", self.tomorrow)  # no description
        with self.assertRaises(ValidationException):
            self.service.add_assignment(1, "Test", yesterday)  # late turn in

    def test_list_assignments(self):
        self.service.add_assignment(1, "Math", self.tomorrow)
        self.service.add_assignment(2, "Science", self.tomorrow)
        assignments = self.service.list_assignments()
        self.assertEqual(len(assignments), 2)

    def test_update_assignment(self):
        self.service.add_assignment(1, "Old description", self.tomorrow)
        new_deadline = self.tomorrow + timedelta(days=5)
        self.service.update_assignment(1, "Updated description", new_deadline)
        assignment = self.service.get_assignment(1)
        self.assertEqual(assignment.description, "Updated description")
        self.assertEqual(assignment.deadline, new_deadline)



if __name__ == '__main__':
    unittest.main()