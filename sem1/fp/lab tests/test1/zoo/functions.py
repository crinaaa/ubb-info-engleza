from texttable import Texttable

def create_animal(code: str, name: str, typee:str, species:str) -> dict:
    return {"code": code, "name": name, "type": typee, "species": species}

def get_code(animal: dict) -> str:
    return animal['code']

def get_name(animal: dict) -> str:
    return animal['name']

def get_type(animal: dict) -> str:
    return animal['type']

def get_species(animal: dict) -> str:
    return animal['species']

def set_type(animal: dict, new_type: str):
    animal['type'] = new_type

def add_animal(collection: list):
    code = input('Enter code: ')
    if code == '':
        raise ValueError('Invalid code!')
    codes_list = []
    for animal in collection:
        codes_list.append(get_code(animal))
    if code in codes_list:
        raise ValueError('Code already exists!')
    name = input('Enter name: ')
    if name == '':
        raise ValueError('Invalid name!')
    typee = input('Enter type: ')
    if typee == '':
        raise ValueError('Invalid type!')
    species = input('Enter species: ')
    if species == '':
        raise ValueError('Invalid species!')
    collection.append(create_animal(code, name, typee, species))

def modify_type(collection: list):
    code = input('Enter code: ')
    new_type = input('Enter new type: ')
    codes_list = []
    for animal in collection:
        codes_list.append(get_code(animal))
    if code not in codes_list:
        raise ValueError('Code does not exist!')
    for animal in collection:
        if get_code(animal) == code:
            set_type(animal, new_type)

def change_type_species(collection: list):
    species = input('Enter species: ')
    new_type = input('Enter new type: ')
    if new_type == '':
        raise ValueError('Invalid input!')
    else:
        for animal in collection:
            if get_species(animal) == species:
                set_type(animal, new_type)

def sort_ascending(collection: list):
    for i in range(0, len(collection)-1):
        for j in range(i+1, len(collection)):
            if get_name(collection[i]).lower() > get_name(collection[j]).lower():
                collection[i], collection[j] = collection[j], collection[i]

def display_collection(collection: list):
    t = Texttable()
    t.header(['Code', 'Name', 'Type', 'Species'])
    for animal in collection:
        t.add_row([get_code(animal), get_name(animal), get_type(animal), get_species(animal)])
    return t.draw()