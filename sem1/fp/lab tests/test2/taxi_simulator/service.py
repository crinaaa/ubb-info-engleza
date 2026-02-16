import random
from domain import Taxi


class TaxiService:
    def __init__(self, repo):
        self._repo = repo

    def validate_coordinates(self, x:int, y:int):
        return 0 <= x <= 100 and 0 <= y <= 100

    def manhattan_distance(self, x1,y1,x2,y2):
        return abs(x1-x2) + abs(y1-y2)

    def generate_taxis(self, taxi_number:int):
        for i in range(taxi_number):
            ok = False
            while not ok:
                ok = True
                x = random.randint(0, 100)
                y = random.randint(0, 100)

                for t in self._repo.get_all():
                    if self.manhattan_distance(x, y, t.x, t.y) <= 5:
                        ok = False
                        break

            self._repo.add_taxi(Taxi(i, x, y, 0))

    def get_taxis(self):
        return self._repo.get_all()

    def add_ride(self, x1, y1, x2, y2):
        taxis = self._repo.get_all()
        nearest = None
        min_dist = 10**9

        for t in taxis:
            d = self.manhattan_distance(x1, y1, t.x, t.y)
            if d < min_dist:
                min_dist = d
                nearest = t

        fare = self.manhattan_distance(x1, y1, x2, y2)

        nearest.fare += fare
        nearest.x = x2
        nearest.y = y2

        self._repo.set_taxi(nearest)

    def simulate_ride(self):
        x1 = random.randint(0, 100)
        y1 = random.randint(0, 100)
        x2 = random.randint(0, 100)
        y2 = random.randint(0, 100)

        while self.manhattan_distance(x1, y1, x2, y2) < 10:
            x1 = random.randint(0, 100)
            y1 = random.randint(0, 100)
            x2 = random.randint(0, 100)
            y2 = random.randint(0, 100)

        self.add_ride(x1, y1, x2, y2)
        return x1, y1, x2, y2

    def display_sorted(self):
        taxis = self.get_taxis()
        taxis.sort(key=lambda t: t.fare, reverse=True)
        return taxis
