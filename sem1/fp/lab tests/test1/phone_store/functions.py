#
# Functions section
#

from texttable import Texttable

def create_phone(manufacturer: str, model: str, price:int) -> dict:
    """
    This functions creates a phone.
    :param manufacturer: manufacturer of the phone
    :param model: model of the phone
    :param price: price of the phone
    :return: the phone, as a dictionary
    :rtype: dict
    """
    if len(manufacturer)<3 or len(model)<3 or price<1000:
        raise ValueError("Invalid input!")
    return {"manufacturer": manufacturer, "model": model, "price": price}

def get_manufacturer(phone:dict) -> str:
    return phone["manufacturer"]

def get_model(phone:dict) -> str:
    return phone["model"]

def get_price(phone:dict) -> int:
    return phone["price"]

def set_manufacturer(phone:dict, new_manufacturer:str) -> None:
    phone["manufacturer"] = new_manufacturer

def set_model(phone:dict, new_model:str) -> None:
    phone["model"] = new_model

def set_price(phone:dict, new_price: int) -> None:
    phone["price"] = new_price

def to_str(phone:dict):
    return str(get_manufacturer(phone)) + ", " + str(get_model(phone)) + ", " + str(get_price(phone))


def add_phone(phone_list:list, phone:dict) -> None:
    """
    This functions adds a phone to the list of phones.
    :param phone_list: the current list of phones
    :param phone: the phone we want to add
    """
    phone_list.append(phone)

def find_phones(phone_list: list, manufacturer: str) -> list:
    l = []
    for phone in phone_list:
        if manufacturer.lower() in get_manufacturer(phone).lower():
            l.append(phone)
    return l

def increase_price_amount(phone_list: list, manufacturer: str, model:str, amount:int) -> None:
    wanted = None
    ok = False
    for phone in phone_list:
        if get_manufacturer(phone) == manufacturer and get_model(phone) == model:
            ok = True
            wanted = phone
    if not ok:
        raise ValueError("There is no phone with the given manufacturer and model name!")
    set_price(wanted, get_price(wanted) + amount)


def increase_price_percent(phone_list:list, percent: int):
    if percent<-50 or percent>100:
        raise ValueError("Invalid percent!")
    for phone in phone_list:
        set_price(phone, get_price(phone) + get_price(phone)*percent//100)

def display_phones(phone_list: list):
    # t = Texttable()
    # t.header(["Manufacturer", "Model", "Price"])
    # for phone in phone_list:
    #     t.add_row([get_manufacturer(phone), get_model(phone), get_price(phone)])
    # return t
    t = []
    for phone in phone_list:
        t.append(to_str(phone))
    return t