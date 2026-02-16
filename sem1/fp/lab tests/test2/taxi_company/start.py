from repository import TextRepo
from ui import ConsoleUI


def start():
    repo = TextRepo("addresses.txt")
    ui = ConsoleUI(repo)
    ui.print_menu()

start()