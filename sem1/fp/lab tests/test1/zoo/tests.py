from functions import *

def test_animal():
    a = create_animal("X07", "Laura", "omnivore", "kangaroo")
    assert get_code(a) == "X07"
    assert get_name(a) == "Laura"
    assert get_type(a) == "omnivore"
    assert get_species(a) == "kangaroo"

test_animal()