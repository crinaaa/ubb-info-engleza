from service.service import GameService
from ui.ui import ConsoleUI


def start():
    service = GameService()
    ui = ConsoleUI(service)
    ui.play()

start()