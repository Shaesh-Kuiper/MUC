import pytest
from ythis import add

def test_add_positive_numbers():
    assert add(1, 2) == 3
    assert add(10, 5) == 15

def test_add_negative_numbers():
    assert add(-1, -1) == -2
    assert add(-5, -10) == -15

def test_add_mixed_numbers():
    assert add(-1, 1) == 0
    assert add(5, -3) == 2

def test_add_zero():
    assert add(0, 0) == 0
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_add_large_numbers():
    assert add(1000000, 2000000) == 3000000
    assert add(-1000000, -2000000) == -3000000

def test_add_edge_cases():
    assert add(1, -1) == 0
    assert add(2147483647, 1) == 2147483648  # Testing overflow for 32-bit int
    assert add(-2147483648, -1) == -2147483649  # Testing underflow for 32-bit i
