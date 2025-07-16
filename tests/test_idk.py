import pytest
from idk import add_it

def test_add_it_positive_numbers():
    assert add_it(1, 2) == 3
    assert add_it(10, 5) == 15
    assert add_it(100, 200) == 300

def test_add_it_negative_numbers():
    assert add_it(-1, -1) == -2
    assert add_it(-5, -10) == -15
    assert add_it(-100, -200) == -300

def test_add_it_mixed_numbers():
    assert add_it(-1, 1) == 0
    assert add_it(-5, 5) == 0
    assert add_it(10, -5) == 5

def test_add_it_zero():
    assert add_it(0, 0) == 0
    assert add_it(0, 5) == 5
    assert add_it(5, 0) == 5

def test_add_it_large_numbers():
    assert add_it(1000000, 2000000) == 3000000
    assert add_it(-1000000, -2000000) == -3000000
    assert add_it(1000000, -1000000) == 0

def test_add_it_edge_cases():
    assert add_it(1, -1) == 0
    assert add_it(0, -1) == -1
    assert add_it(-1, 0) == -1
