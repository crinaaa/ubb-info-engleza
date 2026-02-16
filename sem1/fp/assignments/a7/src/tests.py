from functions import *

def test_add_number():
    numbers = []
    add_number("3+4i", numbers)
    assert numbers == [[3, 4]]

    add_number("10-2i", numbers)
    assert numbers == [[3, 4], [10, -2]]

def test_insert_number():
    numbers = [[1, 1], [2, 2], [3, 3]]
    insert_number("5+5i", numbers, 1)
    assert numbers == [[1, 1], [5, 5], [2, 2], [3, 3]]

def test_remove_position():
    numbers = [[1, 1], [2, 2], [3, 3]]
    remove_position(1, numbers)
    assert numbers == [[1, 1], [3, 3]]

def test_remove_start_end():
    numbers = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]
    remove_start_end(1, 3, numbers)
    assert numbers == [[1, 1], [5, 5]]

def test_replace_x_y():
    numbers = [[1, 1], [2, 2], [1, 1], [3, 3]]
    replace_x_y("1+1i", "9+9i", numbers)
    assert numbers == [[9, 9], [2, 2], [9, 9], [3, 3]]

def test_add_spaces():
    numbers = []
    add_number("  -7   +   8i  ", numbers)
    assert numbers == [[-7, 8]]

def test_all():
    test_add_number()
    test_insert_number()
    test_remove_position()
    test_remove_start_end()
    test_replace_x_y()
    test_add_spaces()

test_all()