from repository.bus_repo import BusTextFileRepo
from repository.route_repo import RouteTextFileRepo
from ui.ui import ConsoleUI


def start():
    bus_repo = BusTextFileRepo("buses.txt")
    route_repo = RouteTextFileRepo("bus_routes.txt")
    ui = ConsoleUI(bus_repo, route_repo)
    ui.print_menu()

start()