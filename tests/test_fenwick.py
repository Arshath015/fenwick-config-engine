import pytest
from engine.fenwick import FenwickTree

def test_basic_operations():
    ft = FenwickTree(5)
    ft.update(0, 1)
    ft.update(1, 2)
    ft.update(2, 3)
    assert ft.prefix_sum(2) == 6
    assert ft.range_sum(1, 3) == 5  # 2+3+0

def test_invalid_range():
    ft = FenwickTree(3, [1, 2, 3])
    with pytest.raises(ValueError):
        ft.range_sum(2, 1)  # left > right
    with pytest.raises(IndexError):
        ft.range_sum(-1, 2)
        ft.range_sum(0, 3)
