from enum import nonmember

from domain import Address
from exceptions import ValidationException
from math import sqrt


class Service:
    def __init__(self, repo):
        self._repo = repo

    def add_address(self, addr_id:int, name:str, number:int, x:int, y:int):
        try:
            if addr_id < 0:
                raise ValidationException("The ID must be a positive integer! Please try again!")

            if not name or len(name.strip()) < 3:
                raise ValidationException("The name must contain at least 3 characters! Please try again!")

            if number < 0 or number > 100:
                raise ValidationException("The number must be a positive integer and at most 100!")

            if x < -100 or x > 100:
                raise ValidationException("Coordinate x must be between -100 and 100! Please try again!")

            if y < -100 or y > 100:
                raise ValidationException("Coordinate y must be between -100 and 100! Please try again!")

            new_address = Address(addr_id, name, number, x, y)
            self._repo.add_address(new_address)

        except ValidationException as ve:
            print(ve)


    def where_to_place_station(self, x:int, y:int, d:int):
        new_list = []
        addresses = self._repo.get_all()
        for a in addresses:
            if sqrt((a.x - x)*(a.x - x) + (a.y - y)*(a.y - y)) <= d:
                new_list.append(a)
        return new_list

    def new_taxi_station(self):
        addresses = self._repo.get_all()

        forbidden = {(a.x, a.y) for a in addresses}
        best_x = None
        best_y = None
        best_dist_sum = 10000000

        for x in range(-100, 101):
            for y in range(-100, 101):
                if (x,y) in forbidden:
                    continue
                total = 0
                for a in addresses:
                    total += sqrt((a.x - x) ** 2 + (a.y - y) ** 2)

                if total < best_dist_sum:
                    best_x = x
                    best_y = y
                    best_dist_sum = total

        return best_x, best_y