class BusService:
    def __init__(self, bus_repo, route_repo):
        self._bus_repo = bus_repo
        self._route_repo = route_repo

    def display_bus_on_route(self, route_id:int):
        buses = self._bus_repo.get_buses()
        new_list = []
        for bus in buses:
            if bus.route == route_id:
                new_list.append(bus)

        return new_list

    def compute_km(self, bus_id:int):
        wanted = None
        buses = self._bus_repo.get_buses()
        for bus in buses:
            if bus.id == bus_id:
                wanted = bus
                break
        route = wanted.route
        routes = self._route_repo.get_routes()
        km = 0
        for r in routes:
            if r.id == route:
                km = r.length
                break

        return km * wanted.times


    def mileage_count(self):
        buses = self._bus_repo.get_buses()
        routes = self._route_repo.get_routes()

        l = []

        for r in routes:
            km = 0
            buses_on_route = []

            for b in buses:
                if r.id == b.route:
                    km += self.compute_km(b.id)
                    buses_on_route.append(b)

            l.append((r, km, buses_on_route))

        return l   # a list of routes

    def order_routes(self):
        l = self.mileage_count()
        n = len(l)

        for i in range(n-1):
            for j in range(i+1, n):
                if l[i][1] < l[j][1]:  # compare mileage
                    l[i], l[j] = l[j], l[i]

        return l