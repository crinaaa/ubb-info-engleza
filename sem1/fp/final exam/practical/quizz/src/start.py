from src.repository import TextRepo
from src.ui import ConsoleUI


def start():
    repo = TextRepo("master.txt")
    ui = ConsoleUI(repo)
    ui.run()

start()