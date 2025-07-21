import pytest
from add_func import add_function

def test_add_function_positive_numbers():
    assert add_function(1, 2) == 3
    assert add_function(10, 5) == 15
    assert add_function(100, 200) == 300

def test_add_function_negative_numbers():
    assert add_function(-1, -1) == -2
    assert add_function(-5, -10) == -15
    assert add_function(-100, -200) == -300

def test_add_function_mixed_numbers():
    assert add_function(-1, 1) == 0
    assert add_function(-5, 5) == 0
    assert add_function(10, -5) == 5

def test_add_function_zero():
    assert add_function(0, 0) == 0
    assert add_function(0, 5) == 5
    assert add_function(5, 0) == 5

def test_add_function_large_numbers():
    assert add_function(1000000, 2000000) == 3000000
    assert add_function(-1000000, -2000000) == -3000000

def test_add_function_edge_cases():
    assert add_function(1, -1) == 0
    assert add_function(1, 0) == 1
    assert add_function(0, 1) == 1
