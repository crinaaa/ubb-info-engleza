
from exceptions import ValidationException, RepositoryException
from service import StudentService


class ConsoleUI:
    def __init__(self, repo):
        self._student_service = StudentService(repo)
        self._repo = repo

    def print_menu(self):
        while True:
            print("1. Add a new student.")
            print("2. Sort students by their grades, in descending order.")
            print("3. Be kind! Give a bonus!")
            print("4. Search by word and sort,")
            print("0. Exit")

            try:
                choice = int(input("Choose an option"))
            except ValueError:
                print("Please enter a valid option!")
                continue

            if choice == 1:
                self.add_student()
            elif choice == 2:
                self.sort_grades()
            elif choice == 3:
                self.bonus()
            elif choice == 4:
                self.word()
            elif choice == 0:
                print("Bye!")
                break
            else:
                print("Invalid option!")

    def add_student(self):
        try:
            student_id = int(input("Enter the ID of the student: "))
            name = input("Enter the name of the student: ")
            attendances = int(input("Enter the number of attendances for the student: "))
            grade = int(input("Enter the grade of the student: "))

            self._student_service.add_student(student_id, name, attendances, grade)

        except ValueError:
            print("Please enter valid numeric values!")
        except (ValidationException, RepositoryException) as e:
            print(e)

    def sort_grades(self):
        students = self._student_service.get_students_sorted()

        for s in students:
            print(f"{s.id}, {s.name}, {s.attendances}, {s.grade}")

    def bonus(self):
        try:
            p = int(input("Enter the number of minimum attendances: "))
            b = int(input("Enter the value of the bonus: "))

            students = self._repo.get_all()
            for s in students:
                self._student_service.bonuses(s, p, b)

        except ValueError:
            print("Please enter valid integers!")

    def word(self):
        w = input("Enter a word: ")
        l = self._student_service.sort_by_name(w)

        for s in l:
            print(f"{s.id}, {s.name}, {s.attendances}, {s.grade}")