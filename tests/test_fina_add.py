import pytest
from fina_add import fina_add

def test_fina_add_positive_numbers():
    assert fina_add(1, 2) == 3
    assert fina_add(10, 5) == 15
    assert fina_add(100, 200) == 300

def test_fina_add_negative_numbers():
    assert fina_add(-1, -1) == -2
    assert fina_add(-5, -10) == -15
    assert fina_add(-100, -200) == -300

def test_fina_add_mixed_numbers():
    assert fina_add(-1, 1) == 0
    assert fina_add(-5, 5) == 0
    assert fina_add(10, -5) == 5

def test_fina_add_zero():
    assert fina_add(0, 0) == 0
    assert fina_add(0, 5) == 5
    assert fina_add(5, 0) == 5

def test_fina_add_large_numbers():
    assert fina_add(1000000, 2000000) == 3000000
    assert fina_add(-1000000, -2000000) == -3000000
    assert fina_add(1000000, -1000000) == 0

def test_fina_add_edge_cases():
    assert fina_add(1, -1) == 0
    assert fina_add(1, 0) == 1
    assert fina_add(0, 1) == 1
