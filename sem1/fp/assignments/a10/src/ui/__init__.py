
class ConsoleUI:
    def __init__(self, student_service, assignment_service):
        self._student_service = student_service
        self._assignment_service = assignment_service

    def start(self):
        while True:
            print("1. Add student")
            print("2. Remove student")
            print("3. Update student")
            print("4. List students")
            print("5. Add assignment")
            print("6. Remove assignment")
            print("7. Update assignment")
            print("8. List assignments")
            print("0. Exit")

            cmd = input(">> ")
            try:
                if cmd == "1":
                    self.ui_add_student()
                elif cmd == "2":
                    self.ui_remove_student()
                elif cmd == "3":
                    self.ui_update_student()
                elif cmd == "4":
                    self.ui_list_students()
                elif cmd == "5":
                    self.ui_add_assignment()
                elif cmd == "6":
                    self.ui_remove_assignment()
                elif cmd == "7":
                    self.ui_update_assignment()
                elif cmd == "8":
                    self.ui_list_assignments()
                elif cmd == "0":
                    return
            except RepositoryException as re:
                print("Error:", re)
