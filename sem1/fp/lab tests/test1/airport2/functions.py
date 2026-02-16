from texttable import Texttable

def create_flight(code: str, duration: int, departure: str, destination: str) -> dict:
    return {"code": code, "duration": duration, "departure city": departure, "destination city": destination}

def get_code(flight:dict):
    return flight["code"]

def get_destination(flight: dict):
    return flight["destination city"]

def get_departure(flight:dict):
    return flight["departure city"]

def get_duration(flight:dict):
    return flight["duration"]

def set_destination(flight:dict, new_destination: str):
    flight["destination city"] = new_destination

def set_duration(flight: dict, new_duration: int):
    flight["duration"] = new_duration

def add_flight(flights_list: list, code: str, duration: int, departure: str, destination: str):
    flights_list.append(create_flight(code, duration, departure, destination))

# def add_flight(flights_list: list):
#     code = input("Enter the code of the flight: ")
#     duration = int(input("Enter the duration of the flight: "))
#     departure = input("Enter the departure city: ")
#     destination = input("Enter the destination city: ")
#     flights_list.append(create_flight(code, duration, departure, destination))

def modify_duration(code: str, new_duration: int, flights_list):
    for flight in flights_list:
        if get_code(flight) == code:
            set_duration(flight, new_duration)

def modify_destination(old_destination: str, new_destination: str, flights_list: list):
    if len(new_destination)<3:
        raise ValueError("Invalid new destination!")
    for flight in flights_list:
        if get_destination(flight) == old_destination:
            set_destination(flight, new_destination)

def sort_by_departure(flights_list, departure:str):
    l = []
    for flight in flights_list:
        if get_departure(flight) == departure:
            l.append(flight)
    for i in range(0, len(l) - 1):
        for j in range(i+1, len(l)):
            if get_duration(l[i]) > get_duration(l[j]):
                l[i], l[j] = l[j], l[i]
    return l

def display(flights_list: list):
    t = Texttable()
    t.header(["Code", "Duration", "Departure", "Destination"])
    for flight in flights_list:
        t.add_row([get_code(flight), get_duration(flight), get_departure(flight), get_destination(flight)])
    return t