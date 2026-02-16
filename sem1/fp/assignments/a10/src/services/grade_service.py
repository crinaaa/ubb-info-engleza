from datetime import date

from src.domain.grade import Grade
from src.exceptions import ValidationException, RepositoryException, ServiceException
from src.services.assignments_service import AssignmentService
from src.services.student_service import StudentService
from src.services.undo_service import FunctionCall, Operation


class GradeService:
    def __init__(self, grade_repo, student_repo, assignment_repo,
                 student_service:StudentService, assignment_service: AssignmentService, undo_service=None):
        self._grade_repo = grade_repo
        self._student_repo = student_repo
        self._assignment_repo = assignment_repo
        self._undo_service = undo_service
        self._student_service = student_service
        self._assignment_service = assignment_service


    def _execute_multiple(self, function_calls):
        #execute multiple function calls
        for func_call in function_calls:
            func_call.call()

    # assign to student or group

    def assign_to_student(self, assignment_id: int, student_id: int):
        """
        Assign an assignment to a specific student.

        :param assignment_id: The ID of the assignment to assign
        :param student_id: The ID of the student to assign to
        :return: True if assignment was successful
        :raises ValidationException: If IDs are not positive
        :raises RepositoryException: If student/assignment doesn't exist or already assigned
        :raises ServiceException: If any other error occurs
        """
        try:
            # validation
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            # check if student exists
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

            # create grade (ungraded)
            grade = Grade(assignment.id, student.id, None)

            # create undo/redo operations
            undo_call = FunctionCall(self._grade_repo.remove_by_student_assignment,
                                     assignment_id, student_id)
            redo_call = FunctionCall(self._grade_repo.add_auto, grade)
            operation = Operation(undo_call, redo_call)

            # add the grade
            self._grade_repo.add_auto(grade)

            # record for undo
            if self._undo_service:
                self._undo_service.record(operation)

            return True

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error assigning assignment: {e}")

    def assign_to_group(self, assignment_id: int, group: int):
        """
        Assign assignment to all students in a group.
        Students who already have this assignment are skipped.

        :param assignment_id: The ID of the assignment to assign
        :param group: The group number to assign to
        :return: List of student IDs who received the assignment
        :raises ValidationException: If IDs are not positive or group is empty
        :raises RepositoryException: If assignment doesn't exist
        :raises ServiceException: If any other error occurs
        """
        try:
            # validation
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
            added_grades = []  #this time, track grades for undo

            for student in students_in_group:
                # skip students who already have this assignment
                if not self._grade_repo.grade_exists(assignment_id, student.id):
                    grade = Grade(assignment.id, student.id, None)
                    added_grades.append(grade)
                    self._grade_repo.add_auto(grade)
                    assigned_students.append(student.id)


            # create undo/redo operations for assigning
            if self._undo_service and added_grades:
                # undo: remove all added grades
                undo_calls = [
                    FunctionCall(self._grade_repo.remove_by_student_assignment,
                                 grade.assignment_id, grade.student_id)
                    for grade in added_grades
                ]

                # redo: add all grades back
                redo_calls = [
                    FunctionCall(self._grade_repo.add_auto, grade)
                    for grade in added_grades
                ]

                # create combined operations
                undo_combined = FunctionCall(self._execute_multiple, undo_calls)
                redo_combined = FunctionCall(self._execute_multiple, redo_calls)
                operation = Operation(undo_combined, redo_combined)

                # record for undo
                self._undo_service.record(operation)

            return assigned_students

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error assigning to group: {e}")

    def grade_student(self, student_id: int, assignment_id: int, grade_value: int):
        """
        Grade a student for a specific assignment.

        :param student_id: The ID of the student to grade
        :param assignment_id: The ID of the assignment to grade
        :param grade_value: The grade value (1-10)
        :return: True if grading was successful
        :raises ValidationException: If IDs are not positive or grade is invalid
        :raises RepositoryException: If student/assignment doesn't exist or not assigned
        :raises ServiceException: If any other error occurs
        """
        try:
            # validation
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

            # get the current grade before updating (for undo)
            current_grade = self._grade_repo.get_grade(assignment_id, student_id)

            if current_grade.grade is not None:
                raise RepositoryException(
                    f"Assignment {assignment_id} for student {student_id} is already graded with {current_grade.grade}"
                )

            # create undo/redo operations
            undo_call = FunctionCall(self._grade_repo.set_grade,
                                     assignment_id, student_id, current_grade.grade)  # current_grade.grade is None
            redo_call = FunctionCall(self._grade_repo.set_grade,
                                     assignment_id, student_id, grade_value)
            operation = Operation(undo_call, redo_call)


            self._grade_repo.set_grade(assignment_id, student_id, grade_value)

            # record for undo
            if self._undo_service:
                self._undo_service.record(operation)

            return True

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error grading student: {e}")


    def get_ungraded_assignments_for_student(self, student_id: int):
        """
        Get all ungraded assignments for a specific student.

        :param student_id: The ID of the student
        :return: List of ungraded Grade objects
        :raises ValidationException: If student_id is not positive
        :raises RepositoryException: If student doesn't exist
        :raises ServiceException: If any other error occurs
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

    def list_grades(self):
        """
        List all grades in the system.

        :return: List of all Grade objects
        :raises ServiceException: If any error occurs
        """
        try:
            return self._grade_repo.get_all()
        except Exception as e:
            raise ServiceException(f"Error listing grades: {e}")

    def get_student_grades(self, student_id: int):
        """
        Get all grades for a specific student.

        :param student_id: The ID of the student
        :return: List of Grade objects for the student
        :raises ValidationException: If student_id is not positive
        :raises RepositoryException: If student doesn't exist
        :raises ServiceException: If any other error occurs
        """
        try:
            if student_id <= 0:
                raise ValidationException("Student ID must be positive")

            student = self._student_repo.get_by_id(student_id)
            if not student:
                raise RepositoryException(f"Student with ID {student_id} does not exist")

            all_grades = self._grade_repo.get_all()
            return [g for g in all_grades if g.student_id == student_id]

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error getting student grades: {e}")

    def get_assignment_grades(self, assignment_id: int):
        """
        Get all grades for a specific assignment.

        :param assignment_id: The ID of the assignment
        :return: List of Grade objects for the assignment
        :raises ValidationException: If assignment_id is not positive
        :raises RepositoryException: If assignment doesn't exist
        :raises ServiceException: If any other error occurs
        """
        try:
            if assignment_id <= 0:
                raise ValidationException("Assignment ID must be positive")

            assignment = self._assignment_repo.get_by_id(assignment_id)
            if not assignment:
                raise RepositoryException(f"Assignment with ID {assignment_id} does not exist")

            all_grades = self._grade_repo.get_all()
            return [g for g in all_grades if g.assignment_id == assignment_id]

        except (ValidationException, RepositoryException) as e:
            raise e
        except Exception as e:
            raise ServiceException(f"Error getting assignment grades: {e}")


    def delete_student_grades(self, student_id: int):
        """
        Delete all grades for a specific student.
        Note: This is usually called from StudentService.remove_student()

        :param student_id: The ID of the student
        :raises ServiceException: If any error occurs
        """
        try:
            self._grade_repo.remove_by_student(student_id)
        except Exception as e:
            raise ServiceException(f"Error deleting student grades: {e}")

    def delete_assignment_grades(self, assignment_id: int):
        """
        Delete all grades for a specific assignment.
        Note: This is usually called from AssignmentService.remove_assignment()

        :param assignment_id: The ID of the assignment
        :raises ServiceException: If any error occurs
        """
        try:
            self._grade_repo.remove_by_assignment(assignment_id)
        except Exception as e:
            raise ServiceException(f"Error deleting assignment grades: {e}")

    #STATISTICS!!!

    def get_assignment_statistics(self, assignment_id: int):
        #get students with a given assignment, sorted by grade descending.

        try:
            assignment_grades = self.get_assignment_grades(assignment_id)

            result = []
            for grade in assignment_grades:
                if grade.grade is not None:
                    student = self._student_service.get_student(grade.student_id)
                    result.append((student, grade.grade))

            # sort by grade, which has the first pos in the (grade, student) tuple
            result.sort(key=lambda x: x[1], reverse=True)   # sort descending
            return result

        except Exception as e:
            raise ServiceException(f"Error getting assignment statistics: {e}")

    def get_late_students(self):
        #get students with late assignments (that is, ungraded+deadline passed)

        try:
            all_grades = self.list_grades()
            today = date.today()

            late_students = set()

            for grade in all_grades:
                if grade.grade is None:
                    try:
                        assignment = self._assignment_service.get_assignment(grade.assignment_id)
                        if assignment.deadline < today:
                            student = self._student_service.get_student(grade.student_id)
                            late_students.add(student)
                    except RepositoryException:
                        continue

            return list(late_students)

        except Exception as e:
            raise ServiceException(f"Error getting late students: {e}")

    def get_students_by_average_grade(self):
        #get students sorted by average grade descending

        try:
            all_students = self._student_service.list_students()
            all_grades = self.list_grades()

            averages = []

            for student in all_students:
                student_grades = [g for g in all_grades
                                  if g.student_id == student.id and g.grade is not None]

                if student_grades:
                    avg = sum(g.grade for g in student_grades) / len(student_grades)
                    averages.append((student, round(avg, 2)))

            averages.sort(key=lambda x: x[1], reverse=True)
            return averages

        except Exception as e:
            raise ServiceException(f"Error getting students by average: {e}")