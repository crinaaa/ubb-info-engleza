from functions import *

def print_menu():
    print("1. Add an animal to the collection.")
    print("2. Modify the type of an animal from the collection.")
    print("3. Change the type of a species from the collection.")
    print("4. Sort the animals by their name, in ascending order.")
    print("5. Display the whole collection of animals.")


def print_ui():
    collection = [
        create_animal("Z01", "Alex", "herbivore", "zebra"),
        create_animal("L02", "Simba", "carnivore", "lion"),
        create_animal("T03", "Sheru", "carnivore", "tiger"),
        create_animal("G04", "Melman", "herbivore", "giraffe"),
        create_animal("B05", "Gloria", "herbivore", "buffalo"),
        create_animal("E06", "Ellie", "herbivore", "elephant"),
        create_animal("H07", "Marty", "herbivore", "hippo")
    ]

    commands = {"1": add_animal, "2": modify_type, "3": change_type_species, "4": sort_ascending, "5": display_collection}

    while True:
        print_menu()
        option = input(">")

        try:
            if option in commands:
                commands[option](collection)
                table = display_collection(collection)
                print(table)
            elif option == "x":
                print("Exiting program...")
                return
            else:
                print("Invalid option!")

        except ValueError as ve:
            print(ve)