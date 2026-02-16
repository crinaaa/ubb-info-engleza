from datetime import datetime


class TrainRoute:
    def __init__(self, number:int, dep_city:str, dep_time:datetime, arr_city:str, arr_time:datetime, tickets:int):
        self._number = number
        self._dep_city = dep_city
        self._dep_time = dep_time
        self._arr_city = arr_city
        self._arr_time = arr_time
        self._tickets = tickets
        self._sold = 0

    @property
    def number(self):
        return self._number

    @property
    def dep_city(self):
        return self._dep_city

    @property
    def dep_time(self):
        return self._dep_time

    @property
    def arr_city(self):
        return self._arr_city

    @property
    def arr_time(self):
        return self._arr_time

    @property
    def tickets(self):
        return self._tickets

    def decrease_tickets(self):
        self._tickets = self.tickets - 1

    def increase_sold(self):
        self._sold += 1

    @property
    def sold_count(self):
        return self._sold