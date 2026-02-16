from functions import *

def print_menu():
    print("1. Add a flight")
    print("2. Delete a flight")
    print("3. Show flights, sorted")
    print("4. Increase duration")
    print("5. Display all flights")

def add_flight_ui(flights:list):
    code = None
    duration = None
    departure = None
    destination = None
    try:
        code = input("Enter the code: ")
        if len(code)<3:
            raise ValueError("Invalid code!")
    except ValueError as ve:
        print(ve)

    try:
        duration = int(input("Enter the duration: "))
        if duration<20:
            raise ValueError("Invalid duration!")
    except ValueError as ve:
        print(ve)

    try:
        departure = input("Enter the departure city: ")
        if len(departure)<3:
            raise ValueError("Invalid departure city!")
    except ValueError as ve:
        print(ve)

    try:
        destination = input("Enter the destination city: ")
        if len(destination)<3:
            raise ValueError("Invalid destination!")
    except ValueError as ve:
        print(ve)

    flights.append(create_flight(code, duration, departure, destination))

def delete_flight_ui(flights: list):
    code = input("Enter the code: ")
    delete_flight(flights, code)

def sort_ui(flights:list):
    departure = input("Enter the departure city: ")
    sort_by_destination(flights, departure)

def increase_ui(flights:list):
    departure = input("Enter the departure city:")
    duration = None
    try:
        duration = int(input("Enter the delay (in minutes): "))
        if duration<10 or duration>60:
            raise ValueError("Invalid duration!")
    except ValueError as ve:
        print(ve)
    increase_duration(flights, departure, duration)

def display_ui(flights:list):
    t = Texttable()
    t.header(["Code", "Duration", "Departure", "Destination"])
    for flight in flights:
        t.add_row([get_code(flight), get_duration(flight), get_departure(flight), get_destination(flight)])
    print(t.draw())

def print_ui():
    flights = [{"code": "AB3456", "duration": 60, "departure": "Cluj", "destination": "Iasi"},
    {"code": "GH5678", "duration": 40, "departure":"Vienna" , "destination":"Prague"},
               {"code": "GH765", "duration": 35, "departure": "London", "destination": "Paris"}]

    commands = {"1": add_flight_ui, "2": delete_flight_ui, "3": sort_ui, "4": increase_ui, "5": display_ui}

    while True:
        print_menu()
        option = input("Enter your option: ")
        try:
            if option in commands:
                commands[option](flights)
            elif option == "x":
                print("Exiting the program...")
                break
            else:
                print("Invalid option!")
        except ValueError as ve:
            print(ve)