from functions import *

def test_codes():
    assert codes_count(1234, 1638) == 2
    assert codes_count(1234, 5234) == 3
    assert codes_count(1234, 6789) == 0

def test_runners():
    assert runners_count(1234, 1638) == 0
    assert runners_count(1234, 4321) == 4
    assert runners_count(1234, 2791) == 2

def test_all():
    test_codes()
    test_runners()

test_all()