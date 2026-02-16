from repo import TextFileRepo
from ui import ConsoleUI


def start():
    repo = TextFileRepo("flights.txt")
    ui = ConsoleUI(repo)
    ui.print_menu()

start()