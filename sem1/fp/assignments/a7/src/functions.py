#
# The program's functions are implemented here. There is no user interaction in this file,
# therefore no input/print statements. Functions here
# communicate via function parameters, the return statement and raising of exceptions. 
#
import random
import re
import math
from texttable import Texttable


def create_complex_number(real: int, imag: int) -> list:
    """
    Create a complex number represented as a list [real, imag].
    :param real: Real part of the complex number.
    :param imag: Imaginary part of the complex number.
    :return: Complex number [real, imag].
    :rtype: list
    """
    return [real, imag]

def get_real(c: list) -> int:
    """
    Return the real part of a complex number.
    :param c: Complex number as a list.
    :return: Real part of the complex number.
    :rtype: int
    """
    return c[0]

def get_imag(c: list) -> int:
    """
    Return the imaginary part of a complex number.
    :param c: Complex number as a list.
    :return: Imaginary part of the complex number.
    :rtype: int
    """
    return c[1]

def set_real(c: list, value: int) -> None:
    """
    Set the real part of a complex number.
    :param c: Complex number as a list.
    :param value: Value to be assigned to the real part of the complex number.
    :rtype: None
    """
    c[0] = value

def set_imag(c: list, value: int) -> None:
    """
    Set the imaginary part of a complex number.
    :param c: Complex number as a list.
    :param value: Value to be assigned to the imaginary part of the complex number.
    :rtype: None
    """
    c[1] = value

def complex_to_string(c:list) -> str:
    """
    Convert a complex number to a string in the form 'a+bi'.
    :param c: Complex number [real, imag].
    :return:String representation of the complex number.
    :rtype: str
    """
    real = get_real(c)
    imag = get_imag(c)
    sign = '+' if imag >= 0 else ''
    return f"{real}{sign}{imag}i"

def generate_random_number() -> list:
    """
    Generate a list of 10 random complex numbers with real and imaginary parts
    between -20 and 20.
    :return: List of 10 complex numbers.
    :rtype: list
    """
    l = []
    for i in range(10):
        l.append(create_complex_number(random.randint(-20, 20), random.randint(-20, 20)))
    return l

#from reading a+bi from the console, we get our complex number
def get_complex_number(number: str) -> list:
    """
    Parse a string as a complex number and return [real, imag].
    :param number: Complex number string, e.g., "3+4i" or "-2-5i"
    :return: Complex number [real, imag]
    :rtype: list
    :raises ValueError: If the string is not a complex number.
    """
    number = number.replace(" ", "")

    # Must end in 'i'
    if not number.endswith("i"):
        raise ValueError("Number must end with 'i'.")

    number = number[:-1]  # remove trailing 'i'

    # split into real + imaginary parts
    parts = re.split(r'(?<!^)(?=[+-])', number)

    if len(parts) != 2:
        raise ValueError("Invalid complex number format! Expected a+bi or a-bi.")

    try:
        real = int(parts[0])
        if parts[1] not in ("+", "-"):
            imag = int(parts[1])
        else:
            if parts[1] == "+":
                imag = 1
            else:
                imag = -1
    except ValueError:
        raise ValueError("Real and imaginary part of complex number must be integers!")

    return create_complex_number(real, imag)



def add_number(number: str, number_list: list) -> None:
    """
    Add a complex number to the end of a list.
    :param number: Complex number string.
    :param number_list: List to append to.
    :rtype: None
    """
    number_list.append(get_complex_number(number))


def insert_number(number: str, number_list: list, pos: int) -> None:
    """
    Insert a complex number at a specific position in the list.
    :param number: Complex number string.
    :param number_list: List to modify.
    :param pos: Position to insert at.
    :raises ValueError: if position is out of range or number string invalid.
    :rtype: None
    """
    if pos >= len(number_list) or pos < 0:
        raise ValueError("Position out of range!")
    new_number = get_complex_number(number)
    number_list.append(None)
    for i in range(len(number_list)-1, pos, -1):
        number_list[i] = number_list[i-1]
    number_list[pos] = new_number


def remove_position(pos: int, number_list: list) -> None:
    """
    Remove a complex number at a specific position.
    :param pos: Position to remove.
    :param number_list: List to modify.
    :raises ValueError: if position is invalid.
    :rtype: None
    """
    if pos >= len(number_list) or pos < 0:
        raise ValueError("Position out of range!")
    for i in range(pos, len(number_list) - 1):
        number_list[i] = number_list[i + 1]
    number_list.pop()


def remove_start_end(start: int, end: int, number_list: list) -> None:
    """
    Remove a range of numbers from the list.
    :param start: Start index.
    :param end: End index.
    :param number_list: List to modify.
    :raises ValueError: if 'start' and 'end' are out of range.
    :rtype: None
    """
    if start < 0 or end < 0 or start >= len(number_list) or end >= len(number_list):
        raise ValueError("Position out of range!")
    if start > end:
        raise ValueError("Start cannot be greater than end!")
    count = end - start + 1  # how many elements to delete
    for i in range(start, len(number_list) - count):
        number_list[i] = number_list[i+count]
    for i in range(count):
        number_list.pop()


