from domain import Address
from exceptions import RepoException


class TextRepo:
    def __init__(self, filename = "locations.txt"):
        self._addresses = {}
        self._filename = filename
        self._load_file()

    def add_address(self, new_address: Address):
        if new_address.id in self._addresses:
            raise RepoException("Address with given ID already exists!")
        self._addresses[new_address.id] = new_address
        self._save_file()

    def get_all(self):
        return list(self._addresses.values())

    def _load_file(self):
        try:
            with open(self._filename, "r") as fin:
                for line in fin:
                    line = line.strip()
                    if line:
                        parts = line.split(",")
                        if len(parts)!=5:
                            continue    #skip bad lines

                        addr_id = int(parts[0])
                        name = parts[1]
                        number = int(parts[2])
                        x = int(parts[3])
                        y = int(parts[4])

                        address = Address(addr_id, name, number, x, y)
                        self._addresses[addr_id] = address
        except EOFError:
            pass

    def _save_file(self):
        try:
            with open(self._filename, "w") as fout:
                for address in self.get_all():
                    fout.write(f"{address.id}, {address.name}, {address.number}, {address.x}, {address.y}\n")
        except EOFError:
            pass