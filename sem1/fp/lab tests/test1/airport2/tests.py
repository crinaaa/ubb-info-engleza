from functions import *

def test_flight():
    f = create_flight("OB3002", 45, "Cluj-Napoca", "London")
    assert get_code(f) == "OB3002"
    assert get_duration(f) == 45
    assert get_departure(f) == "Cluj-Napoca"
    assert get_destination(f) == "London"

def test_add_flight():
    f = []
    add_flight(f, "FL01", 120, "Paris", "London")
    assert len(f) == 1
    assert f == [{"code": "FL01", "duration": 120, "departure city": "Paris", "destination city": "London"}]

def test_all():
    test_flight()
    test_add_flight()

test_all()