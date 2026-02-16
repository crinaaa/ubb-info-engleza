from service.bus_service import BusService


class ConsoleUI:
    def __init__(self, bus_repo, route_repo):
        self._bus_service = BusService(bus_repo, route_repo)

    def print_menu(self):
        while True:
            print("1. Display all buses travelling across a certain route.")
            print("2. For a given bus, compute how many kilometers it has travelled.")
            print("3. Display all bus routes, in descending order of their total mileage.")
            print("0. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a valid input!")
                continue

            if choice == 1:
                self.bus_on_route()

            elif choice == 2:
                self.compute_kilometers()

            elif choice == 3:
                self.display_ordered_mileage()

            elif choice == 0:
                print("Exiting. Bye!")
                break

            else:
                print("Invalid input! Try again!")

    def bus_on_route(self):
        try:
            route = int(input("Enter the route code: "))
            l = self._bus_service.display_bus_on_route(route)
            for bus in l:
                print(f"{bus.id},{bus.route},{bus.model},{bus.times}")
        except ValueError:
            print("Please enter a valid route code!")

    def compute_kilometers(self):
        try:
            bus_id = int(input("Enter the ID of the bus: "))
            n =  self._bus_service.compute_km(bus_id)
            print(n)
        except ValueError:
            print("Please enter a valid bus ID!")

    def display_ordered_mileage(self):
        data = self._bus_service.order_routes()

        for route, km, buses in data:
            print(f"Route {route.id} has a total mileage of: {km}.")

            print("Buses on this route are:")
            for bus in buses:
                print(f"{bus.id},{bus.route},{bus.model},{bus.times}")