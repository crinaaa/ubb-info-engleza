import unittest
from src.services.student_service import StudentService
from src.repository.student_repo.memory_repo import StudentMemoryRepo
from src.repository.grade_repo.memory_repo import GradeMemoryRepo
from src.exceptions import ValidationException, RepositoryException


class TestStudentService(unittest.TestCase):

    def setUp(self):
        self.repo = StudentMemoryRepo(prepopulate=False)
        self.grade_repo = GradeMemoryRepo(prepopulate=False)
        self.service = StudentService(self.repo, self.grade_repo)

    def test_add_and_get_student(self):
        self.service.add_student(1, "John", 101)
        student = self.service.get_student(1)
        self.assertEqual(student.name, "John")
        self.assertEqual(student.group, 101)

    def test_add_student_invalid(self):
        with self.assertRaises(ValidationException):
            self.service.add_student(0, "John", 101)  # invalid ID
        with self.assertRaises(ValidationException):
            self.service.add_student(1, "", 101)  # no name

    def test_list_students(self):
        self.service.add_student(1, "John", 101)
        self.service.add_student(2, "Jane", 102)
        students = self.service.list_students()
        self.assertEqual(len(students), 2)

    def test_update_student(self):
        self.service.add_student(1, "Old", 101)
        self.service.update_student(1, "New", 201)
        student = self.service.get_student(1)
        self.assertEqual(student.name, "New")
        self.assertEqual(student.group, 201)

    def test_remove_student(self):
        self.service.add_student(1, "John", 101)
        self.service.remove_student(1)
        with self.assertRaises(RepositoryException):
            self.service.get_student(1)


if __name__ == '__main__':
    unittest.main()