import pytest
from nu import add_new

def test_add_new_positive_numbers():
    assert add_new(1, 2) == 3
    assert add_new(10, 5) == 15

def test_add_new_negative_numbers():
    assert add_new(-1, -1) == -2
    assert add_new(-5, -10) == -15

def test_add_new_mixed_numbers():
    assert add_new(-1, 1) == 0
    assert add_new(5, -3) == 2

def test_add_new_zero():
    assert add_new(0, 0) == 0
    assert add_new(0, 5) == 5
    assert add_new(5, 0) == 5

def test_add_new_large_numbers():
    assert add_new(1000000, 2000000) == 3000000
    assert add_new(-1000000, -2000000) == -3000000

def test_add_new_edge_cases():
    assert add_new(1, -1) == 0
    assert add_new(1, 0) == 1
    assert add_new(0, 1) == 1
