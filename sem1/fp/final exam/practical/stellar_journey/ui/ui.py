import texttable
from service.service import GameService


class ConsoleUI:
    def __init__(self, service: GameService):
        self._service = service
        self._service.generate_random_stars()
        self._service.generate_random_e()
        self._service.generate_random_b()

    def print_ui(self, cheat = False):
        board = self._service.get_board(cheat)
        table = texttable.Texttable()
        table.add_rows(board)
        print(table.draw())

    def play(self):
        self.print_ui()
        while not self._service.game_over:
            command = input("Enter your command: ")
            command_separated = command.split(" ")
            if len(command_separated) == 1:
                if command == "cheat":
                    self.print_ui(True)
                else:
                    print("Invalid command!")
            elif len(command_separated) == 2:
                if len(command_separated[1]) != 2 or not (
                        'A' <= command_separated[1][0] <= 'H') or not (
                        '1' <= command_separated[1][1] <= '8'):
                    print("Invalid pair of coordinates! Please try again!")
                elif command_separated[0] == "warp":
                    response = self._service.warp_command(command_separated[1])
                    if response != "True":
                        print(response)
                    if self._service.game_over != 0:
                        break
                    self.print_ui()
                elif command_separated[0] == 'fire':
                    response = self._service.fire_command(command_separated[1])
                    if response != "True":
                        print(response)
                    if self._service.game_over != 0:
                        break
                    self.print_ui()
                else:
                    print("Invalid command! Please try again!")
            else:
                print("Invalid command! Please try again!")
        if self._service.game_over == 2:
            print("You destroyed all the ships. You won!!!!")