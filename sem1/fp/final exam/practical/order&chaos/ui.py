
class ConsoleUI:
    def __init__(self, service):
        self._service = service

    def run(self):
        print("--- ORDER AND CHAOS ---")
        print("1. New Game")
        print("2. Load Game")

        choice = input("> ")

        if choice == "exit":
            return

        if choice == "2":
            if self._service.load_game():
                print("Game loaded successfully!")
            else:
                print("No save file found. Starting new game.")

        while True:
            print(self._service) 

            inp = input("Enter row, col, symbol (e.g., 0 0 X) or 'save': ").split()

            if inp[0] == "exit":
                break

            if inp[0].lower() == 'save':
                self._service.save_game()
                print("Game saved!")
                continue

            # Process Move
            try:
                r, c, s = int(inp[0]), int(inp[1]), inp[2].upper()
                self._service.order_move(r, c, s)
            except Exception as e:
                print(f"Invalid move: {e}")
                continue

            # Check Win (Order)
            if self._service.check_win():
                print(self._service)
                print("ORDER WINS!")
                break

            # Chaos Move
            print("\nChaos (Computer) is moving...")
            self._service.computer_move()

            # Check Win (Order wins even on Chaos move) or Chaos Win (Full board)
            if self._service.check_win():
                print(self._service)
                print("ORDER WINS!")
                break
            elif self._service.is_board_full():
                print(self._service)
                print("CHAOS WINS! The board is full.")
                break