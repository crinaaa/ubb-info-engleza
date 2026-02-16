from repo import TextFileRepo
from ui import ConsoleUI


def start():
    repo = TextFileRepo("sentences.txt")
    ui = ConsoleUI(repo)
    ui.run()

start()