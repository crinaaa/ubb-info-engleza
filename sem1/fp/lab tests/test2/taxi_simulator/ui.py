from service import TaxiService

class ConsoleUI:
    def __init__(self, repo):
        self._repo = repo
        self._service = TaxiService(repo)

    def taxi_number(self):
        n = int(input("Enter number of taxis (0–10): "))
        while n < 0 or n > 10:
            print("Invalid number!")
            n = int(input("Enter number of taxis (0–10): "))
        return n

    def print_menu(self):
        self._service.generate_taxis(self.taxi_number())

        while True:
            print("\n1. Add a ride")
            print("2. Simulate a ride")
            print("3. Display taxis")
            print("0. Exit")

            try:
                choice = int(input("Choice: "))
            except ValueError:
                print("Enter a number!")
                continue

            if choice == 1:
                self.add_ride_ui()
            elif choice == 2:
                self.simulate_ride_ui()
            elif choice == 3:
                self.display_taxis_ui()
            elif choice == 0:
                print("Goodbye!")
                break
            else:
                print("Invalid!")

    def add_ride_ui(self):
        x1 = int(input("Start X: "))
        y1 = int(input("Start Y: "))
        x2 = int(input("End X: "))
        y2 = int(input("End Y: "))

        if not self._service.validate_coordinates(x1, y1) \
           or not self._service.validate_coordinates(x2, y2):
            print("Invalid coordinates!")
            return

        self._service.add_ride(x1, y1, x2, y2)
        self.display_taxis_ui()

    def simulate_ride_ui(self):
        x1,y1,x2,y2 = self._service.simulate_ride()
        print(f"Simulated ride: ({x1},{y1}) → ({x2},{y2})")
        self.display_taxis_ui()

    def display_taxis_ui(self):
        taxis = self._service.display_sorted()
        for t in taxis:
            print(f"Taxi {t.id}: ({t.x},{t.y}) fare={t.fare}")
