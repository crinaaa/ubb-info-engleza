from domain import Taxi

class MemoryRepo:
    def __init__(self):
        self._taxis = {}        # id → Taxi

    def add_taxi(self, taxi: Taxi):
        self._taxis[taxi.id] = taxi

    def get_all(self):
        return list(self._taxis.values())

    def set_taxi(self, new_taxi: Taxi):
        self._taxis[new_taxi.id] = new_taxi
