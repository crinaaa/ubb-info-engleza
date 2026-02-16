#
# User interface section
#

from functions import *

def add_phone_ui(phone_list:list):
    manufacturer = input("Enter the manufacturer: ")
    model = input("Enter the model: ")
    price = int(input("Enter the price: "))
    add_phone(phone_list, create_phone(manufacturer, model, price))


def find_phone_ui(phone_list:list):
    manufacturer = input("Enter the manufacturer: ")
    t = display_phones(find_phones(phone_list, manufacturer))
    for i in range(0, len(t)):
        print(i + 1, ".", t[i])

def increase_price_amount_ui(phone_list: list):
    manufacturer = input("Enter manufacturer: ")
    model = input("Enter the model: ")
    amount = int(input("Enter the amount: "))
    increase_price_amount(phone_list, manufacturer, model, amount)


def increase_price_percent_ui(phone_list):
    percent = int(input("Enter the percent: "))
    increase_price_percent(phone_list, percent)


def display_all_phones_ui(phone_list: list):
    t = display_phones(phone_list)
    for i in range(0, len(t)):
        print(i+1, ".", t[i])


def print_menu():
    print("1. Add a phone to the list.")
    print("2. Find all phones from a given manufacturer.")
    print("3. Increase the price of a phone by a given amount.")
    print("4. Increase the price of all phones with a given percent.")
    print("5. Display the list of all phones.")
    print("6. Exit.")


def print_ui():
    phone_list = [{"manufacturer": "Samsung", "model": "GalaxyS25", "price": 3000},
                  {"manufacturer": "Huawei", "model": "P20", "price": 2000},
                  {"manufacturer": "Apple", "model": "iPhone15", "price": 5000},
                  {"manufacturer": "Samsung", "model": "A17", "price": 4000}]

    commands = {"1": add_phone_ui, "2": find_phone_ui, "3": increase_price_amount_ui,
                "4": increase_price_percent_ui, "5": display_all_phones_ui}

    while True:
        print_menu()
        try:
            option = input("Enter your option: ")
            if option in commands:
                commands[option](phone_list)
            elif option == "6":
                print("Exiting the program.")
                return
            else:
                print("Invalid option. Try again!")
        except ValueError as ve:
            print(ve)