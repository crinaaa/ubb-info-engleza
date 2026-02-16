from service import GameService
from ui import ConsoleUI


def start():
    service = GameService()
    ui = ConsoleUI(service)
    ui.run()

start()