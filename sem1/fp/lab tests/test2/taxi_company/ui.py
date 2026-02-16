from exceptions import ValidationException, RepoException
from service import Service


class ConsoleUI:
    def __init__(self, repo):
        self._service = Service(repo)
        self._repo = repo

    def print_menu(self):
        while True:
            print("1. Add an address.")
            print("2. Display all addresses.")
            print("3. Display possible locations for taxi stations.")
            print("4. Optimal position for new taxi station.")
            print("0. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Please enter a valid input")
                continue

            if choice == 1:
                self.add()

            elif choice == 2:
                self.display()

            elif choice == 3:
                self.taxi_stations()

            elif choice == 4:
                self.optimal_pos()

            elif choice == 0:
                print("Exiting!")
                break

            else:
                print("Invalid choice!")

    def add(self):
        try:
            addr_id = int(input("Enter ID: "))
            name = input("Enter name: ").strip()
            number = int(input("Enter number: "))
            x = int(input("Enter x coordinate: "))
            y = int(input("Enter y coordinate: "))
            self._service.add_address(addr_id, name, number, x, y)
        except ValueError:
            print("Please enter valid numbers for ID, number, and coordinates.")
        except (ValidationException, RepoException) as e:
            print(e)

    def display(self):
        l = self._repo.get_all()
        for a in l:
            print(f"{a.id}, {a.name}, {a.number}, {a.x}, {a.y}")

    def taxi_stations(self):
        try:
            x = int(input("Enter x coordinate: "))
            y = int(input("Enter y coordinate: "))
            d = int(input("Enter distance value: "))

            l = self._service.where_to_place_station(x, y, d)
            for a in l:
                print(f"{a.id}, {a.name}, {a.number}, {a.x}, {a.y}")

        except ValueError:
            print("Please enter valid inputs!")

    def optimal_pos(self):
        x, y = self._service.new_taxi_station()
        print(x,y)