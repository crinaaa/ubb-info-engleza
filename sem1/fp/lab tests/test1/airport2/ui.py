from functions import *

def print_menu():
    print("1. Add a flight.")
    print("2. Modify the duration of a flight.")
    print("3. Reroute a flight.")
    print("4. Sort by the duration.")
    print("5. Display the flights.")
    print("6. Exit.")

def ui_add_flight(flights: list):

    code = None
    duration = None
    destination = None
    departure = None

    try:
        code = input("Enter the code: ")
        if len(code)<3:
            raise ValueError("Invalid code!")
    except ValueError as ve:
        print(ve)

    try:
        duration = int(input("Enter the duration: "))
        if duration < 20:
            raise ValueError("Invalid duration!")
    except ValueError as ve:
        print(ve)

    try:
        departure = input("Enter the departure city: ")
        if len(departure)<3:
            raise ValueError("Invalid departure!")
    except ValueError as ve:
        print(ve)

    try:
        destination = input("Enter the destination city: ")
        if len(destination)<3:
            raise ValueError("Invalid destination")
    except ValueError as ve:
        print(ve)

    flights.append(create_flight(code, duration, departure, destination))


def ui_modify_duration(flights):
    code = input("Enter code of flight to modify: ")
    new_duration = int(input("Enter new duration: "))

    modify_duration(code, new_duration, flights)

def ui_modify_destination(flights):
    new = None
    old = input("Enter the current destination: ")
    try:
        new = input("Enter the new destination: ")
        if len(new)<3:
            raise ValueError("Invalid destination!")
    except ValueError as ve:
        print(ve)

    modify_destination(old, new, flights)


def ui_sort_by_departure(flights):
    departure = input("Enter the departure city: ")
    print(sort_by_departure(flights, departure))

def ui_display_flights(flights):
    print(display(flights).draw())


def print_ui():
    flights = [
        create_flight("TY7890", 50, "Cluj-Napoca", "Paris"),
        create_flight("AB1234", 120, "Bucharest", "London"),
        create_flight("CD5678", 95, "Berlin", "Rome"),
        create_flight("EF9012", 180, "Madrid", "New York"),
        create_flight("GH3456", 75, "Vienna", "Amsterdam"),
        create_flight("IJ7891", 140, "Prague", "Dublin")
    ]

    commands = {"1": ui_add_flight, "2": ui_modify_duration, "3": ui_modify_destination, "4": ui_sort_by_departure, "5": ui_display_flights}

    while True:
        print_menu()
        option = input("Enter your option: ")
        try:
            if option in commands:
                commands[option](flights)
            elif option == "6":
                print("Exiting the program...")
                return
            else:
                print("Invalid option!")
        except ValueError as ve:
            print(ve)