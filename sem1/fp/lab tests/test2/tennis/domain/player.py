class Player:
    def __init__(self, player_id:int, name:str, strength:int):
        self._id = player_id
        self._name = name
        self._strength = strength

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def strength(self):
        return self._strength

    def increase_strength(self):
        self._strength += 1