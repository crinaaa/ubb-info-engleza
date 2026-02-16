from functions import *

def add_command(products: list, parts: list):
    if len(parts)!=4:
        raise ValueError("Invalid format!")

    name = parts[1]
    try:
        quantity = int(parts[2])
        price = int(parts[3])
    except ValueError:
        raise ValueError("The quantity and the price have to be integers!")

    add_product(products, name, quantity, price)


def remove_command(products:list, parts:list):
    if len(parts)!=2:
        raise ValueError("Invalid format!")

    name = parts[1]

    remove_product(products, name)


def list_all_command(products: list, parts:list):
    if len(parts)!=2  or parts[1]!='all':
        raise ValueError("Invalid format!")

    sorted_list = list_all(products)
    for p in sorted_list:
        print(p)


def list_command(products:list, parts:list):
    if len(parts)!=1:
        raise ValueError("Invalid format")
    for p in products:
        print(p)


def process_command(products: list, command:str):
    parts = command.strip().split()

    if len(parts)==0:
        raise ValueError("Empty command!")

    cmd = parts[0]

    if cmd=="add":
        add_command(products, parts)
        return None
    elif cmd=="remove":
        remove_command(products, parts)
        return None
    elif cmd=="list" and len(parts)==2 and parts[1]=="all":
        list_all_command(products, parts)
        return None
    elif cmd=="list":
        list_command(products, parts)
        return None
    elif cmd=="exit":
        return "exit"
    else:
        raise ValueError("Unknown command!")

def print_ui():
    products = [{"name": "sugar", "price": 20, "quantity": 100},
                {"name": "biscuits", "price": 15, "quantity": 60},
                {"name": "candies", "price": 10, "quantity": 200}]

    while True:
        command = input("Enter your command: ")
        try:
            result = process_command(products, command)
            if result == "exit":
                print("Exiting...")
                break
        except ValueError as ve:
            print(ve)