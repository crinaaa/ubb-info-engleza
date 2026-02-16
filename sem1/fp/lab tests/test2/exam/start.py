from repository import TextFileRepo
from service import StudentService
from ui import ConsoleUI


def start():
    repo = TextFileRepo("students.txt")
    ui = ConsoleUI(repo)
    ui.print_menu()


start()