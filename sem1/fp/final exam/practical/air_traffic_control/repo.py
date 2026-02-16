from datetime import datetime

from domain import Flight
from exceptions import RepoException


class TextFileRepo:
    def __init__(self, filename:str):
        self._filename = filename
        self._flights = {}
        self._load_file()

    def _load_file(self):
        with open(self._filename, "r") as fin:
            for line in fin:
                parts = line.strip().split(",")
                flight_id = parts[0]
                dep_city = parts[1]
                dep = parts[2]
                dep_time = datetime.strptime(dep, "%H:%M")
                arr_city = parts[3]
                arr = parts[4]
                arr_time = datetime.strptime(arr, "%H:%M")
                flight = Flight(flight_id, dep_city, dep_time, arr_city, arr_time)
                self._flights[flight_id] = flight

    def _save_file(self):
        with open(self._filename, "w") as fout:
            for f in self.get_all():
                dep_str = f.dep_time.strftime("%H:%M")
                arr_str = f.arr_time.strftime("%H:%M")
                fout.write(f"{f.id},{f.dep_city},{dep_str},{f.arr_city},{arr_str}\n")

    def get_all(self):
        return list(self._flights.values())

    def add_flight(self, new_flight:Flight):
        if new_flight.id in self._flights:
            raise RepoException("Duplicate flight!")
        self._flights[new_flight.id] = new_flight
        self._save_file()

    def delete_flight(self, flight_id:str):
        if flight_id not in self._flights:
            raise RepoException("The flight with the given ID does not exist!")
        del self._flights[flight_id]
        self._save_file()