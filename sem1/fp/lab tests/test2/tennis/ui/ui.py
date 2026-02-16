import random

from service.service import PlayerService


class ConsoleUI:
    def __init__(self, repo):
        self._service = PlayerService(repo)
        self._main_players = None  # winners from qualifying
        self._qualifying_played = False  # flag to prevent re-playing qualifying

    def run(self):
        while True:
            print("\n--- Tennis Tournament ---")
            print("1. Display players sorted by strength")
            print("2. Play Qualifying Rounds")
            print("3. Play Tournament")
            print("0. Exit")

            choice = input("Enter choice: ")
            if choice == "1":
                self.sort_players_ui()
            elif choice == "2":
                if self._qualifying_played:
                    print("Qualifying round has already been played and cannot be repeated!")
                else:
                    self.qualifying()
            elif choice == "3":
                self.tournament()
            elif choice == "0":
                break

    def sort_players_ui(self):
        players = self._service.sort_descending_strength()
        for p in players:
            print(f"ID: {p.id}, Name: {p.name}, Strength: {p.strength}")

    def qualifying(self):
        players = self._service.sort_descending_strength()
        qualifying, waiting = self._service.tournament_structure(players)

        if not qualifying:
            print("No qualification matches needed!")
            self._main_players = players
            self._qualifying_played = True
            return

        print("Qualifying Rounds")
        self._main_players = self.play_round_ui(qualifying)
        self._main_players += waiting
        self._qualifying_played = True

        print("\n")
        print("We can begin the TOURNAMENT!")


    def play_round_ui(self, players: list):
        random.shuffle(players)
        winners = []

        for i in range(0,len(players),2):
            p1 = players[i]
            p2 = players[i+1]

            print(f"Match between {p1.name}({p1.strength}) and {p2.name}({p2.strength})")

            winner_choice = int(input("Who won this game? Enter 1 or 2: "))

            if winner_choice == 1:
                p1.increase_strength()
                winners.append(p1)
            else:
                p2.increase_strength()
                winners.append(p2)

        return winners

    def tournament(self):
        all_players = self._service.sort_descending_strength()

        qualifying, _ = self._service.tournament_structure(all_players)
        if qualifying and self._main_players is None:
            print("Qualifying Rounds need to be played first!")
            return

        if self._main_players:
            players = self._main_players
        else:
            players = all_players

        while len(players) >= 2:
            label = f"Last {len(players)}"
            if len(players) == 2:
                label = "Final"

            print(f"{label}")

            players = self.play_round_ui(players)

        winner = players[0]
        print(f"The winner is {winner.name}({winner.strength})!")

        self._service.save()