import math


class PlayerService:
    def __init__(self, repo):
        self._repo = repo

    def sort_descending_strength(self):
        players = self._repo.get_players()
        n = len(players)
        for i in range(n-1):
            for j in range(i+1, n):
                if players[i].strength < players[j].strength:
                    players[i], players[j] = players[j], players[i]

        return players


    def tournament_structure(self, players:list):
        #returns the players that go into qualifying and those who go directly in the tournament

        n = len(players)
        #find the largest power of 2 smaller than n
        p = 2**int(math.log2(n))

        if n == p:
            return [], players

        games_count = n - p
        players_count = games_count * 2

        qualifying = players[-players_count:]
        waiting = players[:-players_count]

        return  qualifying, waiting

    def save(self):
        self._repo.save()