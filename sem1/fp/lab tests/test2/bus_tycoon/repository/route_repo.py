from domain.route import Route


class RouteTextFileRepo:
    def __init__(self, filename):
        self._filename = filename
        self._routes = {}
        self._load_file()

    def _load_file(self):
        with open(self._filename, "r") as fin:
            for line in fin:
                parts = line.split(",")

                route_code = int(parts[0].strip())
                length = int((parts[1].strip()))

                self._routes[route_code] = Route(route_code, length)

    def _save_file(self):
        with open(self._filename, "w") as fout:
            for route in self.get_routes():
                fout.write(f"{route.id},{route.length}\n")

    def add_route_repo(self, route: Route):
        self._routes[route.id] = route
        self._save_file()

    def get_routes(self):
        return list(self._routes.values())