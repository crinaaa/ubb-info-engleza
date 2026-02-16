from texttable import Texttable

def create_flight(code:str, duration:int, departure:str, destination:str):
    return {"code": code, "duration": duration, "departure": departure, "destination": destination}

def get_code(flight:dict):
    return flight["code"]

def get_duration(flight:dict):
    return flight["duration"]

def get_departure(flight: dict):
    return flight["departure"]

def get_destination(flight: dict):
    return flight["destination"]

def set_duration(flight:dict, new_duration:int):
    flight["duration"] = new_duration

def delete_flight(flights:list, code:str):
    pos = 0
    for i in range(len(flights)):
        if get_code(flights[i]) == code:
            pos = i
    for i in range(pos, len(flights) - 1):
        flights[i] = flights[i+1]

def sort_by_destination(flights:list, departure:str):
    l = []
    for flight in flights:
        if get_departure(flight) == departure:
            l.append(flight)
    for i in range(0, len(l) - 1):
        for j in range(i+1, len(l)):
            if get_destination(l[i]) > get_destination(l[i]):
                l[i], l[j] = l[j], l[i]

def increase_duration(flights:list, departure:str, duration:int):
    if duration<10 or duration>60:
        raise ValueError("Duration out of range!")
    for flight in flights:
        if get_departure(flight) == departure:
            set_duration(get_duration(flight) + duration)