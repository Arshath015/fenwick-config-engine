"""Fenwick (Binary Indexed) Tree implementation.

Provides point‑update and prefix‑sum operations in O(log n) time.
The tree is 1‑based internally; external API uses 0‑based indexing for
convenience.
"""

from __future__ import annotations

from typing import List


class FenwickTree:
    """Core Fenwick Tree data structure.

    Parameters
    ----------
    size: int
        Number of elements the tree will manage.
    init_values: List[int] | None, optional
        Optional initial values. If provided, the tree is built in O(n).
    """

    def __init__(self, size: int, init_values: List[int] | None = None) -> None:
        self.n = size
        self.tree: List[int] = [0] * (self.n + 1)
        if init_values:
            if len(init_values) != size:
                raise ValueError("init_values length must match size")
            for idx, val in enumerate(init_values):
                self.update(idx, val)

    def _lsb(self, i: int) -> int:
        """Return least significant bit of i (i & -i)."""
        return i & -i

    def update(self, index: int, delta: int) -> None:
        """Add *delta* to element at *index* (0‑based)."""
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += self._lsb(i)

    def prefix_sum(self, index: int) -> int:
        """Return sum of elements[0..index] inclusive (0‑based)."""
        i = index + 1
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= self._lsb(i)
        return result

    def range_sum(self, left: int, right: int) -> int:
        """Return sum of elements[left..right] inclusive.

        Raises
        ------
        ValueError
            If *left* > *right* or indices are out of bounds.
        """
        if left < 0 or right >= self.n:
            raise IndexError("range indices out of bounds")
        if left > right:
            raise ValueError("left index cannot be greater than right index")
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left > 0 else 0)

    def __repr__(self) -> str:
        return f"FenwickTree(size={self.n})"
