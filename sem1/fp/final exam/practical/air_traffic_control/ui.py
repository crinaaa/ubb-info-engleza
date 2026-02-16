from time import strftime

from exceptions import RepoException, ValidationException
from repo import TextFileRepo
from service import FlightService
from datetime import datetime


class ConsoleUI:
    def __init__(self, repo:TextFileRepo):
        self._service = FlightService(repo)

    def print_menu(self):
        while True:
            print("1. Add a new flight.")
            print("2. Delete a flight.")
            print("3. Sort by activity.")
            print("4. Sort free intervals.")
            print("5. Backup radar.")
            print("0. Exit")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input!")
                continue

            if choice == 1:
                self.add_flight()

            elif choice == 2:
                self.delete_flight()

            elif choice == 3:
                self.sort_activity()

            elif choice == 4:
                self.free_intervals()

            elif choice == 5:
                self.backup_radar()

            elif choice == 0:
                print("Exiting!")
                break

            else:
                print("Invalid choice!")

    def add_flight(self):
        try:
            flight_id = input("Enter the flight ID: ")
            dep_city = input("Enter the departure city: ")
            dep_time = input("Enter the departure time: ")
            arr_city = input("Enter the arrival city: ")
            arr_time = input("Enter the arrival time: ")
            dep = datetime.strptime(dep_time, "%H:%M")
            arr = datetime.strptime(arr_time, "%H:%M")
            self._service.add_flight(flight_id, dep_city, dep, arr_city, arr)
        except (RepoException, ValidationException) as e:
            print(e)

    def delete_flight(self):
        try:
            flight_id = input("Enter the flight ID: ")
            self._service.delete_flight(flight_id)
        except RepoException as e:
            print(e)

    def sort_activity(self):
        airports = self._service.get_activity()
        for a in airports:
            print(a[0],":",a[1])

    def free_intervals(self):
        intervals = self._service.get_free_intervals()
        for i in intervals:
            print(f"({datetime.strftime(i[0],"%H:%M")}-{datetime.strftime(i[1],"%H:%M")})")

    def backup_radar(self):
        flights = self._service.backup_radar()
        print("We have ",len(flights),"flights")
        for f in flights:
            dep = f.dep_time.strftime("%H:%M")
            arr = f.arr_time.strftime("%H:%M")
            print(f"{dep},|,{arr},{f.id},|{f.dep_city}-{f.arr_city}")