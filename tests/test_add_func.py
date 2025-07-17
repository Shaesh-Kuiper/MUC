import pytest
from add_func import add_ints

def test_add_ints_positive_numbers():
    assert add_ints(1, 2) == 3
    assert add_ints(10, 20) == 30

def test_add_ints_negative_numbers():
    assert add_ints(-1, -2) == -3
    assert add_ints(-10, -20) == -30

def test_add_ints_mixed_numbers():
    assert add_ints(-1, 1) == 0
    assert add_ints(5, -3) == 2

def test_add_ints_zero():
    assert add_ints(0, 0) == 0
    assert add_ints(0, 5) == 5
    assert add_ints(5, 0) == 5

def test_add_ints_large_numbers():
    assert add_ints(1000000, 2000000) == 3000000
    assert add_ints(-1000000, -2000000) == -3000000

def test_add_ints_edge_cases():
    assert add_ints(1, -1) == 0
    assert add_ints(2147483647, 1) == 2147483648  # Testing overflow behavior
    assert add_ints(-2147483648, -1) == -2147483649  # Testing underflow behavior
