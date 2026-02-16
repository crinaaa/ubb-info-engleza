from user_interface.ui import ConsoleUI
from gui.nine_morris_gui import NineMensMorrisGUI

def main():
    player_name = input("Enter your name: ").strip() or "Player"

    print("\nSelect Interface:")
    print("1. Console UI")
    print("2. Graphical UI (Pygame)")
    choice = input("Choice (1 or 2): ").strip()

    if choice == "2":
        app = NineMensMorrisGUI()
        app.run()
    else:
        app = ConsoleUI(player_name)
        app.run()

if __name__ == "__main__":
    main()