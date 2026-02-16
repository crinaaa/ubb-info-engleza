from domain.player import Player


class PlayerTextFileRepo:
    def __init__(self, filename:str):
        self._filename = filename
        self._players = {}
        self._load_file()

    def _load_file(self):
        with open(self._filename, "r") as fin:
            for line in fin:
                parts = line.strip().split(",")
                player_id = int(parts[0].strip())
                name = parts[1].strip()
                strength = int(parts[2].strip())

                self._players[player_id] = Player(player_id, name, strength)

    def _save_file(self):
        with open(self._filename, "w") as fout:
            for player in self.get_players():
                fout.write(f"{player.id},{player.name},{player.strength}\n")

    def save(self):
        self._save_file()

    def get_players(self):
        return list(self._players.values())

    def delete_player(self, player_id: int):
        del self._players[player_id]