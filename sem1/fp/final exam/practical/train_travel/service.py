from datetime import datetime

from domain import TrainRoute
from exceptions import ValidationException


class TrainService:
    def __init__(self, repo):
        self._repo = repo
        self._income = 0


    def add_route(self, number:int, dep_city:str, dep_time:datetime, arr_city:str, arr_time:datetime, tickets:int):
        if dep_city == arr_city:
            raise ValidationException("Departure and arrival city cannot be the same!")
        if dep_time > arr_time:
            raise ValidationException("The arrival cannot precede the departure!")
        if tickets < 0:
            raise ValidationException("The number of tickets must be a positive integer!")

        new_route = TrainRoute(number, dep_city, dep_time, arr_city, arr_time, tickets)
        self._repo.add_train_route(new_route)

    def ticket_price(self, route: TrainRoute):
        duration = route.arr_time - route.dep_time
        total_seconds = duration.total_seconds()
        total_minutes = total_seconds / 60
        price = total_minutes * self._repo.rate
        return price

    def find_route(self, number:int):
        trains = self._repo.get_all()
        wanted = None
        for t in trains:
            if t.number == number:
                wanted = t
                break
        return wanted

    def increase_income(self, route:TrainRoute, price:int):
        self._income += price
        route.decrease_tickets()
        route.increase_sold()
        self._repo.save()

    @property
    def income(self):
        return self._income

    def sort_routes(self):
        routes = self._repo.get_all()
        sorted_routes = sorted(routes, key=lambda route: route.sold_count, reverse=True)
        return sorted_routes