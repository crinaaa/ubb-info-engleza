from domain import Flight
from exceptions import ValidationException
from repo import TextFileRepo
from datetime import datetime

class FlightService:
    def __init__(self, repo: TextFileRepo):
        self._repo = repo

    def add_flight(self, flight_id:str, dep_city:str, dep_time:datetime, arr_city:str, arr_time:datetime):
        duration = arr_time - dep_time
        total_seconds = duration.total_seconds()
        total_minutes = total_seconds / 60

        if total_minutes < 15 or total_minutes > 90:
            raise ValidationException("The flight time is between 15 and 90 minutes!")

        all_flights = self._repo.get_all()

        for flight in all_flights:
            if flight.dep_city == dep_city and flight.dep_time == dep_time:
                raise ValidationException("Airport busy at departure!")
            if flight.dep_city == arr_city and flight.arr_time == dep_time:
                raise ValidationException("Airport busy at departure!")

            if flight.arr_city == arr_city and flight.arr_time == arr_time:
                raise ValidationException("Flight busy at arrival!")
            if flight.arr_city == dep_city and flight.dep_time == arr_time:
                raise ValidationException("Airport busy at arrival!")

        new_flight = Flight(flight_id, dep_city, dep_time, arr_city, arr_time)
        self._repo.add_flight(new_flight)


    def delete_flight(self, flight_id):
        self._repo.delete_flight(flight_id)

    def get_activity(self):
        all_flights = self._repo.get_all()
        activity = {}

        for flight in all_flights:
            dep = flight.dep_city
            if dep in activity:
                activity[dep] += 1
            else:
                activity[dep] = 1
            arr = flight.arr_city
            if arr in activity:
                activity[arr] += 1
            else:
                activity[arr] = 1

        sorted_activity = sorted(activity.items(), key=lambda x: x[1], reverse=True)
        return sorted_activity


    def get_free_intervals(self):
        start_day = datetime.strptime("00:00","%H:%M")
        end_day = datetime.strptime("23:59", "%H:%M")

        all_flights = self._repo.get_all()
        all_flights.sort(key=lambda x: x.dep_time)
        free_intervals = []

        if all_flights[0].dep_time > start_day:
            free_intervals.append((start_day,all_flights[0].dep_time))

        for i in range(0, len(all_flights)-1):
            if all_flights[i].arr_time < all_flights[i+1].dep_time:
                free_intervals.append((all_flights[i].arr_time,all_flights[i+1].dep_time))

        if all_flights[-1].arr_time < end_day:
            free_intervals.append((all_flights[-1].arr_time,end_day))

        free_intervals.sort(key=lambda x: (x[1]-x[0]), reverse=True)
        return free_intervals

    def backup_radar(self):
        all_flights = self._repo.get_all()
        all_flights.sort(key=lambda x: x.arr_time)

        accepted_flights = []
        last_arrival_time = datetime.strptime("00:00", "%H:%M")

        for flight in all_flights:
            if flight.dep_time >= last_arrival_time:
                accepted_flights.append(flight)
                last_arrival_time = flight.arr_time

        return accepted_flights