from datetime import datetime


class Flight:
    def __init__(self, flight_id:str, dep_city:str, dep_time:datetime, arr_city:str, arr_time:datetime):
        self._id = flight_id
        self._dep_city = dep_city
        self._dep_time = dep_time
        self._arr_city = arr_city
        self._arr_time = arr_time

    @property
    def id(self):
        return self._id

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