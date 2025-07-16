import pytest
from add_num import add

def test_add_positive_numbers():
    assert add(1, 2) == 3
    assert add(10, 5) == 15
    assert add(100, 200) == 300

def test_add_negative_numbers():
    assert add(-1, -1) == -2
    assert add(-5, -10) == -15
    assert add(-100, -200) == -300

def test_add_mixed_numbers():
    assert add(-1, 1) == 0
    assert add(-5, 5) == 0
    assert add(10, -5) == 5

def test_add_zero():
    assert add(0, 0) == 0
    assert add(0, 5) == 5
    assert add(5, 0) == 5

def test_add_large_numbers():
    assert add(1000000, 2000000) == 3000000
    assert add(-1000000, -2000000) == -3000000

def test_add_edge_cases():
    assert add(1, -1) == 0
    assert add(1, 0) == 1
    assert add(0, 1) == 1
