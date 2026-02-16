from repository import MemoryRepo
from ui import ConsoleUI

def start():
    ui = ConsoleUI(MemoryRepo())
    ui.print_menu()

start()
