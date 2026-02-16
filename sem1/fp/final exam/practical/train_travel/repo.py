from datetime import datetime

from domain import TrainRoute
from exceptions import RepoException


class TextFileRepo:
    def __init__(self, filename:str):
        self._filename = filename
        self._rate = None
        self._trains = {}
        self._load_file()

    def _load_file(self):
        with open(self._filename, "r") as fin:
            self._rate = int(fin.readline().strip())
            for line in fin:
                parts = line.strip().split(",")
                number = int(parts[0])
                dep_city = parts[1]
                dep_time = datetime.strptime(parts[2], "%H:%M")
                arr_city = parts[3]
                arr_time = datetime.strptime(parts[4], "%H:%M")
                tickets = int(parts[5])
                route = TrainRoute(number, dep_city, dep_time, arr_city, arr_time, tickets)
                self._trains[number] = route

    def _save_file(self):
        with open(self._filename, "w") as fout:
            fout.write(f"{self._rate}\n")
            for t in self.get_all():
                dep_str = t.dep_time.strftime("%H:%M")
                arr_str = t.arr_time.strftime("%H:%M")
                fout.write(f"{t.number},{t.dep_city},{dep_str},{t.arr_city},{arr_str},{t.tickets}\n")

    def save(self):
        self._save_file()

    def get_all(self):
        return list(self._trains.values())

    def add_train_route(self, new_route:TrainRoute):
        if new_route.number in self._trains:
            raise RepoException("A train route with the given number already exists!")
        self._trains[new_route.number] = new_route
        self._save_file()

    @property
    def rate(self):
        return self._rate