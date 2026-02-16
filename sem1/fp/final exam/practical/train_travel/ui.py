from exceptions import ValidationException, RepoException
from service import TrainService
from datetime import datetime

class ConsoleUI:
    def __init__(self, repo):
        self._service = TrainService(repo)

    def print_menu(self):
        while True:
            print("1. Add a new train route.")
            print("2. Sell a ticket.")
            print("3. Show the total income.")
            print("4. Show report.")
            print("0. Exit.")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input!")
                continue

            if choice == 1:
                self.add_train_ui()

            elif choice == 2:
                self.sell_ui()

            elif choice == 3:
                self.show_income_ui()

            elif choice == 4:
                self.show_report_ui()

            elif choice == 0:
                print("Exiting!")
                break

            else:
                print("Invalid choice!")

    def add_train_ui(self):
        try:
            number = int(input("Enter the number of the train: "))
            dep_city = input("Enter the departure city: ")
            dep = input("Enter the departure time: ")
            arr_city = input("Enter the arrival city: ")
            arr = input("Enter the arrival time: ")
            tickets = int(input("Enter the number of the tickets: "))

            dep_time = datetime.strptime(dep, "%H:%M")
            arr_time = datetime.strptime(arr, "%H:%M")

            self._service.add_route(number, dep_city, dep_time, arr_city, arr_time, tickets)

        except ValueError:
            print("Invalid input!")
        except (ValidationException, RepoException) as e:
            print(e)

    def sell_ui(self):
        try:
            number = int(input("Enter the train number: "))
            route = self._service.find_route(number)
            price = self._service.ticket_price(route)
            print("The price is: ", price)
            accept = input("Do you want to continue?")
            if accept == "yes":
                self._service.increase_income(route, price)
            else:
                pass
        except ValueError:
            print("Invalid input!")


    def show_income_ui(self):
        i = self._service.income
        print("The income is: ", i)

    def show_report_ui(self):
        routes = self._service.sort_routes()
        for r in routes:
            print(f"Route {r.number},{r.dep_city},{r.dep_time},{r.arr_city},{r.arr_time},{r.tickets} has {r.sold_count} tickets sold!")