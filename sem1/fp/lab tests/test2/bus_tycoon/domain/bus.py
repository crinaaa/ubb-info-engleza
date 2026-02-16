class Bus:
    def __init__(self, bus_id:int, route_id:int, model:str, times:int):
        self._id = bus_id
        self._route = route_id
        self._model = model
        self._times = times

    @property
    def id(self):
        return self._id

    @property
    def route(self):
        return self._route

    @property
    def model(self):
        return self._model

    @property
    def times(self):
        return self._times