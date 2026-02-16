from exceptions import ValidationException, GameException
from texttable import Texttable


class ConsoleUI:
    def __init__(self, service):
        self._service = service
        self._cheat = False

    from texttable import Texttable

    def print_board(self):
        table = Texttable()
        # 14 columns: [Row#] [6 Player] [Spacer] [6 Computer]
        table.set_cols_align(["c"] * 14)
        table.set_cols_valign(["m"] * 14)

        # Manually build the header to ensure it has 14 elements
        header = [' ', 'A', 'B', 'C', 'D', 'E', 'F', ' ', 'A', 'B', 'C', 'D', 'E', 'F']
        table.add_row(header)

        for row in range(6):
            # Start the row with the row number
            current_row = [str(row)]

            # 6 Player columns
            for col in range(6):
                current_row.append(self._service.get_player_status(col, row))

            # 1 Spacer column
            current_row.append(" ")

            # 6 Computer columns
            for col in range(6):
                current_row.append(self._service.get_computer_status(col, row, self._cheat))

            table.add_row(current_row)

        print("\n" + table.draw())
        print("      PLAYER BOARD                TARGETING BOARD")


    def run(self):
        while True:
            self.print_board()
            cmd = input("> ").strip().split()

            if not cmd:
                continue

            command = cmd[0].lower()

            try:
                if command == "ship":
                    self._service.place_ship(cmd[1])

                elif command == "start":
                    self._service.start_game()
                    print("Game started! Place your ships!")

                elif command == "attack":
                    res = self._service.player_attack(cmd[1])
                    print(f"Player {res}")

                    if self._service.check_winner() == "player":
                        print("You won!")
                        break

                    #computer's turn
                    c_res, c_coord = self._service.computer_attack()
                    print(f"Computer attacks at {c_coord} - {c_res}")

                    if self._service.check_winner() == "computer":
                        print("You lost! Try again!")
                        break

                elif command == "cheat":
                    self._cheat = not self._cheat

                elif command == "exit":
                    break

                else:
                    print("Invalid command!")
            except (ValidationException, GameException, Exception) as e:
                print(e)