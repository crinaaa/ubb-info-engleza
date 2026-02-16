from random import randint

def get_digits(number: int):
    digits = []
    digits.append(number // 1000)
    digits.append(number // 100 % 10)
    digits.append(number // 10 % 10)
    digits.append(number % 10)
    return digits

def valid(number: int) -> bool:
    digits = get_digits(number)
    if digits[0] == 0:
        return False
    if (digits[0] == digits[1] or digits[0] == digits[2] or digits[0] == digits[3]
        or digits[1] == digits[2] or digits[1] == digits[3] or digits[2] == digits[3]):
        return False
    return True

def input_validation(number:int)->bool:
    if len(get_digits(number)) != 4:
        return False
    else:
        if valid(number):
            return True
    return False

def generate_number() -> int:
    found = False
    number = 0
    while not found:
        number = randint(1023, 9876)
        if valid(number):
            found = True
    return number

def codes_count(number_computer: int, number_human:int) -> int:
    counter = 0
    digits_c = get_digits(number_computer)
    digits_h = get_digits(number_human)
    for i in range(4):
        if digits_c[i] == digits_h[i]:
            counter += 1
    return counter

def runners_count(number_computer: int, number_human: int) -> int:
    counter = 0
    digits_c = get_digits(number_computer)
    digits_h = get_digits(number_human)
    for c in range(4):
        for h in range(4):
            if digits_c[c] == digits_h[h] and c!=h:
                counter += 1
    return counter