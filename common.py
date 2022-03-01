from decimal import Decimal
from fractions import Fraction
from math import sqrt
from typing import Iterable

frac = Fraction
num = int | float | Fraction


def dec(nums: num | Iterable[num]) -> num | list[num]:
    return float(nums) if isinstance(nums, num) else [float(i) for i in nums]


def disc(a: num, b: num, c: num) -> num:
    return (b ** 2) - (4 * a * c)


def quad(a: num, b: num, c: num = frac(0)) -> tuple[num, num]:
    bottom = 2 * a
    right = sqrt(disc(a, b, c)) / bottom
    left = -b / bottom
    # I prefer to make everything rational where possible
    return frac(left - right), frac(left + right)


def expand_binomial(a: num, b: num) -> tuple[num, num, num]:
    return a ** 2, 2 * a * b, b ** 2