def replace_x_y(num1: str, num2: str, number_list: list) -> None:
    """
    Replace all occurrences of a complex number with a given complex number.
    :param num1: Number to be replaced.
    :param num2: Number to be replaced with.
    :param number_list: List to modify.
    :raises ValueError: if num1 is not found in the list.
    :rtype: None
    """
    nb_to_replace = get_complex_number(num1)
    nb_to_add = get_complex_number(num2)
    found = False
    for i in range(len(number_list)):
        if number_list[i] == nb_to_replace:
            number_list[i] = nb_to_add
            found = True
    if not found:
        raise ValueError("The number you wish to replace is not in the list!")

def list_real_number(number_list: list, start: int, end: int) -> list:
    """
    List real numbers (imaginary part = 0) between positions 'start' and 'end'.
    :param number_list: List to search.
    :param start: Start index.
    :param end: End index.
    :raises ValueError: if 'start' and 'end' are out of range.
    :return: List of real numbers.
    :rtype: list
    """
    if start < 0 or end < 0 or start >= len(number_list) or end >= len(number_list):
        raise ValueError("Position out of range!")
    if start > end:
        raise ValueError("Start cannot be greater than end!")
    list_real = []
    for i in range(start, end + 1):
        if get_imag(number_list[i]) == 0:
            list_real.append(number_list[i])
    return list_real


def get_modulo(c: list) -> float:
    """
    Calculate the modulus of a complex number.
    :param c: Complex number as a list.
    :return: Modulus of complex number.
    :rtype: float
    """
    real = get_real(c)
    imag = get_imag(c)
    return math.sqrt(real*real + imag*imag)


def list_modulo(number_list: list, symbol: str, limit: int) -> list:
    """
    Filter numbers by modulus with a comparison operator.
    :param number_list: List to filter.
    :param symbol: '<', '=', or '>'
    :param limit: Threshold value.
    :raises ValueError: if 'symbol' is invalid.
    :return: The list of numbers that satisfy the condition.
    :rtype: list
    """
    if symbol not in ('<', '=', '>'):
        raise ValueError("Invalid symbol!")
    list_modulos = []
    for i in range(len(number_list)):
        if symbol == '=':
            if get_modulo(number_list[i]) == limit:
                list_modulos.append(number_list[i])
        elif symbol == '<':
            if get_modulo(number_list[i]) < limit:
                list_modulos.append(number_list[i])
        else:
            if get_modulo(number_list[i]) > limit:
                list_modulos.append(number_list[i])
    return list_modulos


def filter_real(number_list: list) -> None:
    """
    Remove all numbers with non-zero imaginary part.
    :param number_list: List to modify.
    :rtype: None
    """
    i = 0
    while i < len(number_list):
        if get_imag(number_list[i]) != 0:  # remove if imaginary ≠ 0
            number_list.pop(i)
        else:
            i += 1


def filter_modulo(number_list: list, symbol: str, limit: int) -> None:
    """
    Remove numbers that do not satisfy modulus condition.
    :param number_list: List to modify.
    :param symbol: '<', '=', or '>'
    :param limit: Threshold value.
    :raises ValueError: if 'symbol' is invalid.
    :rtype: None
    """
    if symbol not in ('<', '=', '>'):
        raise ValueError("Invalid symbol!")

    i = 0
    while i < len(number_list):
        mod = get_modulo(number_list[i])
        remove = False
        if symbol == "<":
            if mod >= limit:  # remove numbers that do not satisfy the condition
                remove = True
        elif symbol == "=":
            if mod != limit:
                remove = True
        elif symbol == ">":
            if mod <= limit:
                remove = True

        if remove:
            for j in range(i, len(number_list) - 1):
                number_list[j] = number_list[j + 1]
            number_list.pop()
        else:
            i += 1

def save_state(number_list: list, history: list) -> None:
    """
    Save a copy of the current list state to the history.
    :param number_list: Current list.
    :param history: History stack, as a list, to append to.
    :rtype: None
    """
    copied_list = [c[:] for c in number_list]
    history.append(copied_list)


def undo_state(number_list: list, history: list) -> None:
    """
    Undo the last operation by restoring the previous list state.
    :param number_list: Current list.
    :param history: History stack, as a list.
    :raises ValueError: if 'history' is empty/ no previous state available.
    :rtype: None
    """
    if not history:
        raise ValueError("No more undo's available!")
    previous_list = history.pop()
    number_list.clear()
    number_list.extend(previous_list)


def build_numbers_table(numbers: list) -> Texttable:
    """
    Build a Texttable representing the list of complex numbers.
    :param numbers: List of numbers.
    :return: Textable representing the list of complex numbers.
    :rtype: Texttable
    """
    table = Texttable()
    table.header(["Index", "Real", "Imag"])
    table.set_deco(Texttable.HEADER | Texttable.VLINES | Texttable.HLINES)

    for i, c in enumerate(numbers):
        table.add_row([i, get_real(c), get_imag(c)])

    return table