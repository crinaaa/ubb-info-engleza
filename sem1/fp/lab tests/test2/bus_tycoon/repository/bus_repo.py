from domain.bus import Bus


class BusTextFileRepo:
    def __init__(self, filename):
        self._filename = filename
        self._buses = {}
        self._load_file()

    def _load_file(self):
        with open(self._filename, "r") as fin:
            for line in fin:
                parts = line.split(",")
                bus_id = int(parts[0].strip())
                route = int(parts[1].strip())
                model = parts[2].strip()
                times = int(parts[3].strip())

                self._buses[bus_id] = Bus(bus_id, route, model, times)

    def _save_file(self):
        with open(self._filename, "w") as fout:
            for bus in self.get_buses():
                fout.write(f"{bus.id},{bus.route},{bus.model},{bus.times}\n")

    def add_bus(self, bus: Bus):
        self._buses[bus.id] = bus
        self._save_file()

    def get_buses(self):
        return list(self._buses.values())