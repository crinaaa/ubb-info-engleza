from functions import *

def test_flight():
    f = create_flight("GH678", 45, "London", "Paris")
    assert get_code(f) == "GH678"
    assert get_duration(f) == 45
    assert get_departure(f) == "London"
    assert get_destination(f) == "Paris"

def test_all():
    test_flight()

test_all()