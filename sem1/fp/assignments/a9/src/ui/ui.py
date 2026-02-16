from datetime import datetime
from src.services.student_service import StudentService
from src.services.assignments_service import AssignmentService
from src.services.grade_service import GradeService
from src.exceptions import ValidationException, RepositoryException, ServiceException


class ConsoleUI:
    def __init__(self, student_service: StudentService, assignment_service: AssignmentService,
                 grade_service: GradeService):
        #initialize all 3 services
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service


    #print the Main Menu
    def run(self):
        while True:
            print("\nMain Menu")
            print("1. Manage Students")
            print("2. Manage Assignments")
            print("3. Assign Assignment")
            print("4. Grade Students")
            print("5. List Students")
            print("6. List Assignments")
            print("7. List Grades")
            print("0. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.manage_students()
            elif choice == "2":
                self.manage_assignments()
            elif choice == "3":
                self.assign_assignment()
            elif choice == "4":
                self.grade_student()
            elif choice == "5":
                self.list_students()
            elif choice == "6":
                self.list_assignments()
            elif choice == "7":
                self.list_grades()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option!")

    #student management
    def manage_students(self):
        while True:
            print("\nManage Students")
            print("1. Add Student")
            print("2. Update Student")
            print("3. Remove Student")
            print("4. Back to Main Menu")

            option = input("Choose an option: ").strip()

            if option == "1":
                self.add_student()
            elif option == "2":
                self.update_student()
            elif option == "3":
                self.remove_student()
            elif option == "4":
                return
            else:
                print("Invalid option!")

    def add_student(self):
        print("\nAdd Student")
        try:
            student_id = int(input("Student ID: "))
            name = input("Student Name: ").strip()
            group = int(input("Group: "))

            self._student_service.add_student(student_id, name, group)

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError:
            print("Please enter valid numbers for ID and group!")

    def update_student(self):
        print("Update Student")
        try:
            student_id = int(input("Student ID to update: "))
            name = input("New Name: ").strip()
            group = int(input("New Group: "))

            self._student_service.update_student(student_id, name, group)

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError:
            print("Please enter valid numbers for ID and group!")

    def remove_student(self):
        print("\nRemove Student")
        try:
            student_id = int(input("Student ID to remove: "))

            self._student_service.remove_student(student_id)

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError:
            print("Please enter a valid student ID!")



    #assignment management
    def manage_assignments(self):
        while True:
            print("\nManage Assignments")
            print("1. Add Assignment")
            print("2. Update Assignment")
            print("3. Remove Assignment")
            print("4. Back to Main Menu")

            option = input("Choose an option: ").strip()

            if option == "1":
                self.add_assignment()
            elif option == "2":
                self.update_assignment()
            elif option == "3":
                self.remove_assignment()
            elif option == "4":
                return
            else:
                print("Invalid option!")

    def add_assignment(self):
        print("\nAdd Assignment")
        try:
            assignment_id = int(input("Assignment ID: "))
            description = input("Description: ").strip()
            deadline_str = input("Deadline (YYYY-MM-DD): ")
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

            self._assignment_service.add_assignment(assignment_id, description, deadline)

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError as e:
            print(e)

    def update_assignment(self):
        print("\nUpdate Assignment")
        try:
            assignment_id = int(input("Assignment ID to update: "))
            description = input("New Description: ").strip()
            deadline_str = input("New Deadline (YYYY-MM-DD): ")
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

            self._assignment_service.update_assignment(assignment_id, description, deadline)

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError as e:
            print(e)

    def remove_assignment(self):
        print("\nRemove Assignment")
        try:
            assignment_id = int(input("Assignment ID to remove: "))

            self._assignment_service.remove_assignment(assignment_id)

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError:
            print("Please enter a valid assignment ID!")

    #assignment operations
    def assign_assignment(self):
        print("\nAssign Assignment")
        try:
            assignment_id = int(input("Assignment ID: "))
            choice = input("Assign to (1) Single Student or (2) Group? ").strip()

            if choice == "1":
                student_id = int(input("Student ID: "))
                self._grade_service.assign_to_student(assignment_id, student_id)

            elif choice == "2":
                group = int(input("Group number: "))
                self._grade_service.assign_to_group(assignment_id, group)

            else:
                print("Invalid choice.")

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError:
            print("Please enter valid numbers!")


    #grading with assignment selection
    def grade_student(self):
        print("\nGrade Student")
        try:
            student_id = int(input("Student ID: "))

            # get ungraded assignments
            ungraded = self._grade_service.get_ungraded_assignments_for_student(student_id)

            if not ungraded:
                print("This student has no ungraded assignments.")
                return

            print(f"\nUngraded assignments for student {student_id}:")
            for i, grade in enumerate(ungraded, 1):
                try:
                    assignment = self._assignment_service.get_assignment(grade.assignment_id)
                    print(f"{i}. Assignment {assignment.id}: {assignment.description}")
                except RepositoryException:
                    print(f"{i}. Assignment {grade.assignment_id}: [DELETED ASSIGNMENT]")
                    continue  # skip this one

            choice = int(input("\nSelect assignment number to grade (press 0 to cancel): "))
            if choice == 0:
                print("Grading cancelled.")
                return

            if 1 <= choice <= len(ungraded):
                selected_grade = ungraded[choice - 1]
                assignment_id = selected_grade.assignment_id

                grade_value = int(input(f"Grade for assignment {assignment_id} (1-10): "))

                self._grade_service.grade_student(student_id, assignment_id, grade_value)
            else:
                print("Invalid selection.")

        except (ValidationException, RepositoryException, ServiceException) as e:
            print(e)
        except ValueError:
            print("Please enter valid numbers!")

    #listing operations
    def list_students(self):
        try:
            students = self._student_service.list_students()

            if not students:
                print("No students found.")
                return

            print("\nStudents")
            for student in students:
                print(student)

        except Exception as e:
            print(e)

    def list_assignments(self):
        try:
            assignments = self._assignment_service.list_assignments()

            if not assignments:
                print("No assignments found.")
                return

            print("\nAssignments")
            for assignment in assignments:
                print(assignment)

        except Exception as e:
            print(e)

    def list_grades(self):
        try:
            grades = self._grade_service.list_grades()

            if not grades:
                print("No grades found.")
                return

            print("\nGrades")
            for grade in grades:
                grade_str = "Ungraded" if grade.grade is None else str(grade.grade)
                print(f"Assignment: {grade.assignment_id}, Student: {grade.student_id}, Grade: {grade_str}")

        except Exception as e:
            print(e)