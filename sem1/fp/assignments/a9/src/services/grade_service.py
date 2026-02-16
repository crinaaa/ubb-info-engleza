from src.domain.grade import Grade
from src.exceptions import ValidationException, RepositoryException, ServiceException


class GradeService:
    def __init__(self, grade_repo, student_repo, assignment_repo):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._assignment_repo = assignment_repo

    # assign to student or group

    def assign_to_student(self, assignment_id: int, student_id: int):
        try:
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")


            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            # check if assignment exists
            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            # check if student already has this assignment
            if self._grade_repo.grade_exists(assignment_id, student_id):
                raise RepositoryException(
                    f"Student {student_id} already has assignment {assignment_id}"
                )

            # create and add grade
            grade = Grade(assignment.id, student.id, None)
            self._grade_repo.add_auto(grade)
            return True

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error assigning assignment: {e}")

    def assign_to_group(self, assignment_id: int, group: int):
        """
        Assign assignment to all students in a group.
        Students who already have this assignment are skipped.
        Returns list of student IDs who received the assignment.
        """
        try:
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")
            if group <= 0:
                raise ValidationException("Group must be positive")

            # check if assignment exists
            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            # get all students in the group
            students_in_group = [
                student for student in self._student_repo.get_all()
                if student.group == group
            ]

            if not students_in_group:
                raise ValidationException(f"No students found in group {group}")

            assigned_students = []
            for student in students_in_group:
                # skip students who already have this assignment
                if not self._grade_repo.grade_exists(assignment_id, student.id):
                    grade = Grade(assignment.id, student.id, None)
                    self._grade_repo.add_auto(grade)
                    assigned_students.append(student.id)

            return assigned_students

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error assigning to group: {e}")


    #grade students with ungraded assignments
    def get_ungraded_assignments_for_student(self, student_id: int):
        """
        Get all ungraded assignments for a specific student.
        Used for UI to show list of assignments that can be graded.
        """
        try:
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            return self._grade_repo.get_ungraded_by_student(student_id)

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error getting ungraded assignments: {e}")

    def grade_student(self, student_id: int, assignment_id: int, grade_value: int):
        """
        Grade a student for a specific assignment.
        Student cannot be graded for assignments they don't have.
        Grade cannot be changed once set.
        """
        try:
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")
            if not (1 <= grade_value <= 10):
                raise ValidationException("Grade must be between 1 and 10")

            # check if student exists
            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            # check if assignment exists
            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            # check if student has this assignment
            if not self._grade_repo.grade_exists(assignment_id, student_id):
                raise RepositoryException(
                    f"Student {student_id} doesn't have assignment {assignment_id}"
                )

            # mark the grade
            self._grade_repo.update_grade(assignment_id, student_id, grade_value)
            return True

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error grading student: {e}")

   #list operations
    def list_grades(self):
        try:
            return self._grade_repo.get_all()
        except Exception as e:
            raise ServiceException(e)

    def get_student_grades(self, student_id: int):
        try:
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            # check if student exists
            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            all_grades = self._grade_repo.get_all()
            return [g for g in all_grades if g.student_id == student_id]

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(e)

    def get_assignment_grades(self, assignment_id: int):
        try:
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")

            # check if assignment exists
            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            all_grades = self._grade_repo.get_all()
            return [g for g in all_grades if g.assignment_id == assignment_id]

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error getting assignment grades: {e}")


    #delete
    def delete_student_grades(self, student_id: int):
        try:
            self._grade_repo.remove_by_student(student_id)
        except Exception as e:
            raise ServiceException(f"Error deleting student grades: {e}")

    def delete_assignment_grades(self, assignment_id: int):
        try:
            self._grade_repo.remove_by_assignment(assignment_id)
        except Exception as e:
            raise ServiceException(f"Error deleting assignment grades: {e}")