import pytest
from super_add import super_power_add

def test_super_power_add_positive_integers():
    assert super_power_add(2, 3) == 13
    assert super_power_add(1, 1) == 2
    assert super_power_add(0, 0) == 0

def test_super_power_add_negative_integers():
    assert super_power_add(-2, -3) == 13
    assert super_power_add(-1, -1) == 2
    assert super_power_add(0, -3) == 9

def test_super_power_add_mixed_integers():
    assert super_power_add(2, -3) == 13
    assert super_power_add(-2, 3) == 13
    assert super_power_add(0, 3) == 9

def test_super_power_add_large_integers():
    assert super_power_add(1000, 1000) == 2000000
    assert super_power_add(10000, 10000) == 200000000

def test_super_power_add_edge_cases():
    assert super_power_add(1, 0) == 1
    assert super_power_add(0, 1) == 1
    assert super_power_add(-1, 0) == 1
    assert super_power_add(0, -1) == 1
