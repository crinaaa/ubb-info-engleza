from repository.repo import PlayerTextFileRepo
from ui.ui import ConsoleUI


def start():
    repo = PlayerTextFileRepo("players.txt")
    ui = ConsoleUI(repo)
    ui.run()

start()